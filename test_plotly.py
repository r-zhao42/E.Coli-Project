import plotly.graph_objects as go
import pandas as pd

df = pd.read_excel('proj1_UK_popu.xlsx')
# df2 = pd.read_csv('Monthly E.Coli 2012-2020.csv')
name = 'UK'

import numpy as np

print(df)

fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=df['x'], y=df['y'],
                         mode='lines + markers',
                         marker=dict(
                             size=10,
                             color=df['y'],  # set color equal to a variable
                             showscale=True)))

fig.update_layout(title={
    'text': name,
    'y': 0.9,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'},
    font=dict(family="Helvetica", size=18),
    barmode='stack',
    legend=dict(x=0.4, y=-0.3),
    legend_orientation="h")


fig.show()

