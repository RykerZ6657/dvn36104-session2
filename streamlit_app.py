import streamlit as st
st.set_page_config(page_title='Streamlit multipage tutorial',page_icon='📊')
st.title('Streamlit multipage tutorial')
st.sidebar.success('Select a demo in the sidebar.')
st.write('Explore three tutorial demonstrations: plotting, mapping and dataframes. Each page is a separate Python file in the pages directory.')
st.markdown('**Plotting demo:** animate a seeded random walk.\n\n**Mapping demo:** compare bike racks, BART stops and outbound travel layers.\n\n**DataFrame demo:** compare gross agricultural production for selected countries.')
st.caption('Based on the official tutorial: https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app')
