import asyncio
import os
from temporalio.client import Client
from workflows import GreetingWorkflow


async def main():
    # 로컬호스트(외부)에서 접속하므로 localhost:7233 을 사용합니다.
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    client = await Client.connect(temporal_address)

    # 워크플로우 실행 요청
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "파이썬 코더",  # 워크플로우에 넘길 인자 (name)
        id="hello-workflow-1",  # 고유 ID 지정 (동일한 ID로 동시에 실행 불가)
        task_queue="hello-task-queue",
    )

    print(f"\n🎉 Workflow 실행 결과: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())