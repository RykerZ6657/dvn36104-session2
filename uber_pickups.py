"""Session 2 Part C: adapted from Streamlit's official Create an app tutorial."""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import requests
import streamlit as st

SOURCE='https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'
SAMPLE=Path(__file__).resolve().parent/'uber_first_10000.csv'
st.set_page_config(page_title='Uber pickups in NYC',layout='wide')
st.title('Uber pickups in NYC')
st.caption('September 2014 • first 10,000 records from the official tutorial dataset; not a random sample of all NYC trips.')

@st.cache_data
def load_data(nrows):
    mode='Downloaded from the tutorial source'
    if os.environ.get('TUTORIAL_SAMPLE_MODE')=='1':
        frame=pd.read_csv(SAMPLE,nrows=nrows);mode='Bundled copy of the same first 10,000 records'
    else:
        try:
            with requests.get(SOURCE,stream=True,timeout=(5,15)) as response:
                response.raise_for_status()
                frame=pd.read_csv(response.raw,compression='gzip',nrows=nrows)
        except (requests.RequestException,OSError,EOFError):
            frame=pd.read_csv(SAMPLE,nrows=nrows);mode='Source unavailable; bundled copy of the same first 10,000 records'
    frame.columns=frame.columns.str.lower()
    frame['date/time']=pd.to_datetime(frame['date/time'])
    return frame,mode

with st.spinner('Loading pickup records…'):
    data,mode=load_data(10000)
st.caption(mode+' • cached with st.cache_data')
st.write(f"{len(data):,} pickups; {data['date/time'].min():%d %b %Y %H:%M} to {data['date/time'].max():%d %b %Y %H:%M} (recorded local times).")
if st.checkbox('Show raw data',key='show_raw'):
    st.subheader('Raw data');st.dataframe(data)
st.subheader('Number of pickups by hour')
counts=np.histogram(data['date/time'].dt.hour,bins=24,range=(0,24))[0]
st.bar_chart(pd.DataFrame({'Pickups':counts},index=pd.Index(range(24),name='Hour')))
hour=st.slider('Hour',0,23,17,key='hour')
selected=data.loc[data['date/time'].dt.hour.eq(hour)]
st.subheader(f'Map of pickups at {hour:02d}:00–{hour:02d}:59')
st.metric('Pickups in selected hour',len(selected))
if selected.empty:st.info('No pickups in the selected hour.')
else:st.map(selected[['lat','lon']])
st.download_button('Download selected pickups',selected.to_csv(index=False).encode(),f'pickups_hour_{hour:02d}.csv','text/csv')
st.caption('Source: Streamlit tutorial dataset, originally NYC TLC Uber pickup records. Tutorial: https://docs.streamlit.io/get-started/tutorials/create-an-app')
