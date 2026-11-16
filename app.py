import streamlit as st
import pandas as pd
st.set_page_config(page_title='Fleming Candle Lab Demo',page_icon='🕯️',layout='wide')
st.title('🕯️ Fleming Candle Lab — Prototype')
st.info('DEMO ONLY — No trained AI model. Results below are historical observations, not predictions or safety approval.')
records = pd.DataFrame([
 {'Report':'260107-009','Product':'15.1 oz 2-wick glass jar — Cabin Moon','Type':'Container candle','Size (oz)':15.1,'Wicks':2,'Flame (mm)':'22–25','Glass max (°C)':56,'Wax pool max (°C)':70,'Burn time (h)':50,'Soot':'Grade 0','Result':'PASS','Formula code':'Unknown','Wick size':'Unknown'},
 {'Report':'260225-005','Product':'Wands taper — Brown Leather','Type':'Taper','Size (oz)':None,'Wicks':None,'Flame (mm)':'38–40','Glass max (°C)':None,'Wax pool max (°C)':None,'Burn time (h)':5,'Soot':'N/A','Result':'PASS','Formula code':'Unknown','Wick size':'Unknown'}])
t1,t2,t3=st.tabs(['New candle / Predict','Historical reports','Data requirements'])
with t1:
 st.subheader('Enter new candle specifications')
 a,b=st.columns(2)
 with a:
  formula=st.text_input('Formula code',placeholder='e.g. Formula ID from Excel')
  size=st.number_input('Wax weight (oz)',min_value=0.0,value=13.0,step=0.5)
  diameter=st.number_input('Vessel inner diameter (mm)',min_value=0.0,value=85.0,step=1.0)
 with b:
  fragrance=st.number_input('Fragrance load (%)',min_value=0.0,max_value=30.0,value=6.0,step=0.5)
  series=st.selectbox('Wick series',['Wedo Stabilo','Wedo LX','Wedo PK','Wood wick','Other'])
  wick_count=st.number_input('Wicks to evaluate',min_value=1,max_value=12,value=2)
 if st.button('Predict burning performance',type='primary'):
  st.warning('Insufficient linked burn-test data. No scientifically defensible wick-count, wick-size or burn-curve prediction is available yet.')
  st.write('**Entered design:**',f'{size:g} oz · Ø{diameter:g} mm · {fragrance:g}% fragrance · {series} · {wick_count} wicks')
  st.write('**Historical example only:** A different 15.1 oz Target glass jar with 2 wicks passed its burn test. Its formula and wick size are unknown; it cannot validate your new design.')
with t2:
 st.subheader('Uploaded burn-test reports — extracted observations')
 st.dataframe(records,use_container_width=True,hide_index=True)
 st.download_button('Download sample observations (CSV)',records.to_csv(index=False).encode('utf-8-sig'),'fleming_burn_test_observations.csv','text/csv')
 st.caption('Source: uploaded Target reports 260107-009 and 260225-005. Values are reported maxima/summary, not hourly time series.')
with t3:
 st.subheader('Data needed before training an AI model')
 st.markdown('''For **each tested sample**, record:\n- Formula code and full wax composition; fragrance type and percentage\n- Vessel inside diameter, shape, fill weight, glass thickness\n- Wick supplier, series, exact size, count, and spacing\n- Burn cycle and measurements by hour: flame height, melt pool diameter/depth, vessel temperature, wax consumption\n- Soot, residue, stability, pass/fail, test date, original report link\n\n**Important:** The two provided reports do not link wick size or wax formula to outcomes. A historical PASS does not imply another candle will pass.''')
 st.markdown('**Next step:** standardize these fields, have Lab validate them, then build and evaluate a predictive model against unseen burn tests.')
