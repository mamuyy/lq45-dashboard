
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Saham LQ45", layout="wide")
st.title("📈 Analisis Saham LQ45 - Ten Bagger Radar")

uploaded_file = st.file_uploader("📂 Upload file Excel hasil scraping", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Data Fundamental Saham")
    st.dataframe(df, use_container_width=True)

    # Hitung skor gabungan
    df["Skor"] = (
        df["ROE (%)"].fillna(0)/5 +
        df["Revenue Growth (%)"].fillna(0)/10 +
        df["PER"].apply(lambda x: 5 if x < 10 else (3 if x < 20 else 1)) +
        df["PBV"].apply(lambda x: 5 if x < 1.5 else (3 if x < 3 else 1))
    )

    df_sorted = df.sort_values(by="Skor", ascending=False)

    # Filter Dinamis
    st.sidebar.header("🔎 Filter Saham")
    per_max = st.sidebar.slider("PER maksimum", 0, 50, 25)
    roe_min = st.sidebar.slider("ROE minimum (%)", 0, 40, 10)
    growth_min = st.sidebar.slider("Revenue Growth minimum (%)", 0, 100, 20)

    filtered = df_sorted[
        (df_sorted["PER"].fillna(99) <= per_max) &
        (df_sorted["ROE (%)"].fillna(0) >= roe_min) &
        (df_sorted["Revenue Growth (%)"].fillna(0) >= growth_min)
    ]

    st.subheader("🏅 Top 5 Saham Potensial (Filtered)")
    st.dataframe(filtered.head(5)[["Kode Saham", "Nama Emiten", "Skor"]], use_container_width=True)

    # Tombol download
    st.download_button("📥 Download Ranking ke CSV", filtered.to_csv(index=False), "ranking_saham.csv", "text/csv")

    # Radar chart interaktif
    st.subheader("📍 Radar Chart per Saham")
    selected = st.selectbox("Pilih saham", df["Kode Saham"])
    saham = df[df["Kode Saham"] == selected].iloc[0]
    radar_data = pd.DataFrame({
        "Kriteria": ["PER", "PBV", "ROE (%)", "Revenue Growth (%)"],
        "Nilai": [saham["PER"], saham["PBV"], saham["ROE (%)"], saham["Revenue Growth (%)"]]
    })

    fig = px.line_polar(radar_data, r='Nilai', theta='Kriteria', line_close=True)
    st.plotly_chart(fig, use_container_width=True)
