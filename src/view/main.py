import asyncio
from concurrent.futures import Future
from datetime import datetime
from typing import Callable, Coroutine, Dict, List
import aiomysql
import wx

from ..data.schedule import DTActiveSchedule

from ..repository.exec.schedule import ExecSchedule

from ..service.schedule import Schedule


MARGIN = 2


class LabelButton(wx.Button):
    def __init__(self, parent: wx.Panel, data: DTActiveSchedule, button_callback: Callable):
        super().__init__(parent, label=data.time_node)
        self.Bind(wx.EVT_BUTTON, button_callback)
        self.__dc = wx.ClientDC(self)
        text_width, text_height = self.__dc.GetTextExtent(data.time_node)
        self.SetMinClientSize((text_width + 10, text_height))
        self.__data = data
        pass
    pass


class ListLabelButton(wx.BoxSizer):
    def __init__(self, parent: wx.Panel, title: str, data_sorted: List[DTActiveSchedule], button_callback: Callable):
        super().__init__(wx.VERTICAL)
        self.__parent = parent
        self.__title = wx.StaticText(parent, label=title)
        self.Add(self.__title, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)
        self.__items = dict()
        self.__callback = button_callback
        for data in data_sorted:
            self.__items[data.time_node] = LabelButton(parent, data, self.__callback)
            self.Add(self.__items[data.time_node], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass

    def __button_idx(self, button: LabelButton):
        for idx, item in enumerate(self.GetChildren()):
            if item.GetWindow() == button:
                return idx
            pass
        return -1

    def refresh(self, data_sorted: List[DTActiveSchedule]):
        keys = [
            data.time_node
            for data in data_sorted
        ]
        # 移除不在列表中的控件
        [
            self.Remove(self.__button_idx(self.__items[key]))
            for key in self.__items.keys()
            if key not in keys
        ]

        # 添加新的控件
        keys = self.__items.keys()
        for idx, data in enumerate(data_sorted, 1):
            key = data.time_node
            if key in keys:
                continue
            self.__items[key] = LabelButton(self.__parent, data, self.__callback)
            self.Insert(idx, self.__items[key], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        # self.Layout()
        pass
    pass


class ListLabel(wx.BoxSizer):
    def __init__(self, parent: wx.Panel, title: str, str_sorted: List[DTActiveSchedule]):
        super().__init__(wx.VERTICAL)
        self.__parent = parent
        self.__title = wx.StaticText(parent, label=title)
        self.Add(self.__title, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)
        self.__items = dict()
        self.refresh(str_sorted)
        pass

    def __button_idx(self, button: wx.StaticText):
        for idx, item in enumerate(self.GetChildren()):
            if item.GetWindow() == button:
                return idx
            pass
        return -1

    def refresh(self, data_sorted: List[DTActiveSchedule]):
        keys = [
            data.time_node
            for data in data_sorted
        ]
        # 移除不在列表中的控件
        [
            self.Remove(self.__button_idx(self.__items[key]))
            for key in self.__items.keys()
            if key not in keys
        ]

        # 添加新的控件
        keys = self.__items.keys()
        for idx, str_label in enumerate(data_sorted, 1):
            if str_label in keys:
                continue
            self.__items[str_label] = wx.StaticText(self.__parent, label=str_label)
            self.Insert(idx, self.__items[str_label], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        # self.Layout()
        pass
    pass


class MyFrame(wx.Frame):
    def __init__(self, title, loop: asyncio.AbstractEventLoop, service: Schedule):
        super().__init__(None, title=title)
        self.__loop = loop
        self.__service = service

        self.__panel = wx.Panel(self)
        self.__view = wx.BoxSizer(wx.VERTICAL)
        self.__panel.SetSizer(self.__view)

        self.__opt = wx.BoxSizer(wx.HORIZONTAL)
        self.__view.Add(self.__opt, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__opt.Add(
            LabelButton(self.__panel, DTActiveSchedule(-1, "回顾", '', -1), self.on_button_click),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )
        self.__opt.Add(
            LabelButton(self.__panel, DTActiveSchedule(-1, "录入", '', -1), self.on_button_click),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )
        self.__opt.Add(
            LabelButton(self.__panel, DTActiveSchedule(-1, "删除", '', -1), self.on_button_click),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )
        self.__opt.Add(
            LabelButton(self.__panel, DTActiveSchedule(-1, "刷新", '', -1), self.on_button_click),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )

        self.__data = wx.BoxSizer(wx.HORIZONTAL)
        self.__view.Add(self.__data, 1, wx.EXPAND | wx.ALL, MARGIN)
        self.__history_active = ListLabelButton(self.__panel, "历史未回顾", [], self.on_button_click)
        self.__data.Add(self.__history_active, 1, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__today_active = ListLabelButton(self.__panel, "今日未回顾", [], self.on_button_click)
        self.__data.Add(self.__today_active, 1, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.__history_inactive = ListLabel(self.__panel, "已回顾", [])
        self.__data.Add(self.__history_inactive, 1, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        self.refresh()
        pass

    async def __get_data(self):
        today = datetime.now().strftime("%Y-%m-%d")
        dict_sorted = await self.__service.list_schedule_activate(today)
        history_inactive = await self.__service.list_schedule_inactivate(today)
        dict_sorted["inactive_history"] = history_inactive
        return dict_sorted

    def __data_show(self, future: Future):
        dict_data_sorted: Dict[str, List[DTActiveSchedule]] = future.result()
        self.__history_active.refresh(dict_data_sorted["active_history"])
        self.__today_active.refresh(dict_data_sorted["active_today"])
        self.__history_inactive.refresh(dict_data_sorted["inactive_history"])
        self.__panel.Layout()
        self.Fit()
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


def main_loop(loop: asyncio.AbstractEventLoop, pool: aiomysql.Pool):
    app = wx.App()
    frame = MyFrame("艾宾浩斯记忆法", loop, Schedule(ExecSchedule(pool)))
    frame.Show()
    app.MainLoop()
    pass
