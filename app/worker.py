import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker
from activities import say_hello
from workflows import GreetingWorkflow


async def connect_with_retry(temporal_address: str, namespace: str) -> Client:
    max_attempts = int(os.getenv("TEMPORAL_CONNECT_MAX_ATTEMPTS", "30"))
    retry_delay_seconds = float(os.getenv("TEMPORAL_CONNECT_RETRY_DELAY_SECONDS", "2"))

    for attempt in range(1, max_attempts + 1):
        try:
            return await Client.connect(temporal_address, namespace=namespace)
        except RuntimeError as err:
            print(
                f"Temporal 연결 실패 (시도 {attempt}/{max_attempts}): {err}. "
                f"{retry_delay_seconds}초 후 재시도합니다."
            )
            if attempt == max_attempts:
                raise
            await asyncio.sleep(retry_delay_seconds)


async def main():
    # 환경변수에서 주소를 가져오며, 기본값은 temporal:7233 입니다.
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

    # 1. Temporal 서버와 연결
    client = await connect_with_retry(temporal_address, temporal_namespace)

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
