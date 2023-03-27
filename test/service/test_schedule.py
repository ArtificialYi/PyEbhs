from ...src.modules.PyCommon.mock.db.sqlite import MockConnection, MockCursor

from ...src.modules.PyCommon.src.tool.func_tool import PytestAsyncTimeout

from ...src.service.schedule import Schedule
from pytest_mock import MockerFixture


class TestSchedule:
    @PytestAsyncTimeout(1)
    async def test_activate_schedule(self, mocker: MockerFixture):
        row0 = {
            'id': 1, 'time_node': '2020-01-01',
            'time_except': '2020-01-01', 'cycle': 1,
        }
        row1 = {
            'id': 1, 'time_node': '2020-01-02',
            'time_except': '2020-01-02', 'cycle': 1,
        }
        mock_cursor = MockCursor().mock_set_fetch_all([row0, row1])
        conn = MockConnection().mock_set_cursor(mock_cursor)
        mocker.patch('PyEbhs.src.modules.PyCommon.src.repository.sqlite.get_conn', return_value=conn)

        schedule = Schedule('test.db')
        # 常规活跃列表
        data_dict = await schedule.list_schedule_activate('2020-01-02')
        assert (
            len(data_dict['active_today']) == 1 and data_dict['active_today'][0]
            .time_node == row1['time_node']
        )
        assert (
            len(data_dict['active_history']) == 1 and data_dict['active_history'][0]
            .time_node == row0['time_node']
        )
        pass

    @PytestAsyncTimeout(1)
    async def test_inactivate_schedule(self, mocker: MockerFixture):
        row0 = {
            'id': 1, 'time_node': '2019-01-01',
            'time_real': '2020-01-01',
        }
        row1 = {
            'id': 1, 'time_node': '2019-01-02',
            'time_real': '2020-01-02',
        }
        mock_cursor = MockCursor().mock_set_fetch_all([row0, row1])
        conn = MockConnection().mock_set_cursor(mock_cursor)
        mocker.patch('PyEbhs.src.modules.PyCommon.src.repository.sqlite.get_conn', return_value=conn)
        schedule = Schedule('test.db')
        data_list = await schedule.list_schedule_inactivate('2020-01-02')
        assert len(data_list) == 2
        assert data_list[0].time_node == row0['time_node']
        pass

    @PytestAsyncTimeout(1)
    async def test_review_one(self, mocker: MockerFixture):
        mocker.patch('PyEbhs.src.modules.PyCommon.src.repository.sqlite.get_conn', new=MockConnection)
        schedule = Schedule('test.db')
        # 检查复查
        await schedule.review_one('2019-12-31', '2020-01-03', 1)

    @PytestAsyncTimeout(1)
    async def test_entry_time_node(self, mocker: MockerFixture):
        mocker.patch('PyEbhs.src.modules.PyCommon.src.repository.sqlite.get_conn', new=MockConnection)
        schedule = Schedule('test.db')
        # 检查入库
        await schedule.entry_time_node('2019-12-31', '2020-01-03', 1)
    pass
