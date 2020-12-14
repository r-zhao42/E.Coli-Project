import plotly.graph_objects as go
import pandas as pd
import yourmomssklearn

end = 2100

total = yourmomssklearn.get_percentage_increase_all_stations(end)

mapbox_access_token = 'pk.eyJ1Ijoiam9qb29udGhhdCIsImEiOiJja2lta3UzbnowYWRtMzVud3NrNjI3N2JjIn0.kYIFPU3HJbjDsNYyQFaGdA'
df = pd.read_csv(
    'jo.csv')
site_lat = df.lat
site_lon = df.lon
locations_name = df.text.tolist()

for i in range(len(locations_name)):
    location = locations_name[i]
    locations_name[i] = "{}: Projected to have {:.4f}% of increase until {}".format(location.title(), total[location], end)

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    lat=site_lat,
    lon=site_lon,
    name='Weather station',
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=20,
        color='rgb(255, 218, 200)',  # percentage
        opacity=0.75
    ),
    text=locations_name,
    hoverinfo='text',
    hoverlabel=dict(
        bgcolor='rgb(255, 217, 255)',
        font_size=40,
        font_family="Helvetica"
    )
))

fig.add_trace(go.Scattermapbox(
    lat=site_lat,
    lon=site_lon,
    name='',
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=14,
        color='rgb(211, 237, 255)',  # percentage
        opacity=0.75
    ),
    text=locations_name,
    hoverinfo='text',
    hoverlabel=dict(
        bgcolor='rgb(182, 252, 213)',
        font_size=40,
        font_family="Helvetica"
    )
))

fig.add_trace(go.Scattermapbox(
    lat=site_lat,
    lon=site_lon,
    name='',
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=7,
        color='rgb(182, 252, 213)',  # percentage
        opacity=0.8
    ),
    text=locations_name,
    hoverinfo='text',
    hoverlabel=dict(
        bgcolor='rgb(182, 252, 213)',
        font_size=14,
        font_family="Helvetica"
    )
))

fig.update_layout(
    title={
        'text': 'Number of E.coli Cases in all Weather Stations in the UK',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    autosize=True,
    hovermode='closest',
    font=dict(family="Helvetica", size=18),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=52,
            lon=0.12
        ),
        pitch=10,
        zoom=3,
        style='dark'
    )
)

fig.update_traces(showlegend=True, selector=dict(type='scattermapbox'))

fig.show()
