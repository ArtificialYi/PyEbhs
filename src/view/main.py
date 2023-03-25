import asyncio
from concurrent.futures import Future
from typing import Callable, Coroutine, Dict, List
import aiomysql
import wx

from ..repository.exec.schedule import ExecSchedule

from ..service.schedule import Schedule


MARGIN = 2


class LabelButton(wx.Button):
    def __init__(self, parent: wx.Panel, label: str, button_callback: Callable):
        super().__init__(parent, label=label)
        self.Bind(wx.EVT_BUTTON, button_callback)
        self.__dc = wx.ClientDC(self)
        text_width, text_height = self.__dc.GetTextExtent(label)
        self.SetMinClientSize((text_width + 10, text_height))
        pass
    pass


class ListLabelButton(wx.BoxSizer):
    def __init__(self, parent: wx.Panel, title: str, str_sorted: List[str], button_callback: Callable):
        super().__init__(wx.VERTICAL)
        self.__parent = parent
        self.__title = wx.StaticText(parent, label=title)
        self.Add(self.__title, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)
        self.__items = dict()
        self.__callback = button_callback
        for str_label in str_sorted:
            self.__items[str_label] = LabelButton(parent, str_label, self.__callback)
            self.Add(self.__items[str_label], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass

    def refresh(self, str_sorted: List[str]):
        # 移除不在列表中的控件
        [
            self.Remove(self.__items[key])
            for key in self.__items.keys()
            if key not in str_sorted
        ]

        # 添加新的控件
        keys = self.__items.keys()
        for idx, str_label in enumerate(str_sorted, 1):
            if str_label in keys:
                continue
            self.__items[str_label] = LabelButton(self.__parent, str_label, self.__callback)
            self.Insert(idx, self.__items[str_label], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass
    pass


class ListLabel(wx.BoxSizer):
    def __init__(self, parent: wx.Panel, title: str, str_sorted: List[str]):
        super().__init__(wx.VERTICAL)
        self.__parent = parent
        self.__title = wx.StaticText(parent, label=title)
        self.Add(self.__title, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)
        self.__items = dict()
        for str_label in str_sorted:
            self.__items[str_label] = wx.StaticText(parent, label=str_label)
            self.Add(self.__items[str_label], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass

    def refresh(self, str_sorted: List[str]):
        # 移除不在列表中的控件
        [
            self.Remove(self.__items[key])
            for key in self.__items.keys()
            if key not in str_sorted
        ]

        # 添加新的控件
        keys = self.__items.keys()
        for idx, str_label in enumerate(str_sorted, 1):
            if str_label in keys:
                continue
            self.__items[str_label] = wx.StaticText(self.__parent, label=str_label)
            self.Insert(idx, self.__items[str_label], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass
    pass


class MyFrame(wx.Frame):
    def __init__(self, title, loop: asyncio.AbstractEventLoop, service: Schedule):
        super().__init__(None, title=title)
        self.__loop = loop
        self.__service = service

        panel = wx.Panel(self)
        self.__view = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(self.__view)

        self.__opt = wx.BoxSizer(wx.HORIZONTAL)
        self.__view.Add(self.__opt, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__opt.Add(LabelButton(panel, "回顾", self.on_button_click), 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__opt.Add(LabelButton(panel, "录入", self.on_button_click), 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__opt.Add(LabelButton(panel, "删除", self.on_button_click), 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__opt.Add(LabelButton(panel, "刷新", self.on_button_click), 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)

        self.__data = wx.BoxSizer(wx.HORIZONTAL)
        self.__view.Add(self.__data, 1, wx.EXPAND | wx.ALL, MARGIN)
        self.__history_active = ListLabelButton(panel, "历史未回顾", ["1", "2", "3"], self.on_button_click)
        self.__data.Add(self.__history_active, 1, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__today_active = ListLabelButton(panel, "今日未回顾", ["1", "2", "3"], self.on_button_click)
        self.__data.Add(self.__today_active, 1, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__history_inactive = ListLabel(panel, "已回顾", ["1", "2", "3"])
        self.__data.Add(self.__history_inactive, 1, wx.ALIGN_CENTER | wx.ALL, MARGIN)

        panel.Fit()
        self.Fit()
        pass

    async def __get_data(self):
        dict_sorted = await self.__service.list_schedule_activate('')
        history_inactive = await self.__service.list_schedule_inactivate('')
        dict_sorted["history_inactive"] = history_inactive
        return dict_sorted

    def __data_show(self, future: Future):
        dict_sorted: Dict[str, List[str]] = future.result()
        self.__history_active.refresh(dict_sorted["history_active"])
        self.__today_active.refresh(dict_sorted["today_active"])
        self.__history_inactive.refresh(dict_sorted["history_inactive"])
        pass

    def async2sync(self, coro: Coroutine, callback: Callable):
        future = asyncio.run_coroutine_threadsafe(coro, self.__loop)
        future.add_done_callback(callback)
        pass

    def refresh(self):
        # 刷新数据
        wx.CallAfter(self.async2sync, self.__get_data(), self.__data_show)
        pass

    def on_button_click(self, event):
        wx.MessageBox("按钮已点击！", "表单事件", wx.OK | wx.ICON_INFORMATION)
        pass
    pass


def main(loop: asyncio.AbstractEventLoop, pool: aiomysql.Pool):
    app = wx.App()
    frame = MyFrame("艾宾浩斯记忆法", loop, Schedule(ExecSchedule(pool)))
    frame.Show()
    app.MainLoop()
    pass
