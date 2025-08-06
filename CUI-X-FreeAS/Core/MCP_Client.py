import asyncio
from typing import Optional, Dict, List, Tuple
from contextlib import AsyncExitStack
import json
import os
import re
import datetime
from lxml import etree
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
from dotenv import load_dotenv
import traceback
load_dotenv()

class ServerConnection:
    def __init__(self, name: str, session: ClientSession, exit_stack: AsyncExitStack):
        self.name = name
        self.session = session
        self.exit_stack = exit_stack
        self.tools = []

class MCPClient:
    def __init__(self, ConfigPath):
        self.servers: Dict[str, ServerConnection] = {}
        self.active_servers: List[str] = []
        self.API_KEY = os.getenv("API_KEY")
        self.BASE_URL = os.getenv("BASE_URL")
        self.MODEL = os.getenv("MODEL")
        self.ConfigPath = ConfigPath
        self.client = OpenAI(api_key=self.API_KEY, base_url=self.BASE_URL)
        self.messages = []
        try:
            an_path = os.path.join(self.ConfigPath, "Agent_list.txt")
            if not os.path.exists(an_path):
                Agent_name = ""
            with open (an_path, "r", encoding="gbk") as file:
                AgentName = file.read()
            prompt_path = os.path.join(self.ConfigPath, "Prompt.txt")
            if os.path.exists(prompt_path):
                try:
                    with open(prompt_path, "r", encoding="utf-8", errors="ignore") as f:
                        prompt_content = f.read()
                    agent_lines = [line.strip() for line in AgentName.strip().split('\n') if line.strip()]
                    formatted_agents = '\n'.join([f"- {agent}" for agent in agent_lines])
                    updated_prompt = prompt_content.replace(
                        "{AgentName}", 
                        formatted_agents if formatted_agents else "暂无可用Agent"
                    )
                    with open(prompt_path, "w", encoding="utf-8") as f:
                        f.write(updated_prompt)                        
                except Exception as e:
                    print(f"更新列表时出错: {e}")
            with open(prompt_path, "r", encoding="utf-8") as file:
                self.system_prompt = file.read()
        except FileNotFoundError:
            print(f"警告: Prompt.txt 文件未找到")
        self.mcp_servers = self._load_mcp_config()
        self.max_servers = 5

    def _load_mcp_config(self) -> Dict:
        try:
            config_path = os.path.join(self.ConfigPath, "mcp.json")
            if not os.path.exists(config_path):
                print(f"警告: {config_path} 文件未找到")
                return {}
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get('mcpServers', {})
        except json.JSONDecodeError as e:
            print(f"错误: mcp.json 格式错误: {e}")
            return {}
        except Exception as e:
            print(f"错误: 读取 mcp.json 失败: {e}")
            return {}

    async def connect_servers(self, server_names: Optional[List[str]] = None):
        if not self.mcp_servers:
            print("警告: 没有可用的MCP服务器配置")
            return
        if server_names is None:
            server_names = list(self.mcp_servers.keys())[:self.max_servers]
        print(f"开始连接 {len(server_names)} 个MCP服务器...")
        for server_name in server_names:
            try:
                await self._connect_single_server(server_name)
            except Exception as e:
                print(f"连接服务器 {server_name} 失败: {e}")
                continue
        if self.servers:
            print(f"成功连接 {len(self.servers)} 个服务器: {list(self.servers.keys())}")
            await self._update_system_prompt()
        else:
            print("警告: 没有成功连接任何MCP服务器")

    async def _connect_single_server(self, server_name: str):
        if server_name in self.servers:
            return
        server_config = self.mcp_servers.get(server_name)
        if not server_config:
            raise ValueError(f"未找到服务器配置: {server_name}")
        command = server_config.get("command")
        args = server_config.get("args", [])
        env = server_config.get("env", {})
        if not command:
            raise ValueError(f"服务器 {server_name} 缺少 command")
        if not isinstance(args, list):
            raise ValueError(f"服务器 {server_name} 的 args 必须是列表")
        exit_stack = AsyncExitStack()
        try:
            merged_env = os.environ.copy()
            merged_env.update(env)
            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=merged_env,
            )
            stdio_transport = await exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            stdio, write = stdio_transport
            session = await exit_stack.enter_async_context(
                ClientSession(stdio, write)
            )
            await session.initialize()
            response = await session.list_tools()
            server_conn = ServerConnection(server_name, session, exit_stack)
            server_conn.tools = response.tools
            self.servers[server_name] = server_conn
            self.active_servers.append(server_name)
            print(f"[成功] 已连接 {server_name} ({len(response.tools)} 个工具)")
        except Exception as e:
            await exit_stack.aclose()
            raise e

    async def _update_system_prompt(self):
        """更新系统提示，包含所有可用工具"""
        if not self.servers:
            return
        all_tools = []
        for server_name, server_conn in self.servers.items():
            for tool in server_conn.tools:
                all_tools.append(
                    f'##{server_name}\n### Available Tools\n- {tool.name}\n{tool.description}\n{json.dumps(tool.inputSchema)}'
                )
        tools_info = "\n".join(all_tools)
        self.system_prompt = self.system_prompt.replace(
            "<$MCP_INFO$>", f"{tools_info}\n<$MCP_INFO$>"
        )

    async def mcp_use(self, server_name: str, tool_name: str, tool_args: dict) -> str:
        """在指定服务器上调用工具"""
        if server_name not in self.servers:
            return f"错误: 服务器 {server_name} 未连接"
        try:
            server_conn = self.servers[server_name]
            result = await server_conn.session.call_tool(tool_name, tool_args)
            return str(result)
        except Exception as e:
            return f"工具调用失败: {str(e)}"

    async def process_query(self, query: str) -> str:
        """处理用户input"""
        if not self.servers:
            return "警告: 没有可用的MCP服务器"
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query}
        ]
        max_iterations = 50
        final_response = ""
        for iteration in range(max_iterations):
            try:
                response = await self.llm_call()
                print(f"[ToolUse] 调用 {iteration + 1}/{max_iterations}")
                print(f"[LLM] 响应: {response[:100]}...")
                if 'Mcp调用终止' in response.lower():
                    final_response = response
                    return final_response
                if '<use_mcp_tool>' not in response:
                    final_response = response
                    return final_response
                server_name, tool_name, tool_args = self.parse_tool_string(response)
                if server_name not in self.servers:
                    error_msg = f"错误: 服务器 {server_name} 未连接"
                    return error_msg
                print(f"[ToolUse] ToolUse: {tool_name} 参数: {tool_args}")
                tool_result = await self.mcp_use(server_name, tool_name, tool_args)
                print(f"[ToolUse] ToolUse 结果: {tool_result}")
                self.messages.append({"role": "assistant", "content": response})
                self.messages.append({
                    "role": "user",
                    "content": f"[工具 {tool_name} 返回: {tool_result}]"
                })
            except Exception as e:
                error_msg = f"处理过程中发生错误: {str(e)}"
                print(f"[ToolUse] 调用 {iteration + 1} 发生错误: {str(e)}")
                return error_msg
        final_response = f"达到最大调用次数({max_iterations})，任务可能需要更复杂的处理"
        return final_response

    async def llm_call(self) -> str:
        """调用LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                max_tokens=2048,
                messages=self.messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM调用失败: {str(e)}"

    def parse_tool_string(self, tool_string: str) -> tuple[str, str, dict]:
        """解析工具调用字符串"""
        try:
            match = re.search(r"<use_mcp_tool>(.*?)</use_mcp_tool>", tool_string, re.DOTALL)
            if not match:
                raise ValueError("未找到工具调用")
            tool_xml = match.group(1).strip()
            root = etree.fromstring(f"<root>{tool_xml}</root>")
            server_name = root.findtext("server_name", default=list(self.servers.keys())[0] if self.servers else "unknown")
            tool_name = root.findtext("tool_name")
            arguments = root.findtext("arguments")
            if not tool_name or not arguments:
                raise ValueError("缺少必要的工具名称或参数")
            try:
                tool_args = json.loads(arguments)
            except json.JSONDecodeError:
                raise ValueError("工具参数 JSON 解析失败")
            return server_name, tool_name, tool_args
        except Exception as e:
            raise ValueError(f"解析工具调用失败: {e}")

    async def cleanup(self):
        """清理所有连接"""
        for server_conn in list(self.servers.values()):
            try:
                if hasattr(server_conn, 'exit_stack') and server_conn.exit_stack:
                    try:
                        await asyncio.wait_for(server_conn.exit_stack.aclose(), timeout=2.0)
                    except asyncio.TimeoutError:
                        pass
                    except asyncio.CancelledError:
                        pass
                    except Exception:
                        pass
            except Exception:
                pass
        self.servers.clear()
        self.active_servers.clear()
    async def get_available_servers(self) -> List[str]:
        """获取可用服务器列表"""
        return list(self.servers.keys())

    async def get_server_tools(self, server_name: str) -> List[str]:
        """获取服务器可用工具"""
        if server_name not in self.servers:
            return []
        return [tool.name for tool in self.servers[server_name].tools]
    async def main_loop(self, output_file=None):
        try:
            while True:
                try:
                    print(".")                       
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(".")
        except Exception as e:
            print(".")
        finally:
            await self.cleanup()

async def main(userq, ConfigPath):
    try:
        client = MCPClient(ConfigPath)
        await client.connect_servers()
        if not userq:
            print("请输入内容！")
            return "请输入内容！"
        print("AI-Agent 正在处理中...")
        response = await client.process_query(userq)
        print(f"CUI X-HiOS> {response}")
    except asyncio.CancelledError:
        pass
    except Exception as e:
        error_msg = f"处理过程中发生错误: {str(e)}"
        print(f"\n{error_msg}")
        print(traceback.format_exc())
        return error_msg
    finally:
        try:
            await client.cleanup()
        except asyncio.CancelledError:
            pass
        except Exception:
            pass

def AgentMain(userq, ConfigPath):
    try:
        return asyncio.run(main(userq, ConfigPath))
    except Exception as e:
        error_msg = f"Agent执行错误: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return error_msg

if __name__ == "__main__":
    print("未启用调试模式")