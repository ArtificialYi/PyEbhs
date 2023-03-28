from datetime import datetime, timedelta
from typing import AsyncGenerator

from ...modules.PyCommon.src.repository.sqlite import SqliteManage

from ..action.history_schedule import ActionHistorySchedule

from ..action.active_schedule import ActionActiveSchedule
from ...modules.PyCommon.src.repository.db import SqlManage


class ScheduleSqlOne:
    """对单库的SQL操作
    """
    def __init__(self, manage: SqlManage):
        self.__manage = manage
        pass

    async def iter_schedule_active(self, str_date: str) -> AsyncGenerator[dict, None]:
        async with self.__manage() as conn:
            # 获取活跃时间
            async for row in conn.iter(ActionActiveSchedule.list_node(str_date)):
                yield row
                pass
            pass
        pass

    async def iter_schedule_history(self, str_date: str) -> AsyncGenerator[dict, None]:
        async with self.__manage() as conn:
            # 获取历史时间
            async for row in conn.iter(ActionHistorySchedule.list_node(str_date)):
                yield row
                pass
            pass
        pass

    async def entry_time_node(self, str_date: str, str_except: str, cycle: int):
        async with self.__manage(True) as conn:
            # 入库活跃时间
            return await conn.exec(ActionActiveSchedule.insert_one(str_date, str_except, cycle))

    async def review_one(self, time_node: str, time_real: str, cycle: int):
        date_real = datetime.strptime(time_real, '%Y-%m-%d')
        date_except = date_real + timedelta(days=cycle)
        time_except = date_except.strftime('%Y-%m-%d')
        async with self.__manage(True) as conn:
            # 更新活跃时间
            await conn.exec(ActionActiveSchedule.update_one(time_node, time_except, cycle))
            # 入库历史时间
            await conn.exec(ActionHistorySchedule.insert_one(time_node, time_real))
            pass
        pass

    async def table_init(self):
        async with self.__manage(True) as conn:
            await conn.exec(ActionActiveSchedule.create_table())
            await conn.exec(ActionActiveSchedule.create_index())
            await conn.exec(ActionHistorySchedule.create())
            pass
        pass
    pass


class ScheduleSqlite(ScheduleSqlOne):
    """对Sqlite的SQL操作
    """
    def __init__(self, path: str):
        super().__init__(SqliteManage(path))
        pass
    pass
