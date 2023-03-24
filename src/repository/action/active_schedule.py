from ....PyCommon.src.repository.rds import FetchAction


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
    pass
