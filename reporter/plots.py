from dataclasses import dataclass
from typing import Literal

from plot.objects import ChartData
from .plot.excel import bar, BAR_TYPES

@dataclass
class Chart:
    _data: ChartData

@dataclass
class Bar(Chart):
    _type: BAR_TYPES = 'normal'

    def __post_init__(self):
        # TO DO
        self.plotly = None

    def to_excel(self):
        return bar(self._data)
    
    def show(self):
        return self.plotly