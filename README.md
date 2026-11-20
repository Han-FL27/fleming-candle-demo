# Fleming Candle Burning Predictor v5

Streamlit synthetic demonstration prototype. NOT a validated predictive model.

## New in v5
- Vessel material selection: Glass, Ceramic, Tin Can
- Vessel thickness and height inputs
- Illustrative total burning time for candidates A/B
- Melt pool diameter and depth, vessel temperature, flame height over time
- Downloadable top-view image and animated GIF (video-like schematic)
- CSV export

## Deploy to existing GitHub repository
1. Download and extract the ZIP package.
2. Open your GitHub repository `Han-FL27/fleming-candle-demo`.
3. Choose **Add file > Upload files** and upload `app.py`, `requirements.txt`, `README.md` from the extracted folder (not the ZIP itself).
4. Confirm **Commit changes**, replacing the existing files. Streamlit should redeploy from `main`.
5. If starting a new Streamlit app, choose `main` branch and `app.py` entrypoint.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Scientific limitations
All equations and material factors are fictional demonstration values. The animation is a schematic GIF, not measured footage or an MP4 video. Do not use for real wick selection, product quality, compliance, thermal shock, or production. Actual wax melting point is not determined by vessel material. To predict performance reliably, use validated Lab measurements and real vessel-specific data.
