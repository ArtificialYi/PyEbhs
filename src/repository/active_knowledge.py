from ...PyCommon.src.repository.rds import FetchAction


class ActionActiveSchedule:
    async def list_node(self, str_date: str):
        sql = """
SELECT * from `active_schedule`
WHERE `time_except` <= %s
AND `delted_date` == '9999-12-31 23:59:59'
ORDER BY `time_except` ASC
LIMIT 10;
        """
        return FetchAction(sql, str_date)
    pass


class ActionHistorySchedule:
    async def list_node(self, str_date: str):
        sql = """
SELECT * FROM `history_schedule`
WHERE `time_real` = %s
ORDER BY `time_node` ASC;
        """
        return FetchAction(sql, str_date)
    pass
