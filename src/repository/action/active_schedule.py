from ....PyCommon.src.repository.rds import ExecuteAction, FetchAction


class ActionActiveSchedule:
    def list_node(self, str_date: str):
        sql = """
SELECT * from `active_schedule`
WHERE `time_except` <= %s
AND `delted_date` == '9999-12-31 23:59:59'
ORDER BY `time_node` ASC
LIMIT 10;
        """
        return FetchAction(sql, str_date)

    def entry_time_node(self, str_date: str, str_except: str, cycle: int):
        sql = """
INPUT INTO `active_schedule` (`time_node`, `time_except`, `cycle`)
VALUES (%s, %s, %s);
        """
        return ExecuteAction(sql, str_date, str_except, cycle)
    pass
