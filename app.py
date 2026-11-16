import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title='Fleming | Candle Intelligence POC',page_icon='🕯️',layout='wide')
st.markdown('''<style>.block-container{padding-top:1.5rem;max-width:1300px}h1,h2,h3{letter-spacing:-.03em}div[data-testid="stMetric"]{background:#f4f6f9;padding:16px;border-radius:12px;border:1px solid #e8ebf0} .small-note{color:#666;font-size:.86rem}</style>''',unsafe_allow_html=True)
st.title('🕯️ Fleming Candle Intelligence')
st.caption('EXECUTIVE PROOF OF CONCEPT  |  Demonstration only — NOT a validated burn prediction model')
with st.sidebar:
    st.header('New candle design')
    formula=st.selectbox('Wax blend (illustrative)', ['Palm / Soy blend','Palm wax','Soy wax','Shea / Paraffin blend','Other'])
    weight=st.number_input('Wax fill (oz)',1.,100.,13.,.5)
    diameter=st.number_input('Vessel inner diameter (mm)',30.,200.,85.,1.)
    height=st.number_input('Vessel inner height (mm)',30.,250.,100.,5.)
    fragrance=st.number_input('Fragrance load (%)',0.,20.,6.,.5)
    series=st.selectbox('Wick series to explore',['Wedo Stabilo','Wedo LX','Wedo PK','Wood wick','Other'])
    count=st.slider('Candidate wick count',1,5,2)
    compare=st.slider('Alternative wick count',1,5,3)
    st.info('No proprietary Fleming formulas are embedded or uploaded in this public demo.')

st.warning('⚠️ DEMO / SYNTHETIC SCENARIOS: All simulation curves and risk indicators below are illustrative, not measurements, scientific predictions, or approval criteria. Actual wick size and safe performance require linked burn tests.')

def synthetic(n):
    # Display-only scenario: deterministic synthetic patterns, not physical equations.
    h=np.arange(0,5)
    area=np.pi*(diameter/2)**2
    coverage=np.clip(n*55**2/(diameter**2),.15,1.6)
    melt=np.clip((1-np.exp(-h/1.45))*diameter*(.55+.24*coverage),0,diameter)
    temp=24+(23+3*n)*(1-np.exp(-h/1.5))
    flame=np.where(h==0,0,14+3*n+2*(1-np.exp(-h/1.2)))
    return pd.DataFrame({'Hour':h,'Melt pool diameter (mm)':np.round(melt,1),'Glass temperature (°C)':np.round(temp,1),'Flame height (mm)':np.round(flame,1)})

p1,p2,p3,p4=st.tabs(['01  Design screening','02  Burn simulation','03  Evidence & validation','04  Business case for AR'])
with p1:
    st.subheader('Candidate screening — conceptual illustration')
    # Historical 55mm reference is an assumed visualization parameter, not a validated model.
    area=np.pi*(diameter/2)**2
    estimate=max(1,int(np.ceil(area/(np.pi*(55/2)**2))))
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Diameter',f'{diameter:.0f} mm')
    c2.metric('Geometry-only reference',f'{max(1,estimate-1)}–{min(5,estimate+1)} wicks')
    c3.metric('Candidate A',f'{count} wicks')
    c4.metric('Exact wick size','Not established')
    st.info('Geometry-only reference uses an ASSUMED 55 mm nominal coverage diameter. It is not a recommendation, validated wick-count prediction or wick-size selection.')
    st.markdown('#### What a production system would return')
    st.dataframe(pd.DataFrame([
        {'Output':'Wick count / arrangement','POC status':'Illustrative screening only','Production requirement':'Verified formula + vessel + historical wick/burn outcomes'},
        {'Output':'Wick series and exact size','POC status':'Not available','Production requirement':'Manufacturer size specification + matched tests'},
        {'Output':'Melt pool / temperature / flame','POC status':'Synthetic example charts','Production requirement':'Hourly test measurements and validation'},
        {'Output':'Soot / residue / safety','POC status':'Qualitative review checklist','Production requirement':'Observed outcomes and customer acceptance criteria'}]),hide_index=True,use_container_width=True)
    st.markdown('#### Lab trial checklist')
    for label in ['Confirm formula and fragrance ID','Record vessel dimensions and glass thickness','Record exact wick series, size, count and placement','Run standard burn cycles and record measurements','Review soot, residue, glass temperature and failure modes']:
        st.checkbox(label)
with p2:
    st.subheader('Two-design scenario comparison')
    st.caption('Synthetic curves only — to demonstrate the future user experience. These are NOT predictions for the selected candle.')
    a=synthetic(count); b=synthetic(compare)
    metric=st.selectbox('Chart measurement',['Melt pool diameter (mm)','Glass temperature (°C)','Flame height (mm)'])
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=a['Hour'],y=a[metric],name=f'Candidate A: {count} wicks',mode='lines+markers'))
    fig.add_trace(go.Scatter(x=b['Hour'],y=b[metric],name=f'Candidate B: {compare} wicks',mode='lines+markers',line={'dash':'dash'}))
    fig.update_layout(height=380,margin=dict(l=15,r=15,t=20,b=15),xaxis_title='Elapsed burn time (hours)',yaxis_title=metric,legend=dict(orientation='h',y=1.12))
    st.plotly_chart(fig,use_container_width=True)
    st.caption('Synthetic generation is deterministic and illustrative; changing wick count changes the curve visually but does not model candle physics.')
    st.markdown('#### Example hourly report layout (synthetic)')
    tab=a.copy();tab.insert(0,'Scenario',f'A: {count} wicks');tab2=b.copy();tab2.insert(0,'Scenario',f'B: {compare} wicks')
    st.dataframe(pd.concat([tab,tab2],ignore_index=True),hide_index=True,use_container_width=True)
    st.download_button('Download synthetic example CSV',pd.concat([tab,tab2],ignore_index=True).to_csv(index=False).encode(),'synthetic_demo_only.csv','text/csv')
    st.markdown('#### Risk assessment — required evidence')
    cols=st.columns(4)
    for col,name,desc in zip(cols,['Tunneling','Soot','High glass temp','Wall residue'],['Melt pool width / depth','Visual soot grading','Measured peak temperature','End-of-life inspection']):
        with col:
            st.error('NOT ASSESSED')
            st.write('**'+name+'**')
            st.caption(desc)
with p3:
    st.subheader('Evidence readiness')
    st.success('Available: wax formulation workbook; historical burn reports; reference wick library.')
    st.error('Missing link: verified formula ID + exact wick series/size + vessel details + hourly burn data for the SAME tested sample.')
    st.markdown('#### Existing report — historical observation only')
    st.write('15.1 oz Target glass jar, 2 wicks: prior report recorded PASS; reported peak glass temperature 56°C, peak wax-pool temperature 70°C, flame height 22–25 mm, soot grade 0 and total burn time 50 hours. Formula and exact wick size are not linked. This does not validate any current input.')
    st.markdown('#### Minimum data per tested sample')
    template=pd.DataFrame(columns=['Test_ID','Formula_Code','Wax_Composition','Fragrance_ID','Fragrance_pct','Fill_oz','Vessel_Inner_Diameter_mm','Vessel_Height_mm','Wick_Series','Wick_Size','Wick_Count','Wick_Placement_mm','Cycle','Elapsed_Hours','Melt_Pool_Diameter_mm','Melt_Pool_Depth_mm','Flame_Height_mm','Glass_Temp_C','Soot_Grade','Wall_Residue','Pass_Fail','Source_Report'])
    st.download_button('Download Lab data template (CSV)',template.to_csv(index=False).encode(),'Fleming_Lab_Burn_Test_Template.csv','text/csv')
    st.markdown('#### How feasibility will be proven')
    st.write('1. Link a small set of real, representative test records.  2. Train a baseline on one subset.  3. Predict withheld samples without seeing their results.  4. Compare prediction error with a simple engineering baseline.  5. Expand only if performance is useful and repeatable.')
with p4:
    st.subheader('Decision brief for AR')
    st.markdown('**Proposal:** Build a searchable burn-test database, then validate an AI-assisted wick-screening tool before any production use.')
    c1,c2,c3=st.columns(3)
    c1.metric('Phase 1','Database')
    c2.metric('Phase 2','Validated POC')
    c3.metric('Phase 3','Lab rollout')
    st.markdown('**Expected value to evaluate (not yet measured):** fewer unsuccessful trial combinations, faster development screening, reusable historical knowledge, consistent reporting.')
    st.markdown('**What AR is being asked to approve:** a limited pilot to standardize burn-test records and provide a small linked dataset for independent model validation — not approval of an untested AI recommendation.')
    st.markdown('**Success criteria to agree with AR:** measurable reduction in trial rounds or screening time; prediction errors within agreed limits; no relaxation of safety burn testing.')
    st.markdown('**Next step:** assign a Lab data owner and choose 10–20 fully traceable candle trials for a feasibility study. This is a proposed starting scope, not a proven minimum sample size.')

st.divider()
st.caption('Fleming Candle Intelligence POC • v3 • Presentation prototype • No proprietary formula database connected • Lab testing remains mandatory')
