from ...modules.PyCommon.src.repository.db import ActionExec, ActionIter


class ActionHistorySchedule:
    @staticmethod
    def create():
        return ActionExec("""
CREATE TABLE IF NOT EXISTS `history_schedule` (
     `id` INTEGER NOT NULL ON CONFLICT FAIL PRIMARY KEY AUTOINCREMENT,
     `time_node` text NOT NULL ON CONFLICT FAIL COLLATE BINARY,
     `time_real` text NOT NULL ON CONFLICT FAIL COLLATE BINARY,
    CONSTRAINT `uniq_cur` UNIQUE (time_real COLLATE BINARY DESC, time_node COLLATE BINARY ASC) ON CONFLICT FAIL
);
        """)

    @staticmethod
    def list_node(str_date: str):
        sql = """
SELECT * FROM `history_schedule`
WHERE `time_real` = %s
ORDER BY `time_node` ASC;
        """
        return ActionIter(sql, str_date)

    @staticmethod
    def insert_one(time_node: str, time_real: str):
        sql = """
INSERT INTO `history_schedule` (`time_node`, `time_real`)
VALUES (%s, %s);
        """
        return ActionExec(sql, time_node, time_real)
    pass
