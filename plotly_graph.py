"""
This python file generates the graph for past and projected E.Coli data in the UK.
"""

import projection
import plotly.graph_objects as go
import pandas as pd


def plot_graph(end_year: int) -> None:
    """
    This plots the total UK E.Coli infection cases over time, past and future.
    It shows the relationship by the line of linear regression, which consequently also
    projects future E.Coli Cases.


    """
    df = projection.get_total_data(2010, end_year)
    df2 = pd.read_excel('past_ecoli_totals.xlsx')
    NAME_ = 'UK E.coli Projection Until {}'.format(end_year)
    df['years'] = df['years'].map("{}-01-01".format)

    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(x=df['years'], y=df['ecoli'],
                            name="Projected E.Coli data",
                            mode='lines + markers',
                            marker=dict(
                                size=10,
                                color=df['ecoli'],
                                showscale=True),
                            ))


    fig.add_trace(go.Scatter(x=df2['x'], y=df2['y'],
                            name='Past E.Coli data',
                            mode='lines + markers'))


    fig.update_layout(title={'text': NAME_,
                            'y': 0.9,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                    font=dict(family="Helvetica", size=18),
                    barmode='stack',
                    legend_orientation="h")

    fig.show()


def plot_individual(name: str, history: pd.DataFrame, projection: pd.DataFrame) -> None:
    """
        Plots the individual graph for individual weather stations. Each weather station has a name which
        you enter in the name argument. History is derived from the E.Coli sorting file and the projection
        is derived from the sklearn modelling file.
        """
    projection['years'] = projection['years'].map("{}-01-01".format)
    projection['ecoli'] = projection['ecoli'].map(lambda value: value[0])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=projection['years'], y=projection['ecoli'],
                             name="Projected E.Coli data",
                             mode='lines + markers',
                             marker=dict(
                                 size=10,
                                 color=projection['ecoli'],
                                 showscale=True),
                             ))

    fig.add_trace(go.Scatter(x=history['x'], y=history['y'],
                             name='Past E.Coli data',
                             mode='lines + markers'))

    fig.update_layout(title={
        'text': name,
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(family="Helvetica", size=18),
        barmode='stack',
        legend_orientation="h")

    fig.show()
