import io
import math
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title='Fleming Candle Predictor v5',page_icon='🕯️',layout='wide')
st.title('🕯️ Fleming Candle Burning Predictor | v5')
st.caption('INTERACTIVE SYNTHETIC DEMO • NOT LAB VALIDATED • NOT FOR PRODUCT APPROVAL')
st.warning('All numbers, vessel-material adjustments, burning-time estimates and visuals below are illustrative assumptions, NOT measured or scientifically validated predictions. Never use for safety, wick selection or production decisions.')

MATERIALS = {'Glass': {'thermal': 1.0, 'spread': 1.0, 'depth': 1.0, 'color': '#9cc9d5'}, 'Ceramic': {'thermal': .88, 'spread': .92, 'depth': .95, 'color': '#d7c7b5'}, 'Tin Can': {'thermal': 1.16, 'spread': 1.08, 'depth': 1.12, 'color': '#a9b3bd'}}
WAX = {'Palm / Soy blend': 1.0, 'Palm wax': .94, 'Soy wax': .91, 'Shea / Paraffin blend': 1.05, 'Rice / Palm blend': .97}

with st.form('inputs'):
    st.subheader('1. Candle specifications')
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        material=st.selectbox('Vessel material',list(MATERIALS))
        wax=st.selectbox('Wax blend',list(WAX))
        fill=st.number_input('Wax fill (g)',min_value=30.0,max_value=3000.0,value=370.0,step=10.0)
    with c2:
        diameter=st.number_input('Vessel inner diameter (mm)',30.0,250.0,85.0,1.0)
        height=st.number_input('Vessel inner height (mm)',25.0,300.0,100.0,1.0)
        wall=st.number_input('Wall thickness (mm)',0.3,20.0,3.0,0.5)
    with c3:
        fragrance=st.number_input('Fragrance load (%)',0.0,20.0,6.0,0.5)
        wick=st.selectbox('Wick family',['Wedo Stabilo','Wedo LX','Wedo PK','Wood wick'])
        wick_size=st.text_input('Wick size / code (reference only)','TBD')
    with c4:
        a=st.slider('Candidate A — wick count',1,6,2)
        b=st.slider('Candidate B — wick count',1,6,3)
        ambient=st.number_input('Ambient temperature (°C)',15.0,40.0,25.0,1.0)
        hours=st.slider('Visual simulation window (hours)',2,12,4)
    run=st.form_submit_button('▶ RUN DEMO PREDICTION',type='primary',use_container_width=True)

if run:
    st.session_state['params']=dict(material=material,wax=wax,fill=fill,diameter=diameter,height=height,wall=wall,fragrance=fragrance,wick=wick,wick_size=wick_size,a=a,b=b,ambient=ambient,hours=hours)


def scenario(p,n):
    # Purely fictional, bounded curves for interface demonstration.
    mat=MATERIALS[p['material']]
    d=p['diameter']
    t=np.linspace(0,p['hours'],p['hours']*4+1)
    scale=(n/2.0)*(85.0/d)**.35
    response=1-np.exp(-t/(1.15+.12/max(scale,.2)))
    melt=np.clip(d*(.77+.075*(scale-1))*WAX[p['wax']]*mat['spread']*response,0,d)
    depth=np.maximum(0, (4.8+1.6*n)*mat['depth']*response)
    surface=p['ambient']+(23+3.1*n+.3*(p['fragrance']-6))*mat['thermal']*response
    flame=np.where(t<.01,0,15+2.7*n+1.6*(1-np.exp(-t/1.2)))
    # Demonstration-only burn rate and duration; not derived from calorimetry or wick trials.
    rate=(4.2+2.6*n)*(d/85)**.15*WAX[p['wax']]*mat['spread']
    duration=.88*p['fill']/rate
    df=pd.DataFrame({'Hour':np.round(t,2),'Melt pool diameter (mm)':np.round(melt,1),'Melt pool depth (mm)':np.round(depth,1),'Vessel temperature (°C)':np.round(surface,1),'Flame height (mm)':np.round(flame,1)})
    return df,duration,rate


def draw_frame(p,n,df,idx):
    S=540
    im=Image.new('RGB',(S,620),'#f5f7fa')
    dr=ImageDraw.Draw(im)
    dr.text((22,16),'FLEMING • SYNTHETIC BURN VISUAL',fill='#1c2836')
    dr.text((22,42),f"{p['material']} | {n} wick(s) | {df.iloc[idx]['Hour']:.2f} h",fill='#394c60')
    cx,cy=270,315
    radius=190
    mat=MATERIALS[p['material']]
    dr.ellipse((cx-radius-10,cy-radius-10,cx+radius+10,cy+radius+10),fill=mat['color'],outline='#566779',width=5)
    dr.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill='#efe1bd',outline='#bba983',width=3)
    mp=float(df.iloc[idx]['Melt pool diameter (mm)'])/p['diameter']*radius
    if mp>1:
        dr.ellipse((cx-mp,cy-mp,cx+mp,cy+mp),fill='#d5ae6e',outline='#a77d44',width=3)
    positions=[]
    if n==1: positions=[(cx,cy)]
    else:
        rr=radius*.40
        positions=[(cx+rr*math.cos(2*math.pi*k/n-math.pi/2),cy+rr*math.sin(2*math.pi*k/n-math.pi/2)) for k in range(n)]
    for x,y in positions:
        dr.ellipse((x-5,y-5,x+5,y+5),fill='#28231c')
        if idx>0:
            dr.ellipse((x-9,y-32,x+9,y-3),fill='#f5ad33')
            dr.ellipse((x-4,y-24,x+4,y-5),fill='#fff3b2')
    dr.text((22,545),f"Melt pool: {df.iloc[idx]['Melt pool diameter (mm)']:.1f} mm  |  Depth: {df.iloc[idx]['Melt pool depth (mm)']:.1f} mm",fill='#28394c')
    dr.text((22,570),f"Vessel temp: {df.iloc[idx]['Vessel temperature (°C)']:.1f} C   |  NOT A REAL TEST",fill='#a43b41')
    return im

if 'params' not in st.session_state:
    st.info('Enter specifications and click RUN DEMO PREDICTION to display the simulation.')
else:
    p=st.session_state['params']
    A,at,ar=scenario(p,p['a'])
    B,bt,br=scenario(p,p['b'])
    st.subheader('2. Burning time & key performance (synthetic)')
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Burning time • A',f'{at:.1f} h')
    c2.metric('Burning time • B',f'{bt:.1f} h')
    c3.metric('Peak vessel temperature • A',f"{A['Vessel temperature (°C)'].max():.1f} °C")
    c4.metric('Exact wick size','Not predicted')
    st.caption('Burning time is a hypothetical estimate using an assumed burn rate and usable wax fraction. The displayed temperature is a synthetic vessel temperature, not a safety assessment. Melting point is a wax property; vessel material influences heat transfer rather than directly changing wax melting point.')
    st.subheader('3. Burning performance curves')
    for metric in ['Melt pool diameter (mm)','Melt pool depth (mm)','Vessel temperature (°C)','Flame height (mm)']:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=A['Hour'],y=A[metric],name=f"A • {p['a']} wicks",mode='lines',line=dict(color='#c63543',width=3)))
        fig.add_trace(go.Scatter(x=B['Hour'],y=B[metric],name=f"B • {p['b']} wicks",mode='lines',line=dict(color='#286d9e',dash='dash',width=3)))
        fig.update_layout(title=metric,xaxis_title='Elapsed hours',height=275,margin=dict(l=15,r=15,t=40,b=25))
        st.plotly_chart(fig,use_container_width=True)
    st.subheader('4. Image & animated burning simulation')
    st.info('Top-view schematic only. Animation frames show synthetic melt-pool expansion; they are not photographs, realistic flames, or a validated physical video.')
    choice=st.radio('Visualize candidate',['A','B'],horizontal=True)
    df,n=(A,p['a']) if choice=='A' else (B,p['b'])
    index=st.slider('Select elapsed time',0,len(df)-1,len(df)-1,format='%d steps')
    pic=draw_frame(p,n,df,index)
    img_buf=io.BytesIO();pic.save(img_buf,format='PNG')
    st.image(pic,caption=f"Candidate {choice} • {df.iloc[index]['Hour']:.2f} h • synthetic schematic",width=450)
    st.download_button('Download prediction image (PNG)',img_buf.getvalue(),file_name=f'Fleming_v5_{choice}_synthetic.png',mime='image/png')
    if st.button('🎞 Generate animated burning preview (GIF)'):
        with st.spinner('Creating animation...'):
            inds=np.linspace(0,len(df)-1,min(30,len(df))).astype(int)
            frames=[draw_frame(p,n,df,int(i)).resize((405,465)) for i in inds]
            buf=io.BytesIO()
            frames[0].save(buf,format='GIF',save_all=True,append_images=frames[1:],duration=220,loop=0,optimize=True)
            st.session_state['gif_bytes']=buf.getvalue()
            st.session_state['gif_key']=(tuple(sorted(p.items())),choice)
    if st.session_state.get('gif_key')==(tuple(sorted(p.items())),choice):
        st.image(st.session_state['gif_bytes'],caption='Animated schematic • NOT a recorded burning test')
        st.download_button('Download animated burning preview (GIF)',st.session_state['gif_bytes'],file_name=f'Fleming_v5_{choice}_burning_animation.gif',mime='image/gif')
    st.subheader('5. Candidate A / B results')
    x,y=st.columns(2)
    with x:
        st.markdown(f"**A — {p['a']} {p['wick']} wicks**")
        st.dataframe(A,use_container_width=True,hide_index=True)
    with y:
        st.markdown(f"**B — {p['b']} {p['wick']} wicks**")
        st.dataframe(B,use_container_width=True,hide_index=True)
    combined=pd.concat([A.assign(Candidate='A'),B.assign(Candidate='B')],ignore_index=True)
    st.download_button('Download comparison CSV',combined.to_csv(index=False).encode('utf-8-sig'),file_name='Fleming_v5_SYNTHETIC_results.csv',mime='text/csv')
    st.error('NOT PREDICTED: soot, wall residue, true burn-out time, cracking/thermal shock, real temperature limits, wick size, or safety compliance. Lab testing is mandatory.')
with st.expander('6. Roadmap: replace synthetic assumptions with Lab-trained model'):
    st.write('Collect actual vessel material, thickness, diameter, height, wax blend, fragrance, wick series/size/count/positions, burn time, mass loss per interval, melt pool diameter/depth, flame height, vessel temperature, soot, residue and failure modes. Fit and validate separate models on held-out burn tests. Use uncertainty intervals and reject out-of-domain inputs. Capture real test photos/videos for comparison with simulated visuals.')
st.caption('Fleming Candle Intelligence • v5 synthetic prototype • No proprietary Fleming data included')
