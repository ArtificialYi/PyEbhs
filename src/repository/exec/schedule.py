import aiomysql

from ..action.history_schedule import ActionHistorySchedule

from ..action.active_schedule import ActionActiveSchedule

from ....PyCommon.src.repository.rds import DBExecutorSafe


class ExecSchedule:
    def __init__(self, pool: aiomysql.Pool):
        self.__exec_direct = DBExecutorSafe(pool)
        # self.__exec_trans = DBExecutorSafe(pool, True)
        pass

    async def iter_schedule_active(self, str_date: str):
        async with self.__exec_direct:
            # 获取活跃时间
            async for row in self.__exec_direct.iter_opt(ActionActiveSchedule().list_node(str_date)):
                yield row
                pass
            pass
        pass

    async def iter_schedule_history(self, str_date: str):
        async with self.__exec_direct:
            # 获取历史时间
            async for row in self.__exec_direct.iter_opt(ActionHistorySchedule().list_node(str_date)):
                yield row
                pass
            pass
        pass

    # async def list_schedule(self, str_date: str):
    #     res = {
    #         'active_today': [],
    #         'active_history': [],
    #         'history': [],
    #     }
    #     async for row in self.iter_schedule_active(str_date):
    #         if str_date > row['time_except']:
    #             res['active_history'].append(row)
    #             continue
    #         res['active_today'].append(row)
    #         pass
    #     pass
    pass
