import os
import geopandas as gpd
import pandas as pd
import plotly.express as px #if using plotly





circo_path = 'france-circonscriptions-legislatives-2012.geojson'
result_elect_path = 'leg_circo_2017.csv'
layer_name = 'Circonscriptions'
gdf = gpd.read_file(circo_path)
gdf['num_circ'] = gdf['num_circ'].apply(lambda x: int(x))
leg = pd.read_csv(result_elect_path)
leg['Code du département'] = leg['Code du département'].apply(lambda x: x.zfill(2))
merged = gdf.merge(leg, right_on=['Code du département', 'Code de la circonscription'], left_on=['code_dpt', 'num_circ'] )

#'Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', '% Vot/Ins', 'Blancs', '% Blancs/Ins', '% Blancs/Vot',
#                            'Nuls', '% Nuls/Ins', '% Nuls/Vot', 'Exprimés', '% Exp/Ins', '% Exp/Vot',
color_source = 'Blancs'

fig = px.choropleth_mapbox(merged, geojson=merged.geometry,
                locations=merged.index, color=color_source,
                hover_data=['Libellé du département', 'Code du département', 'Code de la circonscription'],

                zoom = 5.6,
                center={'lat':46.227638, 'lon':2.213749},
                )
fig.update_layout(mapbox_style="open-street-map")

fig.show()
