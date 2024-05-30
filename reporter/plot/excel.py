
from openpyxl.chart import BarChart, BarChart3D
from typing import Literal

from openpyxl.worksheet.cell_range import CellRange
# HAND-MADE
from .objects import ChartData, excel_reference

# @dataclass
# class BarTypes:
#     normal = 10
#     horizontal = 11
#     stacked_vertical = 12
#     stacked_horizontal = 13

BAR_TYPES = Literal['normal', 'horizontal', 'stacked_vertical', 'stacked_horizonal', '3D']

def set_barchart(type):
    if type == '3D':
        return BarChart3D()
    chart = BarChart()
    type_style = {
        'normal': 10,
        'horizontal' : 11,
        'stacked_vertical': 12,
        'stacked_horizonal': 13
    }
    # Setting type and style
    if type.endswith('horizontal'):
        chart.type = 'bar'

        if type.startswith('stacked'):
            chart.grouping = 'percentStacked'
            chart.overlap = 100

    else:
        chart.type = 'col'

        if type.startswith('stacked'):
            chart.grouping = 'stacked'
            chart.overlap = 100

    chart.style = type_style[type]

    return chart
    
def bar(Chart: ChartData, bar_type: BAR_TYPES):
    
    chart = set_barchart(bar_type)
    # Basic Data
    chart.title = Chart.titles.chart
    chart.y_axis.title = Chart.titles.y_axis
    chart.x_axis.title = Chart.titles.x_axis

    # Data part
    # All table case
    if Chart.ref.series_values == None:
        chart.add_data(
            Chart.ref.table_values,
            titles_from_data = Chart.ref.labels_at_header
        )
    # Just one column from the table 
    else:
        chart.add_data(
                excel_reference(
                cell_range = CellRange(
                    range_string = Chart.ref.series_values
                    ),
                ws = Chart.data.ws,
                adjust= False
            ),
            titles_from_data = Chart.ref.labels_at_header
        )
    # Labels part
    chart.set_categories(
        Chart.ref.first_col
    )

    chart.height = Chart.height
    chart.width = Chart.width

    Chart.chart.ws.add_chart(chart, Chart.ref.chart_position)

