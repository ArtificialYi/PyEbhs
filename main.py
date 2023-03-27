import asyncio
from contextlib import contextmanager
import threading
from src.view.main import main_loop


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


if __name__ == '__main__':
    with loop_threading() as loop:
        main_loop(loop)
        pass
    pass
