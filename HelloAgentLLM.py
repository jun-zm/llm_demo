import os
from openai import OpenAI
from typing import List, Dict


class HelloAgentsLLM:
    def __init__(self, model: str = None, apikey: str = None, baseurl: str = None, timeout: int = None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apikey or os.getenv("LLM_API_KEY")
        baseUrl = baseurl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def think(self, message: list[Dict[str, str]], temperature: float = 0):
        print(f"正在调用{self.model}模型")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=message,
                temperature=temperature,
                stream=True
            )

            print(f"大模型响应:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()
            return "".join(collected_content)

        except Exception as e:
            print(e)
            return None
