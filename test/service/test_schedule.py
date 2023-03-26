from datetime import datetime

from ...src.modules.PyCommon.src.tool.func_tool import PytestAsyncTimeout
from ...src.modules.PyCommon.mock.rds import MockConnection, MockCursor, MockDBPool
from ...src.repository.exec.schedule import ExecSchedule
from ...src.service.schedule import Schedule


class TestSchedule:
    @PytestAsyncTimeout(1)
    async def test_activate_schedule(self):
        row0 = {
            'id': 1, 'time_node': datetime.strptime('2020-01-01', '%Y-%m-%d'),
            'time_except': datetime.strptime('2020-01-01', '%Y-%m-%d'), 'cycle': 1,
        }
        row1 = {
            'id': 1, 'time_node': datetime.strptime('2020-01-02', '%Y-%m-%d'),
            'time_except': datetime.strptime('2020-01-02', '%Y-%m-%d'), 'cycle': 1,
        }
        mock_cursor = MockCursor().mock_set_fetch_all([row0, row1])
        schedule = Schedule(ExecSchedule(MockDBPool('test').mock_set_conn(MockConnection().mock_set_cursor(mock_cursor))))
        # 常规活跃列表
        data_dict = await schedule.list_schedule_activate('2020-01-02')
        assert (
            len(data_dict['active_today']) == 1 and data_dict['active_today'][0]
            .time_node == row1['time_node'].strftime('%Y-%m-%d')
        )
        assert (
            len(data_dict['active_history']) == 1 and data_dict['active_history'][0]
            .time_node == row0['time_node'].strftime('%Y-%m-%d')
        )
        pass

    @PytestAsyncTimeout(1)
    async def test_inactivate_schedule(self):
        row0 = {
            'id': 1, 'time_node': datetime.strptime('2019-01-01', '%Y-%m-%d'),
            'time_real': datetime.strptime('2020-01-01', '%Y-%m-%d'),
        }
        row1 = {
            'id': 1, 'time_node': datetime.strptime('2019-01-02', '%Y-%m-%d'),
            'time_real': datetime.strptime('2020-01-02', '%Y-%m-%d'),
        }
        mock_cursor = MockCursor().mock_set_fetch_all([row0, row1])
        schedule = Schedule(ExecSchedule(MockDBPool('test').mock_set_conn(MockConnection().mock_set_cursor(mock_cursor))))
        data_list = await schedule.list_schedule_inactivate('2020-01-02')
        assert len(data_list) == 2
        assert data_list[0].time_node == row0['time_node'].strftime('%Y-%m-%d')
        pass
    pass
