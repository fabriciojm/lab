import asyncio


async def background_work() -> None:
    print("background: start")
    await asyncio.sleep(2)
    print("background: done")


async def main() -> None:
    task = asyncio.create_task(background_work())

    print("main: I can keep going")
    await asyncio.sleep(1)
    print("main: still working")

    await task


if __name__ == "__main__":
    asyncio.run(main())
