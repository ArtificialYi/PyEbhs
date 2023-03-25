class DTActiveSchedule:
    def __init__(self, id: int, time_node: str, time_except: str, cycle: int,):
        self.id = id
        self.time_node = time_node
        self.time_except = time_except
        self.cycle = cycle
        pass

    @staticmethod
    def create_from_active(row: dict):
        return DTActiveSchedule(
            row['id'], row['time_node'].strftime('%Y-%m-%d'), row['time_except'].strftime('%Y-%m-%d'), row['cycle'],
        )

    @staticmethod
    def create_from_history(row: dict):
        return DTActiveSchedule(
            row['id'], row['time_node'].strftime('%Y-%m-%d'), row['time_real'].strftime('%Y-%m-%d'), -1,
        )
    pass
