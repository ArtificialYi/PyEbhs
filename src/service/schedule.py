from typing import Dict, List

from ..data.schedule import DTActiveSchedule
from ..repository.exec.schedule import ExecSchedule


class Schedule:
    def __init__(self, exec_schedule: ExecSchedule):
        self.__exec_schedule = exec_schedule
        pass

    async def list_schedule_activate(self, str_date: str) -> Dict[str, List[DTActiveSchedule]]:
        res = {
            'active_today': [],
            'active_history': [],
        }
        async for data in self.__exec_schedule.iter_schedule_active(str_date):
            if str_date > data.time_except:
                res['active_history'].append(data)
                continue
            res['active_today'].append(data)
            pass
        return res

    async def list_schedule_inactivate(self, str_date: str) -> List[DTActiveSchedule]:
        res = []
        async for data in self.__exec_schedule.iter_schedule_history(str_date):
            res.append(data)
            pass
        return res

    async def review_one(self, time_node: str, time_real: str, cycle: int):
        await self.__exec_schedule.review_one(time_node, time_real, cycle)

    async def entry_time_node(self, time_node: str, time_except: str, cycle: int):
        await self.__exec_schedule.entry_time_node(time_node, time_except, cycle)
    pass
