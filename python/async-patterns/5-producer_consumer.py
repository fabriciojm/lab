import asyncio


async def producer(queue: asyncio.Queue[str]) -> None:
    await queue.put("job-1")
    await queue.put("job-2")
    await queue.put("job-3")


async def worker(queue: asyncio.Queue[str]) -> None:
    while True:
        job_id = await queue.get()

        try:
            print(f"worker: processing {job_id}")
            await asyncio.sleep(1)
            print(f"worker: finished {job_id}")
        finally:
            queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue()
    worker_task = asyncio.create_task(worker(queue))
    await producer(queue)
    await queue.join()
    worker_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
