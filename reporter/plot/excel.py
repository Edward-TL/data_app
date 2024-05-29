
from dataclasses import dataclass
from openpyxl.chart import BarChart, BarChart3D, Reference
from typing import Literal

# HAND-MADE
from objects import ChartData

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
    values = Reference(
        Chart.ws,
        min_col = Chart.ref.chart_values.min_col,
        max_col = Chart.ref.chart_values.max_col,
        min_row = Chart.ref.chart_values.min_row,
        max_row = Chart.ref.chart_values.max_row,
        )
    
    chart.add_data(values)

    # Labels part
    if Chart.ref.x_axis_labels != False:
        cats = Reference(
            Chart.ws,
            # Same first column
            min_col = Chart.ref.x_axis_labels.min_col,
            max_col = Chart.ref.x_axis_labels.min_col,
            min_row = Chart.ref.x_axis_labels.min_row,
            max_row = Chart.ref.x_axis_labels.max_row,
            )
        
        chart.set_categories(cats)

    Chart.ws.add_chart(chart, Chart.ref.chart_position)

    Chart.wb.save(Chart.file_path)

