"""Teaching model adapted from DVN36104 star_app.py; not a stellar-evolution solver."""
import math
import numpy as np
SUN_T=5772.0

def blackbody_colour(temperature):
    t=max(1000.0,min(float(temperature),40000.0))/100
    r=255 if t<=66 else 329.7*(t-60)**-.1332
    g=99.47*math.log(t)-161.1 if t<=66 else 288.1*(t-60)**-.0755
    b=255 if t>=66 else 0 if t<=19 else 138.5*math.log(t-10)-305
    r,g,b=[int(np.clip(round(v),0,255)) for v in [r,g,b]]
    return f'rgb({r},{g},{b})'

def star_state(mass,age,Z):
    zr=Z/.02
    L=mass**3.5*zr**-.1;R=mass**.8;T=SUN_T*(L/R**2)**.25
    t_pre=.03*mass**-1.5
    t_ms=(10*mass**-2.5*(1+2.5*math.exp(-mass/.12))+.0025)*zr**.1
    t_g=1.15*t_ms
    pair_instability=140<=mass<=260 and Z<.001
    if age<=t_pre:phase='protostar'
    elif age<=t_ms:phase='main sequence'
    elif mass<.25:phase='white dwarf'
    elif mass<8:phase='red giant' if age<=t_g else 'white dwarf'
    elif age<=t_g:phase='blue supergiant' if (age-t_ms)/(t_g-t_ms)<.4 else 'red supergiant'
    elif age<=1.10*t_g:phase='pair-instability supernova' if pair_instability else 'supernova'
    elif pair_instability:phase='no remnant'
    elif mass<18+7*zr:phase='neutron star'
    else:phase='black hole'
    if phase=='protostar':T,L,R=.75*T,2*L,3*R
    elif phase=='red giant':
        T=3900.;R=max(R*60,10);L=R**2*(T/SUN_T)**4
    elif phase=='blue supergiant':
        T=12000.;R=30+120*(age-t_ms)/(t_g-t_ms);L=R**2*(T/SUN_T)**4
    elif phase=='red supergiant':
        T=3500.;R=min(200+900*(age-t_ms)/(t_g-t_ms),900);L=R**2*(T/SUN_T)**4
    elif phase=='white dwarf':
        cool=max(age-(t_ms if mass<.25 else t_g),.001)
        T=float(np.clip(60000*(.01/cool)**.3,3500,150000));R=.009;L=R**2*(T/SUN_T)**4
    elif phase in ['supernova','pair-instability supernova']:T,L,R=8000.,None,None
    elif phase=='neutron star':T,L,R=1e6,None,1.7e-5
    elif phase=='black hole':T,L,R=None,None,4.2e-6*mass/10
    elif phase=='no remnant':T,L,R=None,None,None
    return phase,T,L,R,t_ms
