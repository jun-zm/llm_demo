
from tavily import TavilyClient
import os


def search(query: str) -> str:
    """
    一个基于Tavily的实战网页搜索引擎工具。
    Tavily 专为AI Agent设计，对中文搜索支持很好。
    """
    print(f"🔍 正在执行 [Tavily] 网页搜索: {query}")
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "错误:TAVILY_API_KEY 未在 .env 文件中配置。"

        client = TavilyClient(api_key=api_key)

        # 使用 Tavily 搜索，获取简洁回答
        response = client.search(
            query=query,
            search_depth="basic",
            include_answer=True,
            include_raw_content=False,
            max_results=3
        )

        print(f"[调试] Tavily 返回的键: {list(response.keys())}")

        # 优先使用 Tavily 生成的答案
        if "answer" in response and response["answer"]:
            return response["answer"]

        # 如果没有答案，则使用搜索结果
        if "results" in response and response["results"]:
            snippets = [
                f"[{i + 1}] {res.get('title', '')}\n{res.get('content', '')}"
                for i, res in enumerate(response["results"][:3])
            ]
            return "\n\n".join(snippets)

        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"
