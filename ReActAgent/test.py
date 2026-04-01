from ReActAgent import *
from search_tavily import search

if __name__ == "__main__":
    load_dotenv()  # 加载环境变量
    llm = HelloAgentsLLM()
    tool_executor = ToolExecutor()

    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_description, search)

    reactAgentTest = ReActAgent(llm_client=llm, tool_executor=tool_executor)

    question = "华为最新手机型号以及主要卖点"

    reactAgentTest.run(question)