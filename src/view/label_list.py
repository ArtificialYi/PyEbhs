from typing import Callable, Dict, List, Tuple, Type

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
        self.__items: Dict[str, wx.Window] = dict()
        pass

    def __view_idx(self, view: wx.Window):
        for idx, item in enumerate(self.GetChildren()):
            if item.GetWindow() == view:
                return idx
            pass
        return -1

    def __retain_item(self, keys: set):
        for key in set(self.__items.keys()):
            if key not in keys:
                self.Remove(self.__view_idx(self.__items[key]))
                self.__items[key].Destroy()
                del self.__items[key]
            pass
        pass

    def recombine(self, data_sorted: List[Tuple[str, Type[wx.Window], List, Dict]]):
        self.__retain_item({key for key, _, _, _ in data_sorted})
        for idx, (key, view_type, args, kwargs) in enumerate(data_sorted, 1):
            if key in self.__items.keys():
                continue
            self.__items[key] = view_type(*args, **kwargs)
            self.Insert(idx, self.__items[key], 0, wx.ALIGN_CENTER | wx.ALL, MARGIN)
            pass
        pass
    pass


class ListLabelButton(ListView):
    def __init__(self, parent: wx.Panel, title: str, button_callback: Callable):
        super().__init__(parent, title)
        self.__parent = parent
        self.__callback = button_callback
        pass

    def refresh(self, data_sorted: List[DTActiveSchedule]):
        # 列表重组
        self.recombine([
            (data.time_node, LabelButton, [self.__parent, data, self.__callback], dict())
            for data in data_sorted
        ])
        pass
    pass


class ListLabel(ListView):
    def __init__(self, parent: wx.Panel, title: str):
        super().__init__(parent, title)
        self.__parent = parent
        pass

    def refresh(self, data_sorted: List[DTActiveSchedule]):
        # 列表重组
        self.recombine([
            (data.time_node, wx.StaticText, [self.__parent], {'label': data.time_node})
            for data in data_sorted
        ])
        pass
    pass
