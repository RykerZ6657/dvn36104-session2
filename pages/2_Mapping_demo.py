from pathlib import Path
import pandas as pd
import pydeck as pdk
import streamlit as st
st.title('Mapping demo')
st.write('Tutorial data for bike rental racks and Bay Area Rapid Transit stops and flows.')
DATA=Path(__file__).resolve().parents[1]
@st.cache_data
def load_file(filename):return pd.read_json(DATA/filename)
bikes=load_file('bike_rental_stats.json');stops=load_file('bart_stop_stats.json');flows=load_file('bart_path_stats.json')
specs={
 'Bike rentals':pdk.Layer('HexagonLayer',bikes,get_position=['lon','lat'],radius=200,elevation_scale=4,elevation_range=[0,1000],extruded=True),
 'BART stop exits':pdk.Layer('ScatterplotLayer',stops,get_position=['lon','lat'],get_color=[200,30,0,160],get_radius='exits',radius_scale=.05,pickable=True),
 'BART stop names':pdk.Layer('TextLayer',stops,get_position=['lon','lat'],get_text='name',get_color=[0,0,0,200],get_size=15),
 'Outbound flow':pdk.Layer('ArcLayer',flows,get_source_position=['lon','lat'],get_target_position=['lon2','lat2'],get_source_color=[200,30,0,160],get_target_color=[200,30,0,160],get_width='outbound',width_scale=.0001,width_min_pixels=3,width_max_pixels=30),
}
st.sidebar.subheader('Map layers')
layers=[layer for label,layer in specs.items() if st.sidebar.checkbox(label,True,key=label)]
if layers:
    st.pydeck_chart(pdk.Deck(map_style='light',initial_view_state=pdk.ViewState(latitude=37.76,longitude=-122.4,zoom=11,pitch=50),layers=layers))
else:st.info('Choose at least one map layer in the sidebar.')
st.caption('Source: Streamlit example-data, hello/v1. Local copies of the official tutorial JSON files are bundled; layer names explain the encodings. Base-map tiles need an internet connection.')
