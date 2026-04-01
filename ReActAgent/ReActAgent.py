import re

from dotenv import load_dotenv

from toolExecutor import ToolExecutor
from HelloAgentLLM import HelloAgentsLLM
from search_tavily import search

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""


def _parse_output(text: str):
    thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
    action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)

    thought = thought_match.group(1).strip() if thought_match else None
    action = action_match.group(1).strip() if action_match else None
    return thought, action


def _parse_action(action_text: str):
    match = re.search(r"(\w+)\[(.*)]", action_text, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return None, None


class ReActAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.history = []
        self.max_steps = max_steps

    def run(self, question: str):
        self.history = []
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"---Current step: {current_step}---")

            tools_list = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)

            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_list,
                question=question,
                history=history_str
            )

            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages)
            if not response_text:
                print(f"error:llm无响应")
                break

            thought, action = _parse_output(response_text)
            if thought:
                print(f"思考:{thought}")

            if not action:
                print("未能解析出有效action,流程终止")
                break

            if action.startswith("Finish"):
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"最终答案:{final_answer}")
                return final_answer

            tool_name, tool_input = _parse_action(action)
            if not tool_name or not tool_input:
                continue

            print(f"行动:{tool_name}[{tool_input}]")

            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                observation = f"error:未找到{tool_name}工具"
            else:
                observation = tool_function(tool_input)

            print(f"观察:{observation}")
            self.history.append(f"Action:{action}")
            self.history.append(f"Observation:{observation}")

        print("已达最大步数,流程终止")
        return None