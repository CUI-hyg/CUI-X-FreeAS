# CUI-X-FreeAS 下一代Agent框架
### 由于CUI-X-HiOS项目的开发陷入了困境中,Agent框架几乎崩溃且经过2天的抢救仍无力回天。故这次重构整个架构,改了名字,为大家带来更Free的体验！

经过几个月的开发与打磨，CUI X-FreeAS (CUI X-Sides Free Agent System) MAS 正式亮相啦~🎉🎉🎉

## Flag
- **使命**:从六个"Free"角度重新出发：免费、自由、随意扩张Agent、自由Agents组队(开发中)、自由Plugin/tools开发、自由创造你的⌜CUI-X-FreeAS⌟ (开发中)。
- **目标&愿景**:让Ai能够自主创新、自我改进，成为L5级别的AgentOS.

## What
X-FreeAS 就是将记忆、工具、规划、理解、分析等Agent能力接入具有推理能力的LLM中。
打个比方：LLM相当于人类的脑子,记忆、工具、规划、理解、分析等能力是人类的Body。
CUI-X-FreeAS 希望能在将来不久内实现人类无干预自主操作用户电脑完成任务

## Why
不管是什么人，用电脑干活儿基本是以下流程：
- 搜索大量资料
- 修改各类文件、修BUG
- 整理数据，提交结果…
- ………

所以，CUI X-FreeAS的目标是，通过记忆、工具、规划、理解、分析等，成为你的助手，甚至是你的"替身"，将步骤简化到如下所示：
- 描述需求
- Agents处理任务
- 阅读结果，提交

是不是简单很多？

CUI X-FreeAS的终极目标就是通过精细化需求描述，自动化执行任务，输出一份完美的报告。

# How
CUI X-FreeAS本质是一个AgentsSystem,通过主Agent调用工具、AGENTS来完成任务。
它会先理解，然后规划，生成工作流，根据工作流调用具有相应能力的智能体完成任务，并支持随机应变能力(测试中)，并生成报告。

当它执行任务时，你也可以一起工作，结合AgentsSystem的结果、答案，使你的效率更上一层楼。
甚至，你还可以把你的电脑交给它，只需要精确的描述，它会自动操作你的电脑（目前可用，但执行成功是个概率游戏☺️）

## Usage
### 由于本人没有Apple电脑(懂的都懂)，所以暂时不支持MacOS、移动端、Liunx、HarmonyOSNEXT，仅支持Windows。
1.此版本需要添加两个.env文件：一个在主目录下，一个在GUIOperator(必须使用VLLM)
格式如下：
(这里使用OpenAI通用API格式)
```env
OPENAI_API_KEY = sk-你的key
BASE_URL = https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL = Moonshot-Kimi-K2-Instruct
#建议到阿里云百炼获取API,新人有免费额度
#主模型建议使用agent能力、coding能力强的模型：kimi k2、qwen235b-a22b-*-2507、glm4.5……
#GUIOperator下的建议同上
```
另一个是```环境变量```
```cmd
//1.临时使用
set API_Key=sk-你的key
//2.永久使用（Windows可在高级系统设置中编辑和查看）
setx API_Key=sk-你的key
```
2.创建一个虚拟环境
```python
python -m venv xfreeas
```

3.git本项目
```cmd
cd xfreeas
git clone https://github.com/CUI-hyg/CUI-X-FreeAS.git
```

4.安装依赖
```python
pip install -r requirements.txt
```
如有缺包，请根据报错pip~

5.添加.env

运行```CUI-X-FreeAS.py```,开始使用吧~

## Feature
- 1.提升GUIUse准确度<静等更强VLLM>
- 2.构建Workflow体系<✔️>
- 3.建立memory机制<✔️>
- 4.建立plugin生态<开发中>
- 5.工具直接使用plugin生态<开发中>
- 6.创建边思考边调用工具集<还未动工>
- 7.支持原生Python环境（支持safe）<还未动工>
- 8.……

## Tips
- 1.BUG:要求GUIUse单击一些按钮时会乱点、崩溃（开始菜单就是其一，自己测试一下就知道了）
- 2.欢迎大家修bug,提建议~

## Thanks
- CUI-Hyg:本人,承担主要开发,主导新架构开发
- Kimi K2:写了许多个新功能,但越来越不好用
- Qwen3-Coder:修复主要Bug，对一些不稳定的地方进行重构~

## 最后
###### 感谢你关注本项目，请点亮一下Star,谢谢~⭐
###### 祝愿本项目破100kStars~🎉🎉🎉
