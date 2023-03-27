class DTActiveSchedule:
    def __init__(self, id: int, time_node: str, time_except: str, cycle: int,):
        self.id = id
        self.time_node = time_node
        self.time_except = time_except
        self.cycle = cycle
        pass

    @staticmethod
    def create_from_active_sqlite(row: dict):
        return DTActiveSchedule(
            row['id'], row['time_node'], row['time_except'], row['cycle'],
        )

    @staticmethod
    def create_from_history_sqlite(row: dict):
        return DTActiveSchedule(
            row['id'], row['time_node'], row['time_real'], -1,
        )
    pass
