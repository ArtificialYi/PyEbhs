from datetime import datetime, timedelta
import wx

from .base import MARGIN

from ..data.schedule import DTActiveSchedule


class ReviewDialog(wx.Dialog):
    def __init__(self, parent, data: DTActiveSchedule):
        super().__init__(parent, title=data.time_node)
        self.__panel = wx.Panel(self)
        box_all = wx.BoxSizer(wx.VERTICAL)
        self.__panel.SetSizer(box_all)

        # 回顾时间
        review_tips = wx.StaticText(self.__panel, label="回顾时间：")
        self.__review_input = wx.TextCtrl(self.__panel, value=datetime.now().strftime("%Y-%m-%d"))
        box_date = wx.BoxSizer(wx.HORIZONTAL)
        box_date.Add(review_tips, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_date.Add(self.__review_input, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_date, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)

        # 回顾周期
        cycle_tips = wx.StaticText(self.__panel, label="下个周期：")
        self.__cycle = wx.TextCtrl(self.__panel, value=str(data.cycle * 2))
        box_cycle = wx.BoxSizer(wx.HORIZONTAL)
        box_cycle.Add(cycle_tips, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_cycle.Add(self.__cycle, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_cycle, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)

        # 确认和取消按钮
        ok_button = wx.Button(self.__panel, wx.ID_OK, "确认")
        cancel_button = wx.Button(self.__panel, wx.ID_CANCEL, "取消")
        box_button = wx.BoxSizer(wx.HORIZONTAL)
        box_button.Add(ok_button, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_button.Add(cancel_button, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_button, 0, wx.EXPAND | wx.ALL, MARGIN)

        # 渲染
        self.__panel.Layout()
        self.__panel.Fit()
        self.Fit()
        pass

    @property
    def review_date(self):
        return self.__review_input.GetValue()

    @property
    def cycle(self):
        return int(self.__cycle.GetValue())
    pass


class EntryDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="录入时间节点")
        self.__panel = wx.Panel(self)
        box_all = wx.BoxSizer(wx.VERTICAL)
        self.__panel.SetSizer(box_all)

        # 获取今日日期
        date_toay = datetime.now()
        str_today = date_toay.strftime("%Y-%m-%d")
        # 获取明日日期
        date_tomorrow = date_toay + timedelta(days=1)
        str_tomorrow = date_tomorrow.strftime("%Y-%m-%d")

        # 时间节点
        time_node_tips = wx.StaticText(self.__panel, label="时间节点：")
        self.__time_node_input = wx.TextCtrl(self.__panel, value=str_today)
        box_time_node = wx.BoxSizer(wx.HORIZONTAL)
        box_time_node.Add(time_node_tips, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_time_node.Add(self.__time_node_input, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_time_node, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)

        # 期望时间
        time_expect_tips = wx.StaticText(self.__panel, label="期望时间：")
        self.__time_expect_input = wx.TextCtrl(self.__panel, value=str_tomorrow)
        box_time_expect = wx.BoxSizer(wx.HORIZONTAL)
        box_time_expect.Add(time_expect_tips, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_time_expect.Add(self.__time_expect_input, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_time_expect, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)

        # 初始周期
        cycle_tips = wx.StaticText(self.__panel, label="初始周期：")
        self.__cycle_input = wx.TextCtrl(self.__panel, value="1")
        box_cycle = wx.BoxSizer(wx.HORIZONTAL)
        box_cycle.Add(cycle_tips, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_cycle.Add(self.__cycle_input, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_cycle, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)

        # 确认和取消按钮
        ok_button = wx.Button(self.__panel, wx.ID_OK, "确认")
        cancel_button = wx.Button(self.__panel, wx.ID_CANCEL, "取消")
        box_button = wx.BoxSizer(wx.HORIZONTAL)
        box_button.Add(ok_button, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_button.Add(cancel_button, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_button, 0, wx.EXPAND | wx.ALL, MARGIN)

        # 渲染
        self.__panel.Layout()
        self.__panel.Fit()
        self.Fit()
        pass

    @property
    def time_node(self):
        return self.__time_node_input.GetValue()

    @property
    def time_expect(self):
        return self.__time_expect_input.GetValue()

    @property
    def cycle(self):
        return int(self.__cycle_input.GetValue())
    pass


class DeleteDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="删除时间节点")
        self.__panel = wx.Panel(self)
        box_all = wx.BoxSizer(wx.VERTICAL)
        self.__panel.SetSizer(box_all)

        # 时间节点
        time_node_tips = wx.StaticText(self.__panel, label="时间节点：")
        self.__time_node_input = wx.TextCtrl(self.__panel, value=datetime.now().strftime("%Y-%m-%d"))
        box_time_node = wx.BoxSizer(wx.HORIZONTAL)
        box_time_node.Add(time_node_tips, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_time_node.Add(self.__time_node_input, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_time_node, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)

        # 确认和取消按钮
        ok_button = wx.Button(self.__panel, wx.ID_OK, "确认")
        cancel_button = wx.Button(self.__panel, wx.ID_CANCEL, "取消")
        box_button = wx.BoxSizer(wx.HORIZONTAL)
        box_button.Add(ok_button, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_button.Add(cancel_button, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        box_all.Add(box_button, 0, wx.EXPAND | wx.ALL, MARGIN)

        # 渲染
        self.__panel.Layout()
        self.__panel.Fit()
        self.Fit()
        pass

    @property
    def time_node(self):
        return self.__time_node_input.GetValue()
    pass
