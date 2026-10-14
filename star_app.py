"""Session 2 Part D: metallicity, pair-instability and a linked Altair HR diagram."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from star_model import SUN_T,star_state,blackbody_colour

st.set_page_config(page_title='AppStar — metallicity and the HR diagram',layout='wide')
st.title('AppStar: mass, age and metallicity')
st.caption('A simplified course model. Mass and age update both panels live; metallicity rebuilds the stellar grid.')
lz=st.slider('log10 metallicity',-4.0,-1.4,-1.7,step=.05,key='metallicity')
Z=10**lz;zr=Z/.02
st.write(f'Metal mass fraction Z = {Z:.5f}; neutron-star / black-hole birth-mass boundary ≈ {18+7*zr:.2f} solar masses.')
alt.data_transformers.disable_max_rows()

@st.cache_data
def make_grid(metallicity):
    rows=[]
    for lm in np.round(np.arange(-1,2.451,.05),2):
        for la in np.round(np.arange(-4,3.561,.06),2):
            m,a=10**lm,10**la
            phase,T,L,R,life=star_state(m,a,metallicity)
            color=('#172B3A' if phase=='black hole' else '#CDE7FF' if phase=='neutron star'
                   else '#FFB640' if 'supernova' in phase else '#CCCCCC' if phase=='no remnant'
                   else blackbody_colour(T))
            size=0 if phase=='no remnant' else 1600 if phase=='black hole' else 36 if phase=='neutron star' else 150**2 if 'supernova' in phase else float(np.clip(14+26*(np.log10(R)+2.2),5,150))**2
            rows.append({'lm':float(lm),'la':float(la),'mass':m,'age':a,'phase':phase,
                         'temp_K':T,'lum':L,'rad':R,'colour':color,'size':size,
                         'description':f'{m:.3g} solar masses • {a:.3g} Gyr',
                         'temperature':f'Surface temperature: {T:,.0f} K' if T else '',
                         'luminosity':f'Luminosity: {L:.3g} L☉' if L else 'No equilibrium luminosity plotted',
                         'lifetime':f'Main-sequence lifetime: {life:.3g} Gyr'})
    return pd.DataFrame(rows)

grid=make_grid(Z)
mass=alt.param(name='mass_pick',value=0.,bind=alt.binding_range(min=-1.,max=2.45,step=.05,name='log10 mass (solar masses) '))
age=alt.param(name='age_pick',value=.68,bind=alt.binding_range(min=-4.,max=3.56,step=.06,name='log10 age (Gyr) '))
pick='abs(datum.lm - mass_pick) < 0.02 && abs(datum.la - age_pick) < 0.02'
selected=alt.Chart(grid).transform_filter(pick)
disc=selected.mark_circle(opacity=1).encode(x=alt.value(170),y=alt.value(135),
                size=alt.Size('size:Q',scale=None,legend=None),color=alt.Color('colour:N',scale=None,legend=None))
ring=selected.transform_filter("datum.phase == 'black hole'").mark_point(filled=False,size=2400,stroke='#BC7900',strokeWidth=3,opacity=1).encode(x=alt.value(170),y=alt.value(135))
def readout(field,y,bold=False):
    return selected.mark_text(fontSize=14 if bold else 11,color='#172B3A',fontWeight='bold' if bold else 'normal').encode(x=alt.value(170),y=alt.value(y),text=field)
portrait=alt.layer(disc,ring,readout('phase:N',250,True),readout('description:N',277),
                  readout('temperature:N',303),readout('luminosity:N',329),readout('lifetime:N',355)).properties(width=340,height=390,title='Your star — illustrative portrait')

sweep=np.geomspace(.1,300,200)
band=pd.DataFrame({'mass':sweep,'lum':sweep**3.5*zr**-.1,'temp_K':SUN_T*sweep**.475*zr**-.025})
xs=alt.Scale(type='log',reverse=True,domain=[1500,150000],nice=False)
ys=alt.Scale(type='log',domain=[1e-4,1e6],nice=False)
x=alt.X('temp_K:Q',title='Surface temperature (K), log scale — hot ←',scale=xs)
y=alt.Y('lum:Q',title='Luminosity (solar units), log scale',scale=ys)
main=alt.Chart(band).mark_line(strokeWidth=8,color='#ABB8C7',opacity=.55,clip=True).encode(x=x,y=y,order='mass:Q')
point=selected.transform_filter('isValid(datum.lum) && datum.lum > 0').mark_point(filled=True,size=200,
                    opacity=1,stroke='#172B3A',strokeWidth=1.5,clip=True).encode(x=x,y=y,color=alt.Color('colour:N',scale=None,legend=None),
                    tooltip=['phase:N',alt.Tooltip('mass:Q',format='.3g'),alt.Tooltip('age:Q',format='.3g'),alt.Tooltip('temp_K:Q',format=',.0f'),alt.Tooltip('lum:Q',format='.3g')])
sun=alt.Chart(pd.DataFrame({'temp_K':[5772.],'lum':[1.]})).mark_point(shape='cross',color='#A07D00',size=100).encode(x=x,y=y)
sun_label=alt.Chart(pd.DataFrame({'temp_K':[5772.],'lum':[1.]})).mark_text(text='Sun reference',dx=10,dy=10,align='left',fontSize=10,color='#876500').encode(x=x,y=y)
hr=alt.layer(main,point,sun,sun_label).properties(width=520,height=390,title='Hertzsprung–Russell diagram')
chart=alt.hconcat(portrait,hr).add_params(mass,age).configure_view(stroke=None).configure_axis(gridOpacity=.15)
st.altair_chart(chart,width='content')
st.caption('The muted band is the main sequence at the chosen metallicity. Solar reference is fixed at 5772 K and 1 L☉. Both axes are logarithmic; hotter stars are on the left.')
st.info('Supernovae are transient events; neutron stars, black holes and the no-remnant outcome have no equilibrium luminosity in this model and therefore no HR point. They remain identified in the portrait readout.')
st.caption('At Z < 0.001, birth masses 140–260 M☉ enter pair-instability supernova and then no remnant. The slider extends beyond the present age of the Universe to explore future model states. Disc size and colour are illustrative, not calibrated images.')
st.caption('Source and starter: https://dvn36104.github.io/session2/part-d.html • Metallicity-aware luminosity, lifetime and remnant rules follow the course approximations.')
