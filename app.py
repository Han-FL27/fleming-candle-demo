import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='Fleming Candle Predictor | AR Demo',page_icon='🕯️',layout='wide')
st.markdown('''<style>.block-container{padding-top:1.4rem;max-width:1250px}div[data-testid="stMetric"]{background:#f2f5f9;border:1px solid #dce3ec;border-radius:13px;padding:14px}div.stButton>button[kind="primary"]{background:#c63543;border-radius:10px;font-weight:700;padding:.7rem 1.5rem}</style>''',unsafe_allow_html=True)
st.title('🕯️ Fleming Candle Burning Predictor')
st.caption('AR PRESENTATION • INTERACTIVE PROOF OF CONCEPT • ALL GENERATED RESULTS ARE SYNTHETIC EXAMPLES, NOT VALIDATED PREDICTIONS')
st.info('How to demo: change candle inputs → click **▶ RUN DEMO PREDICTION** → watch the results appear below. Click again with different settings to compare.')

with st.form('design'):
    st.subheader('1  Enter candle specifications')
    c1,c2,c3=st.columns(3)
    with c1:
        formula=st.selectbox('Wax blend (demo)', ['Palm / Soy blend','Palm wax','Soy wax','Shea / Paraffin blend'])
        weight=st.number_input('Wax fill (oz)',1.,100.,13.,.5)
    with c2:
        diameter=st.number_input('Vessel inner diameter (mm)',30.,200.,85.,1.)
        fragrance=st.number_input('Fragrance (%)',0.,20.,6.,.5)
    with c3:
        series=st.selectbox('Wick family',['Wedo Stabilo','Wedo LX','Wedo PK','Wood wick'])
        candidate=st.slider('Candidate A: number of wicks',1,5,2)
        alternative=st.slider('Candidate B: number of wicks',1,5,3)
    run=st.form_submit_button('▶ RUN DEMO PREDICTION',type='primary',use_container_width=True)

if run:
    st.session_state['result']={'formula':formula,'weight':weight,'diameter':diameter,'fragrance':fragrance,'series':series,'candidate':candidate,'alternative':alternative}
    st.session_state['runs']=st.session_state.get('runs',0)+1

if 'result' not in st.session_state:
    st.markdown('### 2  Awaiting input')
    st.write('Click **RUN DEMO PREDICTION** above. Results, charts, and a comparison will appear here.')
else:
    p=st.session_state['result']; d=p['diameter']; n=p['candidate']; m=p['alternative']
    def scenario(wicks):
        hours=np.arange(0,5,1)
        # Fictional curves for UI demonstration only, deliberately not physical equations.
        factor=(wicks/2)*(85/d)**0.35
        blend={'Palm / Soy blend':1.0,'Palm wax':.94,'Soy wax':.9,'Shea / Paraffin blend':1.06}[p['formula']]
        melt=np.clip(d*(.77+.08*(factor-1))*blend*(1-np.exp(-hours/(1.1+0.1/factor))),0,d)
        temp=24+(24+3*wicks+0.35*(p['fragrance']-6))*(1-np.exp(-hours/1.55))
        flame=np.where(hours==0,0,15+2.8*wicks+1.5*(1-np.exp(-hours/1.2)))
        return pd.DataFrame({'Hour':hours,'Melt pool (mm)':np.round(melt,1),'Glass temperature (°C)':np.round(temp,1),'Flame height (mm)':np.round(flame,1)})
    a=scenario(n); b=scenario(m)
    st.success(f'✓ Demo calculation completed — Run #{st.session_state["runs"]}. Results updated for {p["weight"]:g} oz / Ø{d:g} mm / {p["formula"]}.')
    st.warning('**SYNTHETIC DEMONSTRATION — NOT AI OR LAB-VALIDATED.** These values are generated to show how the future app would respond. Do not use them for wick selection, safety, or production.')
    st.subheader('2  Instant demo results')
    r1,r2,r3,r4=st.columns(4)
    r1.metric('Geometry-only wick range (illustrative)',f'{max(1,int(np.ceil((d/55)**2))-1)}–{min(5,int(np.ceil((d/55)**2))+1)}')
    r2.metric('Candidate A',f'{n} wicks')
    r3.metric('Demo peak glass temp A',f'{a["Glass temperature (°C)"].max():.1f} °C')
    r4.metric('Exact wick size','Not established')
    st.subheader('3  Burning curves — 0 to 4 hours (synthetic)')
    metrics=['Melt pool (mm)','Glass temperature (°C)','Flame height (mm)']
    for metric in metrics:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=a['Hour'],y=a[metric],mode='lines+markers',name=f'A — {n} wicks',line=dict(width=4,color='#c63543')))
        fig.add_trace(go.Scatter(x=b['Hour'],y=b[metric],mode='lines+markers',name=f'B — {m} wicks',line=dict(width=3,color='#316f9b',dash='dash')))
        fig.update_layout(title=metric,height=270,margin=dict(l=20,r=20,t=45,b=25),xaxis_title='Burn time (hours)',yaxis_title=metric,legend=dict(orientation='h',y=1.2))
        st.plotly_chart(fig,use_container_width=True)
    st.subheader('4  Side-by-side scenario comparison')
    left,right=st.columns(2)
    with left:
        st.markdown(f'**Candidate A — {n} {p["series"]} wicks**')
        st.dataframe(a,hide_index=True,use_container_width=True)
    with right:
        st.markdown(f'**Candidate B — {m} {p["series"]} wicks**')
        st.dataframe(b,hide_index=True,use_container_width=True)
    st.error('Soot / wall residue / safety: NOT PREDICTED. Exact wick size: UNKNOWN. Real burn tests are mandatory.')
    data=pd.concat([a.assign(Scenario=f'A ({n} wicks)'),b.assign(Scenario=f'B ({m} wicks)')],ignore_index=True)
    st.download_button('Download synthetic demo results (CSV)',data.to_csv(index=False).encode('utf-8-sig'),'Fleming_Synthetic_Demo_Only.csv','text/csv')

with st.expander('5  What AR would approve — next stage'):
    st.write('**Goal:** convert the demonstration into a validated predictor by linking wax formula, exact wick size, vessel dimensions, and burn-test measurements for the same samples.')
    st.write('**Validation:** reserve real burn tests not used in model training; compare predictions with measured results and quantify errors before relying on outputs.')
    st.write('**Business case:** assess whether the validated tool reduces unsuccessful wick trials and development time; these savings are not yet measured.')
    st.write('**Data security:** this public demonstration contains no Fleming proprietary formula workbook or costing data.')
st.caption('Fleming Candle Intelligence • v4 • Interactive synthetic POC • Not a scientific prediction or product approval tool')
