from ...modules.PyCommon.src.repository.rds import FetchAction


class ActionHistorySchedule:
    def list_node(self, str_date: str):
        sql = """
SELECT * FROM `history_schedule`
WHERE `time_real` = %s
ORDER BY `time_node` ASC;
        """
        return FetchAction(sql, str_date)
    pass
