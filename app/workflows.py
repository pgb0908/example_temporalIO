from datetime import timedelta
from temporalio import workflow

# 액티비티 임포트
with workflow.unsafe.imports_passed_through():
    from activities import say_hello

@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        # 액티비티를 실행하고, 최대 10초를 기다립니다.
        return await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )