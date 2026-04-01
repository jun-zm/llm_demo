from PlanAndExecutor.Executor import Executor
from PlanAndExecutor.Planner import Planner


class PlanAndSolveAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.planner = Planner(self.llm_client)
        self.executor = Executor(self.llm_client)

    def run(self, question: str):
        print(f"开始处理问题: {question}")

        # 规划器生成计划
        plan = self.planner.plan(question)

        if not plan:
            print(f"\n---任务结束---\n无法生成有效的行动计划")
            return

        final_answer = self.executor.execute(question, plan)

        print(f"\n---任务完成---\n最终答案: {final_answer}")
