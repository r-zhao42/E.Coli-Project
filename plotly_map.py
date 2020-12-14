"""
Plots a map showing the weather stations in the UK and their projected
increase percentage in E.Coli cases.
"""
import plotly.graph_objects as go
import pandas as pd
import projection
# Copyright: Hayk Nazaryan, Ryan Zhao, Joanne Pan, Cliff Zhang


def plot_map(end_year: int) -> None:
    """
    Plots a map showing the weather stations in the UK and their projected
    increase percentage in E.Coli cases.
    """
    total = projection.get_percentage_increase(end_year)
    temps = projection.temp_prediction_all(end_year)
    print(temps)

    mapbox_access_token = 'pk.eyJ1Ijoiam9qb29udGhhdCIsImEiOiJja2lta3Uzbnow' \
                          'YWRtMzVud3NrNjI3N2JjIn0.kYIFPU3HJbjDsNYyQFaGdA'
    df = pd.read_csv(
        'plotly_map_station_locations.csv')
    site_lat = df.lat
    site_lon = df.lon
    locations_name = df.text.tolist()

    temp_values = temps['temp'].tolist()
    max_temp = max(temp_values)
    min_temp = min(temp_values)
    temp_diff = max_temp - min_temp
    location_colors = []

    for i in range(len(locations_name)):
        location = locations_name[i]
        locations_name[i] = "{}: Projected to have {:.4f}% of increase until {}".format(
            location.title(), total[location], end_year)
        temp_value = temps.loc[temps['location'] == location]['temp'][0][0]
        ratio = (temp_value - min_temp) / temp_diff
        gb_value = 255 - int(ratio * 255)
        rgb = 'rgb(255, {}, {})'.format(gb_value, gb_value)
        location_colors.append(rgb)


    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        name='Weather Station Temperature',
        mode='markers',
        marker=dict(
            size=20,
            color=location_colors,
            colorscale=[[0, "rgb(255, 255, 255)"],
                        [1, "rgb(255, 0, 0)"]],
            showscale=False,
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
            size=0,
            color=temps['temp'],
            colorscale=[[0, "rgb(255, 255, 255)"],
                        [1, "rgb(255, 0, 0)"]],
            showscale=True,
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
            'text': 'Percentage of Increase in E.Coli Cases for Weather Stations in the UK',
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

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.00,
        xanchor="right",
        x=1.00
    ))

    fig.show()
