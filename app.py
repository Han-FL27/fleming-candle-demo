import math
import streamlit as st
import pandas as pd
st.set_page_config(page_title='Fleming Candle Predictor — Demo v2',page_icon='🕯️',layout='wide')
st.title('🕯️ Fleming Candle Predictor — Demo v2')
st.warning('PRELIMINARY SCREENING ONLY. The wick count below is a geometric starting point, NOT an AI prediction, validated wick recommendation, burn-test result or safety approval. Do not use it to release product.')
reports=pd.DataFrame([{'Report':'260107-009','Product':'15.1 oz Target glass jar','Wick count':2,'Flame (mm)':'22–25','Max glass (°C)':56,'Burn time (h)':50,'Soot':'Grade 0','Result':'PASS','Formula':'Unknown','Wick size':'Unknown'},{'Report':'260225-005','Product':'Wands taper','Wick count':None,'Flame (mm)':'38–40','Max glass (°C)':None,'Burn time (h)':5,'Soot':'N/A','Result':'PASS','Formula':'Unknown','Wick size':'Unknown'}])
a,b,c=st.tabs(['New candle / Get screening result','Historical reports','Data collection'])
with a:
 st.subheader('Enter new candle specifications')
 x,y=st.columns(2)
 with x:
  formula=st.text_input('Formula code (optional)',placeholder='e.g. NL8-17')
  oz=st.number_input('Wax weight (oz)',min_value=1.0,max_value=100.0,value=13.0,step=0.5)
  diameter=st.number_input('Vessel inner diameter (mm)',min_value=20.0,max_value=350.0,value=85.0,step=1.0)
 with y:
  fragrance=st.number_input('Fragrance load (%)',min_value=0.0,max_value=30.0,value=6.0,step=0.5)
  series=st.selectbox('Wick series',['Wedo Stabilo','Wedo LX','Wedo PK','Wood wick','Other'])
  count=st.number_input('Wicks to compare',min_value=1,max_value=12,value=2)
 if st.button('Get preliminary screening result',type='primary'):
  # A transparent geometry-only example: one nominal 55 mm circular coverage region per wick.
  # This is an arbitrary DEMONSTRATION assumption, not an empirical wick sizing law.
  coverage=55.0
  theoretical=(diameter/coverage)**2
  lower=max(1,min(12,math.floor(theoretical)))
  upper=max(1,min(12,math.ceil(theoretical)))
  st.subheader('Preliminary result — geometry-only demo')
  m1,m2,m3=st.columns(3)
  m1.metric('Illustrative wick-count range',f'{lower}–{upper}' if lower!=upper else str(lower))
  m2.metric('Your comparison',f'{count} wicks')
  m3.metric('Exact wick size','Unknown')
  st.info(f'How calculated: circular vessel area ÷ nominal area per wick using an ASSUMED {coverage:g} mm coverage diameter. This is a demo calculation only, not a validated physical model. Your wax formula, wick series, fragrance and vessel design can change the real result.')
  st.write('**Historical observation (not a match):** A different 15.1 oz Target jar with 2 wicks passed its test. Its wax formula, exact wick size and diameter are not linked to this input.')
  st.error('Melt pool, flame height, glass temperature and soot over time: cannot be predicted reliably from the available data. Lab burn testing is required.')
  st.caption('For a usable predictor, collect linked formula + vessel + exact wick size/count + hourly burn measurements and validate against held-out tests.')
with b:
 st.dataframe(reports,hide_index=True,use_container_width=True)
 st.download_button('Download historical observations',reports.to_csv(index=False).encode('utf-8-sig'),'historical_observations.csv','text/csv')
with c:
 st.write('Record each new burn test with the exact formula, vessel, wick supplier/series/size/count, fragrance, burn-cycle timestamps, melt pool, flame height, glass temperature, soot and residue.')
 template=pd.DataFrame(columns=['Sample ID','Formula code','Wax weight (oz)','Vessel diameter (mm)','Fragrance (%)','Wick series','Wick size','Wick count','Burn cycle','Hour','Flame height (mm)','Melt pool diameter (mm)','Glass temperature (C)','Soot','Result','Source report'])
 st.download_button('Download blank burn-test template',template.to_csv(index=False).encode('utf-8-sig'),'burn_test_template.csv','text/csv')
