

```
docker compose exec python-worker python start.py
```



``` mermaid
graph TD
    User((사용자))

    subgraph "Docker Compose 환경"
        UI[Temporal Web UI<br/>:8080]
        Server[Temporal Server<br/>:7233]
        DB[(PostgreSQL)]
        Worker[Python Worker]
    end

    User -->|start.py 실행| Server
    User -->|상태 확인| UI

    UI -->|API 호출| Server
    Server <-->|상태 및 큐 저장| DB
    Worker <-->|Task Queue 폴링 및 결과 보고| Server

    classDef server fill:#f9f,stroke:#333,stroke-width:2px;
    classDef db fill:#bbf,stroke:#333,stroke-width:2px;
    classDef worker fill:#dfd,stroke:#333,stroke-width:2px;
    class Server server
    class DB db
    class Worker worker
```

``` mermaid
sequenceDiagram
    autonumber
    actor U as User (start.py)
    participant S as Temporal Server
    participant DB as PostgreSQL
    participant W as Python Worker

    U->>S: Workflow 실행 요청 (인자: "파이썬 코더")
    S->>DB: Workflow 시작 이벤트 기록 저장
    S-->>S: Task Queue ('hello-task-queue')에 작업 등록

    loop 계속 반복 (Polling)
        W->>S: Task Queue에 제가 할 일 있나요?
    end

    S->>W: 작업 할당 (say_hello 액티비티 실행 지시)

    Note over W: 파이썬 코드(activities.py) 실행<br/>"안녕하세요, 파이썬 코더님!..." 생성

    W->>S: 실행 완료 및 결과 반환
    S->>DB: Workflow 완료 상태 및 결과 기록
    S->>U: 최종 결과 전달 및 종료
```