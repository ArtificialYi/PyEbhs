from datetime import datetime, timedelta
import aiomysql

from ...data.schedule import DTActiveSchedule

from ...modules.PyCommon.src.repository.rds import DBExecutorSafe

from ..action.history_schedule import ActionHistorySchedule

from ..action.active_schedule import ActionActiveSchedule


class ExecSchedule:
    def __init__(self, pool: aiomysql.Pool):
        self.__exec_direct = DBExecutorSafe(pool)
        self.__exec_trans = DBExecutorSafe(pool, True)
        pass

    async def iter_schedule_active(self, str_date: str):
        async with self.__exec_direct:
            # 获取活跃时间
            async for row in self.__exec_direct.iter_opt(ActionActiveSchedule.list_node(str_date)):
                yield DTActiveSchedule.create_from_active(row)
                pass
            pass
        pass

    async def iter_schedule_history(self, str_date: str):
        async with self.__exec_direct:
            # 获取历史时间
            async for row in self.__exec_direct.iter_opt(ActionHistorySchedule.list_node(str_date)):
                yield DTActiveSchedule.create_from_history(row)
                pass
            pass
        pass

    async def entry_time_node(self, str_date: str, str_except: str, cycle: int):
        async with self.__exec_trans:
            # 入库活跃时间
            return await self.__exec_direct.execute(ActionActiveSchedule.entry_time_node(str_date, str_except, cycle))

    async def review_one(self, time_node: str, time_real: str, cycle: int):
        date_real = datetime.strptime(time_real, '%Y-%m-%d')
        date_except = date_real + timedelta(days=cycle)
        time_except = date_except.strftime('%Y-%m-%d')
        async with self.__exec_trans:
            # 更新活跃时间
            await self.__exec_trans.execute(ActionActiveSchedule.update_one(time_node, time_except, cycle))
            # 入库历史时间
            await self.__exec_trans.execute(ActionHistorySchedule.insert_one(time_node, time_real))
            pass
    pass
