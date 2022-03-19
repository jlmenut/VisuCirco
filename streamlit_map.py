import os
import geopandas as gpd
import streamlit as st
import pandas as pd
import plotly.express as px #if using plotly

st.set_page_config(layout="wide")

def save_uploaded_file(file_content, file_name):
    """
    Save the uploaded file to a temporary directory
    """
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(file_name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(file_content.getbuffer())

    return file_path

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )
    
def app():

    st.title("Circonscriptions france")

    # row1_col1, row1_col2 = st.columns([2, 1])
    # width = 950
    # height = 600
    _max_width_()

    data = st.selectbox(
        "Selectionnez une donnée à visualiser", ['Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', '% Vot/Ins', 
                                                 'Blancs', '% Blancs/Ins', '% Blancs/Vot','Nuls', '% Nuls/Ins', 
                                                 '% Nuls/Vot', 'Exprimés', '% Exp/Ins', '% Exp/Vot',], index=3
    )

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
    

    fig = px.choropleth_mapbox(merged, geojson=merged.geometry,
                    locations=merged.index, color=data,
                    hover_data=['Libellé du département', 'Code du département', 'Code de la circonscription'],
                    width=1200,
                    height=1200,
                    zoom = 5.6,
                    center={'lat':46.227638, 'lon':2.213749},
                    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
    # if st.checkbox('Montrer les données brutes'):
    #     st.subheader('Données brutes')
    #     st.write('geojson des circos')
    #     st.write(pd.DataFrame(gdf.to_wkt()))
    #     st.write('résultats des circos')
    #     st.write(leg)
    #     st.write("merge")
    #     st.write(merged.to_wkt())
    # print(gdf.dtypes, leg.dtypes)
    # lon, lat = leafmap.gdf_centroid(gdf)
    # if backend == "pydeck":

    #     column_names = ['Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', '% Vot/Ins', 'Blancs', '% Blancs/Ins',
    #                     '% Blancs/Vot', 'Nuls', '% Nuls/Ins', '% Nuls/Vot',  'Exprimés',
    #                     '% Exp/Ins', '% Exp/Vot']
    #     random_column = None
    #     with container:
    #         random_color = st.checkbox("Apply random colors", True)
    #         if random_color:
    #             random_column = st.selectbox(
    #                 "Select a column to apply random colors", column_names
    #             )

    #     m = leafmap.Map(center=(lat, lon))
    #     m.add_gdf(merged, random_color_column=random_column)
    #     st.pydeck_chart(m)

    # else:
    #     m = leafmap.Map(center=(lat, lon), draw_export=True)
    #     m.add_gdf(merged, layer_name=layer_name)
    #     # m.add_vector(file_path, layer_name=layer_name)
    #     if backend == "folium":
    #         m.zoom_to_gdf(merged)
        # m.to_streamlit()


app()