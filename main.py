import asyncio

from .src.view.main import main

from .PyCommon.src.tool.base import AsyncBase

from .PyCommon.configuration.rds import DBPool


async def async_main():
    # 异步主程序入口
    loop = asyncio.get_event_loop()
    async with DBPool() as pool:
        return await AsyncBase.func2coro_exec(main, loop, pool)
