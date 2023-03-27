from ...modules.PyCommon.src.repository.db import ActionExec, ActionIter


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
        return ActionIter(sql, str_date)

    @staticmethod
    def insert_one(str_date: str, str_except: str, cycle: int):
        sql = """
INSERT INTO `active_schedule` (`time_node`, `time_except`, `cycle`)
VALUES (%s, %s, %s);
        """
        return ActionExec(sql, str_date, str_except, cycle)

    @staticmethod
    def update_one(time_node: str, time_except: str, cycle: int):
        sql = """
UPDATE `active_schedule` SET `time_except` = %s, `cycle` = %s
WHERE `time_node` = %s AND `deleted_date` = '9999-12-31 23:59:59'
LIMIT 2;
        """
        return ActionExec(sql, time_except, cycle, time_node)
    pass
