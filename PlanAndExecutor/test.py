from dotenv import load_dotenv

from PlanAndSolveAgent import PlanAndSolveAgent
from HelloAgentLLM import *


if __name__ == '__main__':
    load_dotenv()
    # 底层大模型
    llm_client_demo = HelloAgentsLLM()

    pasa_demo = PlanAndSolveAgent(llm_client_demo)

    question_str = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
    pasa_demo.run(question_str)

