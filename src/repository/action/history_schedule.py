from ...modules.PyCommon.src.repository.rds import ExecuteAction, FetchAction


class ActionHistorySchedule:
    @staticmethod
    def list_node(str_date: str):
        sql = """
SELECT * FROM `history_schedule`
WHERE `time_real` = %s
ORDER BY `time_node` ASC;
        """
        return FetchAction(sql, str_date)

    @staticmethod
    def insert_one(time_node: str, time_real: str):
        sql = """
INSERT INTO `history_schedule` (`time_node`, `time_real`)
VALUES (%s, %s);
        """
        return ExecuteAction(sql, time_node, time_real)
    pass
