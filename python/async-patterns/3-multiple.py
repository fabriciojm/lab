import asyncio


async def process_job(job_id: int) -> str:
    print(f"job {job_id}: start")
    await asyncio.sleep(2)
    print(f"job {job_id}: done")
    return f"result-{job_id}"


async def main() -> None:
    task1 = asyncio.create_task(process_job(1))
    task2 = asyncio.create_task(process_job(2))
    task3 = asyncio.create_task(process_job(3))

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1, result2, result3)


if __name__ == "__main__":
    asyncio.run(main())
