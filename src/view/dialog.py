from datetime import datetime
import wx

from .base import MARGIN

from ..data.schedule import DTActiveSchedule


class ButtonDialog(wx.Dialog):
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

        # self.Center()
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
