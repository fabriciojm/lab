import asyncio


async def say_hello() -> None:
    print("hello")
    await asyncio.sleep(1)
    print("done")


async def main() -> None:
    await say_hello()


if __name__ == "__main__":
    asyncio.run(main())
