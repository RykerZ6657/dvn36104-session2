from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st
st.title('DataFrame demo')
st.write('Compare gross agricultural production across countries and years.')
@st.cache_data
def load_agriculture():return pd.read_csv(Path(__file__).resolve().parents[1]/'agri.csv').set_index('Region')
df=load_agriculture()
countries=st.multiselect('Choose countries',list(df.index),['China','United States of America'],key='countries')
if not countries:
    st.info('Please select at least one country.')
else:
    selected=df.loc[countries].astype(float)/1_000_000
    st.subheader('Gross agricultural production ($B)');st.dataframe(selected.sort_index())
    tidy=selected.reset_index().melt(id_vars='Region',var_name='Year',value_name='Production ($B)')
    tidy['Year']=tidy.Year.astype(int)
    chart=alt.Chart(tidy).mark_area(opacity=.25).encode(x=alt.X('Year:Q',axis=alt.Axis(format='d')),
              y=alt.Y('Production ($B):Q',stack=None),color=alt.Color('Region:N',title='Country'),tooltip=['Region:N','Year:Q',alt.Tooltip('Production ($B):Q',format='.3f')])
    st.altair_chart(chart,width='stretch')
    st.download_button('Download selected countries',selected.to_csv().encode(),'agricultural_production_billions.csv','text/csv')
st.caption('Source: official Streamlit tutorial agri.csv.gz, credited there to UN Data Explorer. Historical teaching dataset; dollar scaling follows the tutorial, and price-base metadata is not provided in this extract. This is not a current economic indicator.')
