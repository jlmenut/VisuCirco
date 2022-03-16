import os
import geopandas as gpd
import streamlit as st
import pandas as pd

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


def app():

    st.title("Circonscriptions france")

    # row1_col1, row1_col2 = st.columns([2, 1])
    # width = 950
    # height = 600


    backend = st.selectbox(
        "Select a plotting backend", ["folium", "kepler.gl", "pydeck"], index=2
    )

    if backend == "folium":
        import leafmap.foliumap as leafmap
    elif backend == "kepler.gl":
        import leafmap.kepler as leafmap
    elif backend == "pydeck":
        import leafmap.deck as leafmap

    # url = st.text_input(
    #     "Enter a URL to a vector dataset",
    #     "https://github.com/giswqs/streamlit-geospatial/raw/master/data/us_states.geojson",
    # )

    # data = st.file_uploader(
    #     "Upload a vector dataset", type=["geojson", "kml", "zip", "tab"]
    # )

    data = None
    container = st.container()

    circo_path = 'france-circonscriptions-legislatives-2012.geojson'
    result_elect_path = 'leg_circo_2017.csv'
    layer_name = 'Circonscriptions'
    gdf = gpd.read_file(circo_path)
    gdf['num_circ'] = gdf['num_circ'].apply(lambda x: int(x))
    leg = pd.read_csv(result_elect_path)
    leg['Code du département'] = leg['Code du département'].apply(lambda x: x.zfill(2))
    merged = gdf.merge(leg, right_on=['Code du département', 'Code de la circonscription'], left_on=['code_dpt', 'num_circ'] )
    if st.checkbox('Montrer les données brutes'):
        st.subheader('Données brutes')
        st.write('geojson des circos')
        st.write(pd.DataFrame(gdf.to_wkt()))
        st.write('résultats des circos')
        st.write(leg)
        st.write("merge")
        st.write(merged.to_wkt())
    print(gdf.dtypes, leg.dtypes)
    lon, lat = leafmap.gdf_centroid(gdf)
    if backend == "pydeck":

        column_names = ['Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', '% Vot/Ins', 'Blancs', '% Blancs/Ins',
                        '% Blancs/Vot', 'Nuls', '% Nuls/Ins', '% Nuls/Vot',  'Exprimés',
                        '% Exp/Ins', '% Exp/Vot']
        random_column = None
        with container:
            random_color = st.checkbox("Apply random colors", True)
            if random_color:
                random_column = st.selectbox(
                    "Select a column to apply random colors", column_names
                )

        m = leafmap.Map(center=(lat, lon))
        m.add_gdf(merged, random_color_column=random_column)
        st.pydeck_chart(m)

    else:
        m = leafmap.Map(center=(lat, lon), draw_export=True)
        m.add_gdf(merged, layer_name=layer_name)
        # m.add_vector(file_path, layer_name=layer_name)
        if backend == "folium":
            m.zoom_to_gdf(merged)
        m.to_streamlit()


app()