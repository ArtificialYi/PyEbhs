from datetime import datetime, timedelta
from typing import Dict, List

from ..data.schedule import DTActiveSchedule
from ..repository.exec.schedule import ScheduleSqlite


class Schedule:
    def __init__(self, db_name: str):
        self.__exec = ScheduleSqlite(db_name)
        pass

    async def table_init(self):
        await self.__exec.table_init()
        pass

    def __group_active(self, data: DTActiveSchedule, str_today: str):
        if data.time_except > str_today:
            return 'active_tomorrow'
        if data.time_except == str_today:
            return 'active_today'
        return 'active_history'

    async def list_schedule_activate(self, str_today: str) -> Dict[str, List[DTActiveSchedule]]:
        res = {
            'active_tomorrow': [],
            'active_today': [],
            'active_history': [],
        }
        date_tomorrow = datetime.strptime(str_today, '%Y-%m-%d') + timedelta(days=1)
        str_tomorrow = date_tomorrow.strftime('%Y-%m-%d')
        async for row in self.__exec.iter_schedule_active(str_tomorrow):
            data = DTActiveSchedule.create_from_active_sqlite(row)
            res[self.__group_active(data, str_today)].append(data)
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
        print('录入时间节点: ', time_node, time_except, cycle)
        pass

    async def delete_time_node(self, time_node: str):
        await self.__exec.delete_time_node(time_node)
        print('删除时间节点: ', time_node)
        pass
    pass
