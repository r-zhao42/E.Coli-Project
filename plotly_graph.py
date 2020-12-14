"""
This python file generates the graph for past and projected E.coli data in the UK.
"""

import yourmomssklearn
import plotly.graph_objects as go
import pandas as pd

df = yourmomssklearn.get_total_data(2010, 2030)
df2 = pd.read_excel('totals.xlsx')
NAME_ = 'UK E.coli Projection Until 2100'

df['years'] = df['years'].map("{}-01-01".format)

fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=df['years'], y=df['ecoli'],
                         name="Projected E.coli data",
                         mode='lines + markers',
                         marker=dict(
                             size=10,
                             color=df['ecoli'],
                             showscale=True),
                         ))


fig.add_trace(go.Scatter(x=df2['x'], y=df2['y'],
                         name='Past E.coli data',
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
