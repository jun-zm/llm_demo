from dotenv import load_dotenv

from ReActAgent.search_tavily import search
from ReActAgent.toolExecutor import ToolExecutor

load_dotenv()

# if __name__ == "__main__":
#     try:
#         llmClient = HelloAgentsLLM()
#
#         exampleMessage = [
#             {"role": "system", "content": "You are a helpful assistant that writes Python code."},
#             {"role": "user", "content": "写一个快速排序算法"}
#         ]
#
#         print("调用llm")
#         responseText = llmClient.think(exampleMessage)
#         if responseText:
#             print("\n\n---响应")
#             print(responseText)
#
#     except ValueError as e:
#         print(e)

# --- 工具初始化与使用示例 ---
if __name__ == '__main__':
    # 1. 初始化工具执行器
    toolExecutor = ToolExecutor()

    # 2. 注册我们的实战搜索工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)

    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    # 4. 智能体的Action调用，这次我们问一个实时性的问题
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")
