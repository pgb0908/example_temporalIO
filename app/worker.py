import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker
from activities import say_hello
from workflows import GreetingWorkflow


async def main():
    # 환경변수에서 주소를 가져오며, 기본값은 temporal:7233 입니다.
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")

    # 1. Temporal 서버와 연결
    client = await Client.connect(temporal_address)

    # 2. Worker 설정 (작업 대기열 이름, 등록할 워크플로우와 액티비티 지정)
    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[GreetingWorkflow],
        activities=[say_hello],
    )

    print("Python Worker가 성공적으로 시작되었습니다! 작업을 기다리는 중...")

    # 3. Worker 실행
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())