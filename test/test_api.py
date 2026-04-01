# 测试天气 API

if __name__ == '__main__':

    import requests
    response = requests.get("https://wttr.in/Beijing?format=j1")
    print("天气API状态:", response.status_code)

    # 测试 Tavily API
    from tavily import TavilyClient
    tavily = TavilyClient(api_key="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")
    try:
        result = tavily.search("test", search_depth="basic")
        print("Tavily API 连接成功")
    except Exception as e:
        print("Tavily API 错误:", e)

    # 测试 LLM API - AIHubmix
    from openai import OpenAI
    client = OpenAI(
        api_key="sk-X87HZQWySdKAKka4AfD544C68cF14eA5BaFdF91a3c0b0aF0",
        base_url="https://aihubmix.com/v1"
    )
    try:
        response = client.chat.completions.create(
            model="coding-glm-5-free",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("LLM API 连接成功:", response.choices[0].message.content)
    except Exception as e:
        print("LLM API 错误:", e)