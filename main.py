import asyncio

from .src.view.main import async_main


if __name__ == '__main__':
    # 异步主程序入口
    asyncio.run(async_main())
    pass
