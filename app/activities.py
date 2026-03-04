from temporalio import activity

@activity.defn
async def say_hello(name: str) -> str:
    return f"안녕하세요, {name}님! Temporal의 세계에 오신 것을 환영합니다."