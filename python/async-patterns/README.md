# Async patterns and coroutines to be used in development with FastAPI

The two patterns to keep in mind:

```python
import asyncio
from contextlib import asynccontextmanager
import FastAPI


async def worker_loop(self) -> None:
    while True:
        job_id = await self.queue.get()
        try:
            await self.process_job(job_id)
        finally:
            self.queue.task_done()
```

and

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    worker_task = asyncio.create_task(job_service.worker_loop())
    try:
        yield
    finally:
        worker_task.cancel()
```
