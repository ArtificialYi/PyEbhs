from ..repository.exec.schedule import ExecSchedule


class Schedule:
    def __init__(self, exec_schedule: ExecSchedule):
        self.__exec_schedule = exec_schedule
        pass

    async def list_schedule_activate(self, str_date: str):
        res = {
            'active_today': [],
            'active_history': [],
        }
        async for row in self.__exec_schedule.iter_schedule_active(str_date):
            if str_date > row['time_except']:
                res['active_history'].append(row)
                continue
            res['active_today'].append(row)
            pass
        return res

    async def list_schedule_history(self, str_date: str):
        res = []
        async for row in self.__exec_schedule.iter_schedule_history(str_date):
            res.append(row)
            pass
        return res
    pass
