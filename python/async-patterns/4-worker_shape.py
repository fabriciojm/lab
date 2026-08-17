import asyncio


async def worker() -> None:
    try:
        while True:
            print("worker: waiting")
            await asyncio.sleep(1)
            print("worker: tick")
    except asyncio.CancelledError:
        print("worker: cancelled")
        raise


async def main() -> None:
    worker_task = asyncio.create_task(worker())
    await asyncio.sleep(3)
    worker_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
