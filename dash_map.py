from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import os
import geopandas as gpd
import pandas as pd
from urllib.request import urlopen
import json
circo_path = "france-circonscriptions-legislatives-2012.geojson"
result_elect_path = "leg_circo_2017.csv"
layer_name = "Circonscriptions"
gdf = gpd.read_file(circo_path)
gdf["num_circ"] = gdf["num_circ"].apply(lambda x: int(x))
leg = pd.read_csv(result_elect_path)
leg["Code du département"] = leg["Code du département"].apply(lambda x: x.zfill(2))
merged = gdf.merge(
    leg,
    right_on=["Code du département", "Code de la circonscription"],
    left_on=["code_dpt", "num_circ"],
)


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# @app.callback(Output("graph", "figure"), Input("candidate", "value"))
# def display_choropleth():
fig = px.choropleth(
    counties,
    geojson=counties,
    locations='fips',
    scope='usa'
    # color=candidate,
    # locations="district",
    # featureidkey="properties.district",
    # projection="mercator",
    # range_color=[0, 6500],
)
# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # return fig


app = Dash(__name__)



app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

dcc.Graph(figure=fig)
])




# [dash_table.DataTable(
#     #merged.to_wkt().to_dict("records")

# )]




if __name__ == "__main__":
    app.run_server(debug=True)

