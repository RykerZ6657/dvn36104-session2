import time
import numpy as np
import pandas as pd
import streamlit as st
st.title('Plotting demo')
st.write('A random walk demonstrates charts, progress updates and reruns. This is synthetic data, not an observed trend.')
seed=st.number_input('Random seed',min_value=0,max_value=100000,value=36104,step=1)
rng=np.random.default_rng(int(seed))
values=np.vstack([np.zeros((1,3)),rng.normal(size=(500,3)).cumsum(axis=0)])
placeholder=st.empty()
if st.button('Animate walk',key='animate'):
    progress=st.progress(0);status=st.empty()
    for step in range(1,101):
        placeholder.line_chart(pd.DataFrame(values[:step*5+1],columns=['Series A','Series B','Series C']))
        progress.progress(step);status.caption(f'{step}% complete');time.sleep(.02)
    progress.empty();status.empty()
else:placeholder.line_chart(pd.DataFrame(values,columns=['Series A','Series B','Series C']))
st.caption('Changing the seed changes the walk; repeating the same seed reproduces it.')
