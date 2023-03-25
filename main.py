import asyncio
from concurrent.futures import Future
from contextlib import contextmanager
import threading
from src.modules.PyCommon.configuration.rds import pool_manage
from src.view.main import main_loop


# 异步线程程序入口
async def db_loop(future_pool: Future, future_stop: asyncio.Future):
    async with await pool_manage() as pool:
        future_pool.set_result(pool)
        print('数据库连接池创建成功')
        await future_stop
        pass
    pass


def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
    pass


@contextmanager
def loop_threading():
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_event_loop, args=(loop,))
    t.start()
    yield loop
    loop.call_soon_threadsafe(loop.stop)
    t.join()
    pass


@contextmanager
def pool_threading(loop: asyncio.AbstractEventLoop):
    future_pool = Future()
    future_stop = asyncio.Future(loop=loop)
    asyncio.run_coroutine_threadsafe(db_loop(future_pool, future_stop), loop)
    yield future_pool.result()
    future_stop.set_result(None)
    pass


if __name__ == '__main__':
    with (
        loop_threading() as loop,
        pool_threading(loop) as pool
    ):
        main_loop(loop, pool)
        pass
    pass
