import asyncio
from concurrent.futures import Future
from datetime import datetime
from typing import Callable, Coroutine, Dict, List
import aiomysql
import wx

from .dialog import EntryDialog, ReviewDialog

from .label_list import LabelButton, ListLabel, ListLabelButton
from .base import MARGIN
from ..data.schedule import DTActiveSchedule
from ..repository.exec.schedule import ExecSchedule
from ..service.schedule import Schedule


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
            LabelButton(self.__panel, DTActiveSchedule(-1, "回顾", '', -1), self.on_default),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )
        self.__opt.Add(
            LabelButton(self.__panel, DTActiveSchedule(-1, "录入", '', -1), self.on_entry_click),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )
        self.__opt.Add(
            LabelButton(self.__panel, DTActiveSchedule(-1, "删除", '', -1), self.on_default),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )
        self.__opt.Add(
            LabelButton(self.__panel, DTActiveSchedule(-1, "刷新", '', -1), self.refresh),
            0, wx.ALIGN_CENTER | wx.ALL, MARGIN,
        )

        self.__data = wx.BoxSizer(wx.HORIZONTAL)
        self.__view.Add(self.__data, 1, wx.EXPAND | wx.ALL, MARGIN)
        self.__history_active = ListLabelButton(self.__panel, "历史未回顾", [], self.on_review_one_click)
        self.__data.Add(self.__history_active, 1, wx.ALIGN_TOP | wx.ALL, MARGIN)
        self.__today_active = ListLabelButton(self.__panel, "今日未回顾", [], self.on_review_one_click)
        self.__data.Add(self.__today_active, 1, wx.ALIGN_TOP | wx.ALL, MARGIN)
        self.__history_inactive = ListLabel(self.__panel, "已回顾", [])
        self.__data.Add(self.__history_inactive, 1, wx.ALIGN_TOP | wx.ALL, MARGIN)
        self.refresh()
        pass

    def on_default(self, event: wx.CommandEvent):
        wx.MessageDialog(self, "功能尚未完成").ShowWindowModal()
        pass

    def refresh(self, event=None):
        # 刷新数据
        self.__coro_and_callback(self.__get_data(), self.__data_show)
        pass

    def __coro_and_callback(self, coro: Coroutine, callback: Callable):
        future = asyncio.run_coroutine_threadsafe(coro, self.__loop)
        future.add_done_callback(callback)
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
        wx.CallAfter(self.__review_main)
        pass

    def __review_main(self):
        self.__panel.Layout()
        self.__panel.Fit()
        self.Fit()
        self.__panel.Refresh()
        pass

    def on_review_one_click(self, event: wx.CommandEvent):
        button = event.GetEventObject()
        dialog = ReviewDialog(self.__panel, button.data)
        dialog.CenterOnParent()
        res = dialog.ShowModal()
        if res != wx.ID_OK:
            return
        # 执行回顾事件 + 刷新界面
        self.__coro_and_callback(
            self.__service.review_one(button.data.time_node, dialog.review_date, dialog.cycle),
            self.refresh,
        )
        return

    def on_entry_click(self, event: wx.CommandEvent):
        dialog = EntryDialog(self.__panel)
        dialog.CenterOnParent()
        res = dialog.ShowModal()
        if res != wx.ID_OK:
            return
        # 执行录入事件 + 刷新界面
        self.__coro_and_callback(
            self.__service.entry_time_node(dialog.time_node, dialog.time_expect, dialog.cycle),
            self.refresh,
        )
        pass
    pass


def main_loop(loop: asyncio.AbstractEventLoop, pool: aiomysql.Pool):
    app = wx.App()
    frame = MyFrame("艾宾浩斯记忆法", loop, Schedule(ExecSchedule(pool)))
    frame.Show()
    app.MainLoop()
    pass
