from typing import Dict, List

from ..data.schedule import DTActiveSchedule
from ..repository.exec.schedule import ScheduleSqlite


class Schedule:
    def __init__(self, db_name: str):
        self.__exec = ScheduleSqlite(db_name)
        pass

    async def list_schedule_activate(self, str_date: str) -> Dict[str, List[DTActiveSchedule]]:
        res = {
            'active_today': [],
            'active_history': [],
        }
        async for row in self.__exec.iter_schedule_active(str_date):
            data = DTActiveSchedule.create_from_active_sqlite(row)
            if str_date > data.time_except:
                res['active_history'].append(data)
                continue
            res['active_today'].append(data)
            pass
        return res

    async def list_schedule_inactivate(self, str_date: str) -> List[DTActiveSchedule]:
        res = []
        async for row in self.__exec.iter_schedule_history(str_date):
            data = DTActiveSchedule.create_from_history_sqlite(row)
            res.append(data)
            pass
        return res

    async def review_one(self, time_node: str, time_real: str, cycle: int):
        await self.__exec.review_one(time_node, time_real, cycle)
        pass

    async def entry_time_node(self, time_node: str, time_except: str, cycle: int):
        await self.__exec.entry_time_node(time_node, time_except, cycle)
        pass

    async def table_init(self):
        await self.__exec.table_init()
        pass
    pass
