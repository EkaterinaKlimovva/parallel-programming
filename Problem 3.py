import asyncio

async def a():
    print("a start")
    await asyncio.sleep(1)
    print("a end")

async def b():
    print("b start")
    await asyncio.sleep(1)
    print("b end")

async def c():
    print("c start")
    await asyncio.sleep(4)
    print("c end")

async def d():
    print("d start")
    await asyncio.sleep(1)
    print("d end")

async def e():
    print("e start")
    await asyncio.sleep(3)
    print("e end")

async def ae():
    await a()
    await e()

async def bd():
    await b()
    await d()

async def baed():
    await asyncio.gather(*[asyncio.create_task(bd()), asyncio.create_task(ae())])


async def main() -> None:
    print("main start")
    await asyncio.gather(asyncio.create_task(baed()), asyncio.create_task(c()))
    print("main end")
    return None

if __name__ == '__main__':
    asyncio.run(main())
