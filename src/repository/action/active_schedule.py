

from ...modules.PyCommon.src.repository.rds import ExecuteAction, FetchAction


class ActionActiveSchedule:
    @staticmethod
    def list_node(str_date: str):
        sql = """
SELECT * from `active_schedule`
WHERE `time_except` <= %s
AND `deleted_date` = '9999-12-31 23:59:59'
ORDER BY `time_node` ASC
LIMIT 10;
        """
        return FetchAction(sql, str_date)

    @staticmethod
    def entry_time_node(str_date: str, str_except: str, cycle: int):
        sql = """
INPUT INTO `active_schedule` (`time_node`, `time_except`, `cycle`)
VALUES (%s, %s, %s);
        """
        return ExecuteAction(sql, str_date, str_except, cycle)

    @staticmethod
    def update_one(time_node: str, time_except: str, cycle: int):
        sql = """
UPDATE `active_schedule` SET `time_except` = %s, `cycle` = %s
WHERE `time_node` = %s AND `deleted_date` = '9999-12-31 23:59:59'
LIMIT 2;
        """
        return ExecuteAction(sql, time_except, cycle, time_node)
    pass
