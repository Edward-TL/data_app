# from modules.palette import palette
# Check for the palette object
from plotly import graph_objects as go
from typing import Literal
import pandas as pd

from dataclasses import dataclass
from typing import List, Literal, Tuple
from pandas import DataFrame as PandasDataFrame


@dataclass
class Plot:
    df: PandasDataFrame
    name: str
    x_axis: str
    y_axis: str
    cat: int  = 0
    fig_row_pos: int = 0
    fig_col_pos: int = 0
    x_title: str = ""
    y_title: str = ""
    


@dataclass
class LinePlot(Plot):
    def __post_init__(self):
        if self.x_title == "": self.x_title = self.x_axis
        if self.y_title == "": self.y_title = self.y_axis
        self.graph = go.Scatter(
            x = self.df[self.x_axis],
            y = self.df[self.y_axis],
            mode = "lines",
            name = self.name,
            line = {"color": palette[f'cat_{self.cat}']},
            showlegend = False,
#             stackgroup = 'one'
        )

        self.color = palette[f'cat_{self.cat}']

    def show(self):
        fig_display(self)

def fig_display(plot: Plot, dimensions: Literal[1, 2, 3] = 2):
    fig = go.Figure().add_trace(plot.graph)
    
    if dimensions == 2:
        fig.update_layout(
            title = plot.name,
            xaxis_title = plot.x_title,
            yaxis_title = plot.y_title
        )
    elif dimensions == 1:
        fig.update_layout(
            hoverinfo = 'label+percent',
            textinfo = 'value',
            marker = dict(colors = plot.color_cats)
        )
    else:
        pass
    fig.show()

# Test object

# GrafBajas = LinePlot(
#     df = bajas_dia,
#     name = "Bajas por dia",
#     x_axis= bajas_dia.columns[0],
#     y_axis= bajas_dia.columns[1],
# )


def fig_layout(fig, theme, titles, type: str = None) -> None:
    fig.update_layout(
        plot_bgcolor = palette[f'{theme}_plot_bg'],
        paper_bgcolor = palette[f'{theme}_paper_bg'],
        font = {'color': palette[f'{theme}_font']},
        title = titles['plot'],
        xaxis_title = titles['x'],
        yaxis_title = titles['y']
    )

    if type == 'bar_group':
        fig.update_layout(barmode = 'group')

def bars(
    data: pd.DataFrame , x: str, y: str, titles: dict,
    category_col: str = None,
    theme: str = 'light',
    orientation: str = 'vertical'
    ) -> go.Figure:

    """Returns a BAR Plotly Graph with the colors of the institution.
    If category_col it's passed, will return a line plot with the
    lines according to the unique values of that category.
    """

    # Creates the plot
    # Just ONE group
    if category_col == None:
        bar_fig = go.Figure(
            data = go.Bar(
                x = data[x],
                y = data[y],
                marker_color = palette['cat_0'],
                text = data[y],
                textposition='auto'
            )
        )

    
    # Multiple lines
    else:
        bar_fig = go.Figure(
            data = [
                    go.Scatter(
                        x = data[[category_col] == category][x],
                        y = data[[category_col] == category][y],
                        marker_color = palette[f'cat_{c}'],
                        name = category,
                        text = data[[category_col] == category][y],
                        textposition='auto'
                ) for c, category in enumerate(tuple(data[category_col].unique())) 
            ]
        )
        
    fig_layout(bar_fig, theme=theme, titles=titles)

    return bar_fig


# GrafBajas.show()