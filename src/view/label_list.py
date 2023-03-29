from typing import Callable, Dict, List

from .base import MARGIN
from ..data.schedule import DTActiveSchedule
import wx


class LabelButton(wx.Button):
    def __init__(self, parent: wx.Panel, data: DTActiveSchedule, button_callback: Callable):
        super().__init__(parent, label=data.time_node)
        self.Bind(wx.EVT_BUTTON, button_callback)
        self.__dc = wx.ClientDC(self)
        text_width, text_height = self.__dc.GetTextExtent(data.time_node)
        self.SetMinClientSize((text_width + 10, text_height))
        self.__data = data
        pass

    @property
    def data(self):
        return self.__data
    pass


class ListView(wx.BoxSizer):
    def __init__(self, parent: wx.Panel, title: str):
        super().__init__(wx.VERTICAL)
        self.__title = wx.StaticText(parent, label=title)
        self.Add(self.__title, 0, wx.ALIGN_LEFT | wx.ALL, MARGIN)
        self.__items = dict()
        pass

    def view_idx(self, view):
        for idx, item in enumerate(self.GetChildren()):
            if item.GetWindow() == view:
                return idx
            pass
        return -1

    def add_item(self, key: str, view):
        self.__items[key] = view
        self.Add(view, 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
        pass
    pass


class ListLabelButton(ListView):
    def __init__(self, parent: wx.Panel, title: str, data_sorted: List[DTActiveSchedule], button_callback: Callable):
        super().__init__(parent, title)
        self.__parent = parent
        self.__items: Dict[str, LabelButton] = dict()
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
        # 移除不在列表中的控件
        self.__remove_window([
            data.time_node
            for data in data_sorted
        ])

        # 添加新的控件
        keys = self.__items.keys()
        for idx, data in enumerate(data_sorted, 1):
            key = data.time_node
            if key in keys:
                continue
            self.__items[key] = LabelButton(self.__parent, data, self.__callback)
            self.Insert(idx, self.__items[key], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass

    def __remove_window(self, key_available: List[str]):
        keys = set(self.__items.keys())
        for key in keys:
            if key not in key_available:
                self.Remove(self.__button_idx(self.__items[key]))
                self.__items[key].Destroy()
                del self.__items[key]
                pass
            pass
        pass
    pass


class ListLabel(ListView):
    def __init__(self, parent: wx.Panel, title: str, str_sorted: List[DTActiveSchedule]):
        super().__init__(parent, title)
        self.__parent = parent
        self.__items: Dict[str, wx.StaticText] = dict()
        self.refresh(str_sorted)
        pass

    def __button_idx(self, button: wx.StaticText):
        for idx, item in enumerate(self.GetChildren()):
            if item.GetWindow() == button:
                return idx
            pass
        return -1

    def refresh(self, data_sorted: List[DTActiveSchedule]):
        # 移除不在列表中的控件
        self.__remove_window([
            data.time_node
            for data in data_sorted
        ])

        # 添加新的控件
        keys = self.__items.keys()
        for idx, data in enumerate(data_sorted, 1):
            if data.time_node in keys:
                continue
            self.__items[data.time_node] = wx.StaticText(self.__parent, label=data.time_node)
            self.Insert(idx, self.__items[data.time_node], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass

    def __remove_window(self, key_available: List[str]):
        keys = set(self.__items.keys())
        for key in keys:
            if key not in key_available:
                idx = self.__button_idx(self.__items[key])
                self.Remove(idx)
                print('移除：', key, idx)
                self.__items[key].Destroy()
                del self.__items[key]
                pass
            pass
        pass
    pass
