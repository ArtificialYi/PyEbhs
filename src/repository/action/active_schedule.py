from ...modules.PyCommon.src.repository.db import ActionExec, ActionIter


class ActionActiveSchedule:
    @staticmethod
    def create_table():
        return ActionExec("""
CREATE TABLE IF NOT EXISTS `active_schedule` (
     `id` integer NOT NULL ON CONFLICT FAIL PRIMARY KEY AUTOINCREMENT,
     `time_node` TEXT(10,0) NOT NULL ON CONFLICT FAIL COLLATE BINARY,
     `time_except` TEXT(10,0) NOT NULL ON CONFLICT FAIL COLLATE BINARY,
     `cycle` integer NOT NULL ON CONFLICT FAIL,
     `deleted_date` TEXT(19,0) NOT NULL ON CONFLICT FAIL DEFAULT '9999-12-31 23:59:59' COLLATE BINARY,
    CONSTRAINT `idx_node` UNIQUE (`time_node` COLLATE BINARY ASC, `deleted_date` COLLATE BINARY DESC) ON CONFLICT FAIL
);
        """)

    @staticmethod
    def create_index():
        return ActionExec("""
CREATE INDEX IF NOT EXISTS `idx_cur` ON `active_schedule` (
    `deleted_date` COLLATE BINARY DESC, `time_except` COLLATE BINARY ASC
);
        """)

    @staticmethod
    def list_node(str_date: str):
        sql = """
SELECT * from `active_schedule`
WHERE `time_except` <= %s
AND `deleted_date` = '9999-12-31 23:59:59'
ORDER BY `time_node` ASC
LIMIT 30;
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
WHERE `id` IN (
    SELECT `id` FROM `active_schedule`
    WHERE `time_node` = %s AND `deleted_date` = '9999-12-31 23:59:59'
    LIMIT 2
);
        """
        return ActionExec(sql, time_except, cycle, time_node)

    @staticmethod
    def delete_one(time_node: str, deleted_datetime: str):
        sql = """
UPDATE `active_schedule` SET `deleted_date` = %s
WHERE `id` IN (
    SELECT `id` FROM `active_schedule`
    WHERE `time_node` = %s AND `deleted_date` = '9999-12-31 23:59:59'
    LIMIT 2
);"""
        return ActionExec(sql, deleted_datetime, time_node)
    pass
