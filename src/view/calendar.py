import wx
import calendar

from .base import MARGIN


class CustomDatePicker(wx.Panel):
    def __init__(self, parent, ymd_str: str):
        super(CustomDatePicker, self).__init__(parent)
        year, month, day = ymd_str.split("-")
        # 创建一个水平的布局管理器
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # 创建年、月和日的标签和选择器
        year_begin = 2019
        self.__year_choice = wx.Choice(self, choices=[str(y) for y in range(year_begin, 2200)])
        self.__year_choice.SetSelection(int(year) - year_begin)
        self.__year_choice.Bind(wx.EVT_CHOICE, self.update_days)
        hbox.Add(self.__year_choice, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)

        self.__month_choice = wx.Choice(self, choices=[f'{m:02}' for m in range(1, 13)])
        self.__month_choice.SetSelection(int(month) - 1)
        self.__month_choice.Bind(wx.EVT_CHOICE, self.update_days)
        hbox.Add(self.__month_choice, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)

        self.__day_choice = wx.Choice(self, choices=[f'{d:02}' for d in range(1, 32)])
        self.__day_choice.SetSelection(int(day) - 1)
        hbox.Add(self.__day_choice, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)

        # 设置布局
        self.SetSizer(hbox)
        self.Layout()
        pass

    def update_days(self, event):
        year = int(self.__year_choice.GetString(self.__year_choice.GetSelection()))
        month = int(self.__month_choice.GetString(self.__month_choice.GetSelection()))

        _, days_in_month = calendar.monthrange(year, month)

        idx_pre = self.__day_choice.GetSelection()
        self.__day_choice.Clear()
        self.__day_choice.AppendItems([str(d) for d in range(1, days_in_month + 1)])
        self.__day_choice.SetSelection(min(idx_pre, days_in_month - 1))
        pass

    @property
    def ymd_str(self):
        year_str = self.__year_choice.GetString(self.__year_choice.GetSelection())
        month_str = self.__month_choice.GetString(self.__month_choice.GetSelection())
        day_str = self.__day_choice.GetString(self.__day_choice.GetSelection())
        return f'{year_str}-{month_str}-{day_str}'
    pass
