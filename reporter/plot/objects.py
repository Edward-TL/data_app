from dataclasses import dataclass

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.chart import BarChart, Reference, Series

from pathlib import PosixPath

from pandas import DataFrame

from typing import Literal

@dataclass
class Theme:
    font: str
    plot_bg: str
    paper_bg: str

@dataclass
class ColorRange:
    val: int
    color: str

@dataclass
class Scale:
    color_range: tuple[ColorRange]
    name: str = None

@dataclass
class Palette:
    light: Theme
    dark: Theme
    colors: list[str]
    scales: tuple[Scale] = None

    def __post_init__(self):
        self.categories = {f'cat_{c}': color for c, color in enumerate(self.colors)}

        for c, color in enumerate(self.colors):
            setattr(self, f"cat_{c}", color)

@dataclass
class Titles:
    chart: str = "Test CHART"
    y_axis: str = "Y AXIS Test"
    x_axis: str = "X AXIS Test"
    

@dataclass
class ChartReferences:
    """
    Remember that any CellRange value must be created with the constructor from
    openpyxl.worksheet.cell_range. With ith, you can pass the string range
    (example "A1:X29") and it will get the properties needed.

    chart_values = None means that its omited because its position is on the
                   preset value of pandas writer. Using the dataframe given in
                   the ChartData upper class, we can set the values using the
                   shape of the df.

    labels = False indicate that it's not required.
    labels = True indicate that it's required but the range is omited,
             so the __post_init__ func will create it with the df shape.
    labels = CellRange("A1:A5") is for better precision.

    table_values, first_row and first_col are assigned with the Worksheet
    data on a __post_init__ func. Don't type in there
    """
    table_sheet: str = "Hoja1"
    # chart_sheet: str = "Prueba de Grafico"

    # DO NOT TOUCH THIS UNTIL NEW VERSION OF OPENPYXL
    # IF YOU DO THIS OTHER WAY, YOU WILL HAVE THE NEXT ERROR:
    # Value must be of the form sheetname!A1:E4
    chart_position: str = None
    chart_values: CellRange = None
    labels_at_header: bool = True
    table_values: Reference = None
    series_values: str = None
    first_row: Reference = None
    first_col: Reference = None

    def __post_init__(self):
        if self.chart_position == None:
            self.chart_position = "A1"

        # So yeap, this is needed AF
        if type(self.chart_values) == str:
            self.chart_values = CellRange(self.chart_values)

def excel_reference(cell_range: CellRange, ws: Worksheet,
        first_col=False, first_row=False, adjust=True) -> Reference:
    
    """Sugar sintax just for passing a CellRange and set the
    Reference to the table.
    
    If first_col or first_row set as True, will take the dimensions
    stored at CharData.ref.chart_values and change the max_col or max_row
    to 1, depending on the case setted as True.

    If first_col or first_row remains
    False, it will use the same dimensions stored at
    ChartData.ref.chart_values.
    """
    if adjust:
        correction = 1
    else:
        correction = 0

    if first_col == True:    
        return Reference(
            worksheet = ws,
            # Same first column
            min_col = cell_range.min_col,
            max_col = cell_range.min_col,

            min_row = cell_range.min_row + correction,
            max_row = cell_range.max_row,
        )
    
    elif first_row == True:
        return Reference(
            worksheet = ws,
            # Same first column
            min_col = cell_range.min_col + correction,
            max_col = cell_range.max_col,

            min_row = cell_range.min_row,
            max_row = cell_range.min_row,
        )
    else:
        return Reference(
            worksheet = ws,
            min_col = cell_range.min_col + correction,
            max_col = cell_range.max_col,
            min_row = cell_range.min_row,
            max_row = cell_range.max_row,
        )
@dataclass
class Source:
    """Use to show the data according to the original source of data, or
    the plotted data"""
    ws: Worksheet
    df: DataFrame

@dataclass
class ChartData:
    """
    titles: stored the title values of the chart, as its x and y axis.
    wb: path and file name (ending with '.xlsx') of the workbook
    ref: Reference object that stores [table_sheet, chart_sheet, chart_values, labels]
    df: pandas.DataFrame of the data.
    palette: Palette object that stores company palette.
    """
    titles: Titles

    data: Source
    chart: Source
    ref: ChartReferences
    palette: Palette = None
    height: int | float = 7.5
    width: int | float = 15

    def __post_init__(self):
        if (self.ref.chart_values == None):
            self.ref.chart_values = CellRange(
                min_col = 1, min_row = 1,
                # Remember that Excel starts with 1 and pandas with 0
                max_row = self.data.df.shape[0] + 1,
                max_col = self.data.df.shape[1]
                )
        
        self.ref.table_values = excel_reference(
            self.ref.chart_values,
            ws = self.data.ws,
            ) 
        
        self.ref.first_row = excel_reference(
            self.ref.chart_values,
            ws = self.data.ws,
            first_row = True
            )
        
        self.ref.first_col = excel_reference(
            self.ref.chart_values,
            ws = self.data.ws,
            first_col = True
            )