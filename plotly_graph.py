import sklearn
import yourmomssklearn
import misc1
import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = yourmomssklearn.get_total_data(2010, 2030)
df2 = pd.read_excel('totals.xlsx')
name = 'UK E.coli vs. Temperature'

df['years'] = df['years'].map(lambda year: "{}-01-01".format(year))

print(df)
print(df2)

fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=df['years'], y=df['ecoli'],
                         name="Past E.coli data",
                         mode='lines + markers',
                         marker=dict(
                             size=10,
                             color=df['ecoli'],
                             showscale=True),
                         ))



fig.add_trace(go.Scatter(x=df2['x'], y=df2['y'],
                         name='Projected E.coli data',
                         mode='lines + markers'))
                        #  marker=dict(
                        #      size=10,
                        #      color=df2['y'],  # set color equal to a variable
                        #      showscale=True)))

fig.update_layout(title={
    'text': name,
    'y': 0.9,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'},
    font=dict(family="Helvetica", size=18),
    barmode='stack',
    legend_orientation="h",

)


fig.show()
