from serpapi import SerpApiClient
import os


def search(query: str) -> str:
    """
    一个基于SerpApi的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    """
    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误:SERPAPI_API_KEY 未在 .env 文件中配置。"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",  # 国家代码
            "hl": "zh-cn",  # 语言代码,
            "google_domain": "google.com"
        }

        client = SerpApiClient(params)
        results = client.get_dict()

        # 调试：打印返回的所有键
        print(f"[调试] SerpApi 返回的键: {list(results.keys())}")

        # 检查是否有错误
        if "error" in results:
            return f"SerpApi 错误: {results['error']}"

        # 智能解析:优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results:
            if "answer" in results["answer_box"]:
                return results["answer_box"]["answer"]
            if "snippet" in results["answer_box"]:
                return results["answer_box"]["snippet"]
        if "knowledge_graph" in results:
            kg = results["knowledge_graph"]
            if "description" in kg:
                return kg["description"]
            if "title" in kg:
                return f"{kg.get('title', '')}: {kg.get('type', '')}"
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i + 1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)

        # 如果什么都没找到，打印一些调试信息
        print(f"[调试] 无法解析结果，可用的键: {list(results.keys())}")
        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"
