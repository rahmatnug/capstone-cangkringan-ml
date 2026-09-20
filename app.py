import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import joblib
from predict import DemandPredictor

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Prediksi Produksi Cangkringan",
    page_icon="🌾",
    layout="wide",
)

# ============================================================
# NEO-BRUTALISM CSS
# ============================================================
st.markdown("""
<style>
/* ---------- Google Font ---------- */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ---------- Global ---------- */
.stApp {
    background-color: #FFF8E7 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.main .block-container {
    padding-top: 1.5rem;
    max-width: 1400px;
}
h1, h2, h3, h4, p, span, label, div {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background-color: #FFD600 !important;
    border-right: 4px solid #1a1a1a !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] hr {
    border-color: #1a1a1a !important;
    border-width: 2px !important;
}

/* --- Sidebar: Multiselect --- */
[data-testid="stSidebar"] .stMultiSelect > div {
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
    background: #FFFFFF !important;
}
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #FFFFFF !important;
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #FFD600 !important;
    color: #1a1a1a !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] .stMultiSelect svg {
    fill: #1a1a1a !important;
}
[data-testid="stSidebar"] .stMultiSelect input {
    color: #1a1a1a !important;
}
/* Dropdown menu */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="popover"] {
    background: #FFFFFF !important;
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
}

/* --- Sidebar: Selectbox --- */
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
    min-height: 48px !important;
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
    background: #FFFFFF !important;
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"],
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div,
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] [role="combobox"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] input {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] input::placeholder {
    color: #555555 !important;
    -webkit-text-fill-color: #555555 !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] svg {
    fill: #1a1a1a !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] {
    background: #FFFFFF !important;
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
}

/* --- Sidebar: Date Input --- */
[data-testid="stSidebar"] .stDateInput {
    background: transparent !important;
}
[data-testid="stSidebar"] .stDateInput > div {
    background: transparent !important;
}
[data-testid="stSidebar"] .stDateInput > div > div {
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
    background: #FFFFFF !important;
}
[data-testid="stSidebar"] .stDateInput input {
    background: #FFFFFF !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebar"] .stDateInput svg {
    fill: #1a1a1a !important;
}
[data-testid="stSidebar"] .stDateInput * {
    color: #1a1a1a !important;
}

/* --- Sidebar: Slider --- */
[data-testid="stSidebar"] .stSlider > div {
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div {
    color: #1a1a1a !important;
}

/* --- Sidebar: all generic base-web inputs white bg --- */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border-color: transparent !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] {
    background: #FFFFFF !important;
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
    border: 3px solid #1a1a1a;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 5px 5px 0px #1a1a1a;
    transition: transform 0.15s, box-shadow 0.15s;
}
[data-testid="stMetric"]:hover {
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0px #1a1a1a;
}
/* Rotate colours via nth-child on the column wrapper */
[data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetric"] { background-color: #7BF1A8; }
[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] { background-color: #88D4FF; }
[data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] { background-color: #FFD600; }
[data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] { background-color: #C4B5FD; }
[data-testid="stMetric"] label, [data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Nuclear: target every possible tab element */
.stTabs button[role="tab"],
.stTabs [data-baseweb="tab"],
.stTabs [data-testid="stTab"] {
    background: #FFD600 !important;
    background-color: #FFD600 !important;
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 4px 4px 0px #1a1a1a;
    font-weight: 600 !important;
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    padding: 10px 20px !important;
    transition: all 0.15s;
}
.stTabs button[role="tab"] *,
.stTabs [data-baseweb="tab"] * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    font-weight: 600 !important;
}
.stTabs button[role="tab"] p,
.stTabs [data-baseweb="tab"] p {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    font-weight: 600 !important;
    margin: 0 !important;
}
.stTabs button[role="tab"]:hover,
.stTabs [data-baseweb="tab"]:hover {
    background: #FFD600 !important;
    transform: translate(-2px,-2px);
    box-shadow: 6px 6px 0px #1a1a1a;
}
.stTabs [aria-selected="true"],
.stTabs button[aria-selected="true"] {
    background: #7BF1A8 !important;
    background-color: #7BF1A8 !important;
    transform: translate(2px,2px);
    box-shadow: 2px 2px 0px #1a1a1a !important;
}
.stTabs [aria-selected="true"] *,
.stTabs button[aria-selected="true"] * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
/* ---------- Pills (st.pills) ---------- */
[data-testid="stPills"] button {
    background: #1a1a1a !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 999px !important;
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    transition: all 0.15s;
}
[data-testid="stPills"] button * {
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
}
[data-testid="stPills"] button[aria-checked="true"],
[data-testid="stPills"] button[aria-selected="true"] {
    background: #FFD600 !important;
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    border-color: #1a1a1a !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
}
[data-testid="stPills"] button[aria-checked="true"] *,
[data-testid="stPills"] button[aria-selected="true"] * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
[data-testid="stPills"] button:hover {
    background: #333333 !important;
    transform: translate(-1px, -1px);
}

/* ---------- Segmented Control (st.segmented_control) ---------- */
[data-testid="stSegmentedControl"] button,
[data-testid="stSegmentedControl"] [role="radio"] {
    background: #1a1a1a !important;
    border: 2px solid #1a1a1a !important;
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 6px 14px !important;
    transition: all 0.15s;
}
[data-testid="stSegmentedControl"] button *,
[data-testid="stSegmentedControl"] [role="radio"] * {
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
}
[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"],
[data-testid="stSegmentedControl"] button[data-selected="true"] {
    background: #FFD600 !important;
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    border-color: #1a1a1a !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
}
[data-testid="stSegmentedControl"] button[aria-checked="true"] *,
[data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"] *,
[data-testid="stSegmentedControl"] button[data-selected="true"] * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
[data-testid="stSegmentedControl"] button:hover {
    background: #333333 !important;
}
/* Segmented control container */
[data-testid="stSegmentedControl"] {
    background: #2d2d2d !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 12px !important;
    padding: 3px !important;
}


[data-testid="stPlotlyChart"] {
    border: 3px solid #1a1a1a;
    border-radius: 16px;
    box-shadow: 5px 5px 0px #1a1a1a;
    background: #fff;
    padding: 8px;
}

/* ---------- DataFrames ---------- */
[data-testid="stDataFrame"] {
    border: 3px solid #1a1a1a;
    border-radius: 12px;
    box-shadow: 5px 5px 0px #1a1a1a;
    overflow: hidden;
}

/* ---------- Expander ---------- */
[data-testid="stExpander"] {
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 4px 4px 0px #1a1a1a !important;
    background: #fff !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary p {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] svg {
    fill: #1a1a1a !important;
    color: #1a1a1a !important;
}

/* ---------- Alerts ---------- */
.stAlert > div {
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
}

/* ---------- Divider ---------- */
hr { border: 2px solid #1a1a1a !important; }

/* ---------- Custom classes ---------- */
.neo-card {
    background: #fff; border: 3px solid #1a1a1a; border-radius: 16px;
    padding: 24px; box-shadow: 5px 5px 0px #1a1a1a; margin-bottom: 1.2rem; color: #1a1a1a !important;
}
.neo-card-yellow { background: #FFD600; border: 3px solid #1a1a1a; border-radius: 16px; padding: 24px; box-shadow: 5px 5px 0px #1a1a1a; margin-bottom: 1.2rem; }
.neo-card-green  { background: #7BF1A8; border: 3px solid #1a1a1a; border-radius: 16px; padding: 24px; box-shadow: 5px 5px 0px #1a1a1a; margin-bottom: 1.2rem; }
.neo-card-pink   { background: #FF6B9D; border: 3px solid #1a1a1a; border-radius: 16px; padding: 24px; box-shadow: 5px 5px 0px #1a1a1a; margin-bottom: 1.2rem; }
.neo-card-blue   { background: #88D4FF; border: 3px solid #1a1a1a; border-radius: 16px; padding: 24px; box-shadow: 5px 5px 0px #1a1a1a; margin-bottom: 1.2rem; }
.neo-card-purple { background: #C4B5FD; border: 3px solid #1a1a1a; border-radius: 16px; padding: 24px; box-shadow: 5px 5px 0px #1a1a1a; margin-bottom: 1.2rem; }

.neo-title    { font-weight: 700; font-size: 2.2rem; color: #1a1a1a; margin-bottom: .3rem; }
.neo-subtitle { font-weight: 500; font-size: 1rem; color: #4a4a4a; margin-bottom: 1rem; }

.neo-badge       { display:inline-block; background:#FFD600; border:2px solid #1a1a1a; border-radius:8px; padding:4px 12px; font-weight:600; font-size:.85rem; box-shadow:2px 2px 0 #1a1a1a; margin-right:6px; }
.neo-badge-green { display:inline-block; background:#7BF1A8; border:2px solid #1a1a1a; border-radius:8px; padding:4px 12px; font-weight:600; font-size:.85rem; box-shadow:2px 2px 0 #1a1a1a; margin-right:6px; }
.neo-badge-pink  { display:inline-block; background:#FF6B9D; color:#fff; border:2px solid #1a1a1a; border-radius:8px; padding:4px 12px; font-weight:600; font-size:.85rem; box-shadow:2px 2px 0 #1a1a1a; margin-right:6px; }

.flow-container { display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; margin:1.5rem 0; }
.flow-step {
    background:#fff; border:3px solid #1a1a1a; border-radius:16px;
    padding:14px 22px; box-shadow:4px 4px 0 #1a1a1a; text-align:center;
    font-weight:600; min-width:130px; transition:transform .15s;
}
.flow-step:hover { transform:translate(-2px,-2px); box-shadow:6px 6px 0 #1a1a1a; }
.flow-step-active { background:#FFD600; }
.flow-arrow { font-size:1.8rem; font-weight:700; color:#1a1a1a; }

.status-aman      { display:inline-block; background:#7BF1A8; border:2px solid #1a1a1a; border-radius:8px; padding:4px 14px; font-weight:700; box-shadow:2px 2px 0 #1a1a1a; }
.status-peringatan{ display:inline-block; background:#FFD600; border:2px solid #1a1a1a; border-radius:8px; padding:4px 14px; font-weight:700; box-shadow:2px 2px 0 #1a1a1a; }
.status-kritis    { display:inline-block; background:#FF6B9D; color:#fff; border:2px solid #1a1a1a; border-radius:8px; padding:4px 14px; font-weight:700; box-shadow:2px 2px 0 #1a1a1a; }

/* Scrollbar */
::-webkit-scrollbar       { width: 8px; }
::-webkit-scrollbar-track { background: #FFF8E7; }
::-webkit-scrollbar-thumb { background: #1a1a1a; border-radius: 4px; }

/* ========== NUCLEAR: force ALL text black ========== */
.stApp {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
/* Keep white text on pink badges/status */
.neo-badge-pink, .neo-badge-pink *,
.status-kritis, .status-kritis * {
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
}
/* Keep chart internals untouched */
.js-plotly-plot *, .plotly * {
    color: unset !important;
    -webkit-text-fill-color: unset !important;
}

/* ===== Pills (st.pills) — AFTER nuclear, lebih spesifik ===== */
.stApp [data-testid="stPills"] button,
.stApp [data-testid="stPills"] [role="option"] {
    background: #1a1a1a !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 999px !important;
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
    font-weight: 600 !important;
    padding: 5px 15px !important;
    transition: all 0.15s;
}
.stApp [data-testid="stPills"] button span,
.stApp [data-testid="stPills"] button p,
.stApp [data-testid="stPills"] button * {
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
}
.stApp [data-testid="stPills"] button[aria-checked="true"],
.stApp [data-testid="stPills"] button[aria-selected="true"],
.stApp [data-testid="stPills"] [role="option"][aria-selected="true"] {
    background: #FFD600 !important;
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    border-color: #1a1a1a !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
}
.stApp [data-testid="stPills"] button[aria-checked="true"] *,
.stApp [data-testid="stPills"] button[aria-selected="true"] *,
.stApp [data-testid="stPills"] [role="option"][aria-selected="true"] * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}

/* ===== Segmented Control (st.segmented_control) — AFTER nuclear ===== */
.stApp [data-testid="stSegmentedControl"] {
    background: #2d2d2d !important;
    border: 2px solid #1a1a1a !important;
    border-radius: 12px !important;
    padding: 3px !important;
}
.stApp [data-testid="stSegmentedControl"] button,
.stApp [data-testid="stSegmentedControl"] [role="radio"],
.stApp [data-testid="stSegmentedControl"] label {
    background: transparent !important;
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: all 0.15s;
}
.stApp [data-testid="stSegmentedControl"] button span,
.stApp [data-testid="stSegmentedControl"] button p,
.stApp [data-testid="stSegmentedControl"] button *,
.stApp [data-testid="stSegmentedControl"] [role="radio"] *,
.stApp [data-testid="stSegmentedControl"] label * {
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
}
.stApp [data-testid="stSegmentedControl"] button[aria-checked="true"],
.stApp [data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"],
.stApp [data-testid="stSegmentedControl"] button[data-selected="true"] {
    background: #FFD600 !important;
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    box-shadow: 2px 2px 0px #1a1a1a !important;
}
.stApp [data-testid="stSegmentedControl"] button[aria-checked="true"] *,
.stApp [data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"] *,
.stApp [data-testid="stSegmentedControl"] button[data-selected="true"] * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    """Memuat dan memperkaya CSV demand data."""
    file_path = "synthetic_demand_data.csv"
    if not os.path.exists(file_path):
        st.error(f"File data '{file_path}' tidak ditemukan!")
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    df["tanggal_permintaan"] = pd.to_datetime(df["tanggal_permintaan"])

    # Mapping komoditas sesuai schema.sql
    komoditas_map = {
        1: "GB Propunic", 
        2: "GB Profeed", 
        3: "GB Proquatic",
        4: "Pendawa Subur POC",
        5: "Compossap",
        6: "Agen Hayati [Trichogem / Methagem]"
    }
    df["nama_komoditas"] = (
        df["id_komoditas"].map(komoditas_map).fillna("Lainnya")
        if "id_komoditas" in df.columns
        else "Unknown"
    )
    return df

df = load_data()

# ============================================================
# LOAD MODEL & KONTRAK INFERENSI
# ============================================================
FITUR_INPUT = [
    'id_poktan', 'id_komoditas', 'harga_satuan_transaksi', 
    'curah_hujan_mm', 'lag_1w', 'lag_4w', 'lag_7w', 
    'rolling_mean_4w', 'fase_musim_Bera', 'fase_musim_Gadu', 'fase_musim_Rendeng'
]

@st.cache_resource
def load_model():
    """Memuat model ML secara otomatis"""
    # Cek model_demand.pkl terlebih dahulu, lalu pipeline.pkl
    for path in ["model_demand.pkl", "pipeline.pkl"]:
        if os.path.exists(path):
            try:
                obj = joblib.load(path)
            except Exception:
                continue
            # Jika file pkl berupa dictionary yang menyimpan objek model
            if isinstance(obj, dict):
                return obj.get("model", None)
            return obj
    return None

model = load_model()


@st.cache_resource
def get_predictor():
    return DemandPredictor()

predictor = get_predictor()

# ============================================================
# CHART HELPERS (Neo-Brutalism palette)
# ============================================================
NB_MUSIM   = {"Rendeng": "#FFD600", "Gadu": "#7BF1A8", "Bera": "#88D4FF"}
NB_KOMOD   = {
    "GB Propunic": "#FFD600", 
    "GB Profeed": "#7BF1A8", 
    "GB Proquatic": "#FF6B9D",
    "Pendawa Subur POC": "#88D4FF",
    "Compossap": "#C4B5FD",
    "Agen Hayati [Trichogem / Methagem]": "#FFA07A"
}
NB_PALETTE = ["#FFD600", "#7BF1A8", "#FF6B9D", "#88D4FF", "#C4B5FD", "#FFA07A"]

KOMODITAS_ICONS = {
    "GB Propunic": "💧", 
    "GB Profeed": "🐄", 
    "GB Proquatic": "🐟",
    "Pendawa Subur POC": "🌿",
    "Compossap": "🪨",
    "Agen Hayati [Trichogem / Methagem]": "🛡️"
}

UNIT_PRODUK = {
    "GB Propunic": "Liter",
    "GB Profeed": "Liter",
    "GB Proquatic": "Liter",
    "Pendawa Subur POC": "Liter",
    "Compossap": "Zak",
    "Agen Hayati [Trichogem / Methagem]": "Saset/Kg",
}

STOK_MOCK = {
    "GB Propunic":  {"stok": 150.0, "threshold": 100.0, "masa_simpan": 180, "sisa_hari": 120},
    "GB Profeed": {"stok": 80.0,  "threshold": 50.0,  "masa_simpan": 120, "sisa_hari": 45},
    "GB Proquatic":{"stok": 20.0,  "threshold": 30.0,  "masa_simpan": 90,  "sisa_hari": 15},
    "Pendawa Subur POC":{"stok": 50.0,  "threshold": 40.0,  "masa_simpan": 90,  "sisa_hari": 30},
    "Compossap":{"stok": 60.0,  "threshold": 40.0,  "masa_simpan": 90,  "sisa_hari": 30},
    "Agen Hayati [Trichogem / Methagem]":{"stok": 30.0,  "threshold": 20.0,  "masa_simpan": 90,  "sisa_hari": 30},
}
STOK_DEFAULT = {"stok": 50.0, "threshold": 40.0, "masa_simpan": 90, "sisa_hari": 30}

def nb_layout(fig, title="", x_title="", y_title=""):
    """Terapkan Neo-Brutalism layout ke figure Plotly."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family="Space Grotesk, sans-serif", size=20, color="#1a1a1a"),
            x=0.02,
        ),
        font=dict(family="Space Grotesk, sans-serif", size=13, color="#1a1a1a"),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="#FFFFFF",
        legend=dict(
            bgcolor="#FFFFFF", bordercolor="#1a1a1a", borderwidth=2,
            font=dict(family="Space Grotesk, sans-serif", size=12, color="#1a1a1a"),
            title=dict(font=dict(family="Space Grotesk, sans-serif", size=12, color="#1a1a1a")),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        ),
        margin=dict(l=50, r=30, t=80, b=60),
        hoverlabel=dict(
            bgcolor="#FFD600", bordercolor="#1a1a1a",
            font=dict(family="Space Grotesk", size=13, color="#1a1a1a"),
        ),
    )
    fig.update_xaxes(
        showgrid=True, gridcolor="#E8E8E8", gridwidth=1,
        linecolor="#1a1a1a", linewidth=2,
        title_text=x_title, title_font=dict(size=13, color="#1a1a1a"),
        tickfont=dict(size=11, color="#1a1a1a"),
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="#E8E8E8", gridwidth=1,
        linecolor="#1a1a1a", linewidth=2,
        title_text=y_title, title_font=dict(size=13, color="#1a1a1a"),
        tickfont=dict(size=11, color="#1a1a1a"),
    )
    return fig

# ============================================================
# SIDEBAR — PANEL PARAMETER
# ============================================================
st.sidebar.markdown("""
<div style="text-align:center; margin-bottom:.8rem;">
    <span style="font-size:3rem;">🌾</span>
    <div class="neo-title" style="font-size:1.5rem; margin-top:.4rem;">Panel Parameter</div>
    <div class="neo-subtitle" style="font-size:.85rem;">Filter data & simulasi input prediksi</div>
</div>
""", unsafe_allow_html=True)

# --- defaults ---
selected_komoditas = []
selected_musim     = []
simulasi_harga     = 0.0
jalur_penjualan    = []
filtered_df        = pd.DataFrame()

if "prediction_requested" not in st.session_state:
    st.session_state.prediction_requested = False

if not df.empty:
    # Komoditas
    st.sidebar.markdown("### 🌾 Komoditas")
    komoditas_list = list(KOMODITAS_ICONS.keys())
    selected_komoditas = st.sidebar.multiselect(
        "Pilih Komoditas", komoditas_list, default=komoditas_list, label_visibility="collapsed"
    )

    # Jalur penjualan menjadi bagian dari kontrak input Sprint 2.
    st.sidebar.markdown("### 🛒 Jalur Penjualan")
    jalur_penjualan = st.sidebar.multiselect(
        "Pilih Jalur Penjualan",
        ["Wholesale (Grosir)", "E-commerce Retail (Eceran)"],
        default=[],
        max_selections=1,
        placeholder="Pilih jalur penjualan...",
        label_visibility="collapsed",
    )

    # Fase Musim
    st.sidebar.markdown("### 🌦️ Fase Musim")
    musim_list = (
        sorted(df["fase_musim"].unique().tolist())
        if "fase_musim" in df.columns
        else ["Rendeng", "Gadu", "Bera"]
    )
    selected_musim = st.sidebar.multiselect(
        "Pilih Fase Musim", musim_list, default=musim_list, label_visibility="collapsed"
    )

    # Date range
    st.sidebar.markdown("### 📅 Rentang Tanggal")
    min_date = df["tanggal_permintaan"].min().date()
    max_date = df["tanggal_permintaan"].max().date()
    date_range = st.sidebar.date_input(
        "Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")

    # Slider harga (what-if)
    st.sidebar.markdown("### 💰 Simulasi Harga")
    min_h = float(df["harga_satuan_transaksi"].min())
    max_h = float(df["harga_satuan_transaksi"].max())
    mean_h = float(df["harga_satuan_transaksi"].mean())
    lo = int((min_h * 0.5) // 1000 * 1000)
    hi = int((max_h * 1.5) // 1000 * 1000)
    mid = int(mean_h // 1000 * 1000)
    if hi <= lo:
        hi = lo + 1000

    simulasi_harga = st.sidebar.slider(
        "Harga Transaksi (Rp)", lo, hi, mid, step=1000, label_visibility="collapsed"
    )
    st.sidebar.markdown(
        f"""
        <div class="neo-card" style="text-align:center; padding:12px;">
            <div style="font-size:.8rem; font-weight:600;">HARGA SIMULASI</div>
            <div style="font-size:1.4rem; font-weight:700;">Rp {simulasi_harga:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    prediksi_diklik = st.sidebar.button("🔮 Prediksi", type="primary", use_container_width=True)
    if prediksi_diklik:
        validation_errors = []
        if not selected_komoditas:
            validation_errors.append("pilih minimal satu produk")
        if not jalur_penjualan:
            validation_errors.append("pilih jalur penjualan")
        if not isinstance(date_range, tuple) or len(date_range) != 2:
            validation_errors.append("lengkapi rentang tanggal")

        if validation_errors:
            st.session_state.prediction_requested = False
            st.sidebar.error("Harap " + ", ".join(validation_errors) + ".")
        else:
            st.session_state.prediction_requested = True
            st.sidebar.success("Input valid. Prediksi berhasil dibuat.")

    # Apply filters
    filtered_df = df[
        df["nama_komoditas"].isin(selected_komoditas)
        & df["fase_musim"].isin(selected_musim)
    ]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        s, e = date_range
        filtered_df = filtered_df[
            (filtered_df["tanggal_permintaan"].dt.date >= s)
            & (filtered_df["tanggal_permintaan"].dt.date <= e)
        ]
else:
    st.sidebar.warning("Data tidak tersedia.")

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="neo-title">🌾 Dasbor Prediksi Produksi Pertanian</div>
<div class="neo-subtitle">Prototipe UI Capstone Cangkringan ML — Sprint 3</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard Historis",
    "🔮 Simulasi & Prediksi",
    "📦 Manajemen Stok",
    "📊 Rekomendasi Produksi (DSS)",
    "📚 Panduan Literasi Digital",
])

# ============================================================
# TAB 1 — DASHBOARD HISTORIS
# ============================================================
with tab1:
    if not filtered_df.empty:
        # --- KPI row ---
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Total Transaksi", f"{len(filtered_df):,}")
        total_nilai = (
            filtered_df["volume_permintaan"]
            * filtered_df["harga_satuan_transaksi"]
        ).sum()
        c2.metric("💰 Total Nilai Estimasi", f"Rp {total_nilai:,.0f}")
        c3.metric("💰 Rata-rata Harga", f"Rp {filtered_df['harga_satuan_transaksi'].mean():,.0f}")
        c4.metric("🌧️ Curah Hujan", f"{filtered_df['curah_hujan_mm'].mean():,.1f} mm")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Row: trend + bar ---
        left, right = st.columns([3, 2])

        with left:
            trend = (
                filtered_df
                .groupby([pd.Grouper(key="tanggal_permintaan", freq="ME"), "nama_komoditas"])["volume_permintaan"]
                .sum()
                .reset_index()
            )
            trend["Satuan"] = trend["nama_komoditas"].map(UNIT_PRODUK)
            fig = px.area(
                trend, x="tanggal_permintaan", y="volume_permintaan",
                color="nama_komoditas", color_discrete_map=NB_KOMOD,
                markers=True, facet_row="Satuan"
            )
            fig.update_traces(
                line_width=3,
                marker=dict(size=7, line=dict(width=2, color="#1a1a1a")),
                fillcolor=None,  # let plotly auto-fill with opacity
            )
            # Make area fills semi-transparent
            for trace in fig.data:
                hex_c = trace.line.color or "#FFD600"
                trace.fillcolor = hex_c.replace(")", ",0.15)").replace("rgb", "rgba") if "rgb" in str(hex_c) else None
            
            fig.update_yaxes(matches=None, showticklabels=True)
            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            nb_layout(fig, "📈 Tren Volume Permintaan", x_title="Bulan", y_title="Volume")
            fig.update_layout(height=550)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with right:
            vol = filtered_df.groupby("nama_komoditas")["volume_permintaan"].sum().reset_index()
            vol["Satuan"] = vol["nama_komoditas"].map(UNIT_PRODUK)
            vol = vol.sort_values(["volume_permintaan"], ascending=True)
            fig = px.bar(
                vol, y="nama_komoditas", x="volume_permintaan",
                color="nama_komoditas", color_discrete_map=NB_KOMOD,
                orientation="h", text="volume_permintaan",
                facet_row="Satuan"
            )
            fig.update_traces(
                marker_line_color="#1a1a1a", marker_line_width=2,
                texttemplate="%{text:,.0f}", textposition="outside",
                textfont=dict(family="Space Grotesk", size=13, color="#1a1a1a"),
            )
            fig.update_xaxes(matches=None, showticklabels=True)
            fig.update_yaxes(matches=None, showticklabels=True)
            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            fig.update_layout(showlegend=False)
            nb_layout(fig, "📊 Volume per Komoditas", x_title="Volume", y_title="")
            fig.update_layout(height=550)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Row: donut + scatter ---
        left2, right2 = st.columns([2, 3])

        with left2:
            mcount = filtered_df.groupby("fase_musim")["volume_permintaan"].sum().reset_index()
            fig = px.pie(
                mcount, values="volume_permintaan", names="fase_musim",
                color="fase_musim", color_discrete_map=NB_MUSIM, hole=0.45,
            )
            fig.update_traces(
                textinfo="label+percent",
                textfont=dict(family="Space Grotesk", size=14, color="#1a1a1a"),
                marker_line=dict(color="#1a1a1a", width=2.5),
                pull=[0.03, 0.03, 0.03],
            )
            nb_layout(fig, "🌦️ Distribusi Volume per Musim")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with right2:
            # Header & Mode Switcher
            r_head1, r_head2 = st.columns([1, 1])
            with r_head1:
                st.markdown('<div style="font-size:1.1rem; font-weight:700; color:#1a1a1a; padding-top:4px;">💰 Analisis Harga & Permintaan</div>', unsafe_allow_html=True)
            with r_head2:
                chart_view = st.pills(
                    "Mode Tampilan",
                    options=["🎯 Sebaran & Korelasi", "📅 Tren Bulanan (Dual-Axis)", "📦 Sebaran Boxplot"],
                    default="🎯 Sebaran & Korelasi",
                    label_visibility="collapsed"
                )

            if chart_view == "🎯 Sebaran & Korelasi":
                avail_komod = [k for k in ["GB Propunic", "GB Profeed", "GB Proquatic", "Pendawa Subur POC", "Compossap", "Agen Hayati [Trichogem / Methagem]"] if k in filtered_df["nama_komoditas"].unique()]
                
                if len(avail_komod) > 1:
                    fokus_opts = ["📊 Bandingkan Semua (Subplot)"] + [f"📦 {k}" for k in avail_komod]
                    sel_fokus = st.segmented_control(
                        "Fokus Komoditas:",
                        options=fokus_opts,
                        default="📊 Bandingkan Semua (Subplot)",
                        label_visibility="collapsed"
                    )
                elif len(avail_komod) == 1:
                    sel_fokus = f"📦 {avail_komod[0]}"
                else:
                    sel_fokus = None

                if sel_fokus == "📊 Bandingkan Semua (Subplot)":
                    cols_count = len(avail_komod)
                    fig_sub = make_subplots(
                        rows=1, cols=cols_count,
                        subplot_titles=[f"<b>📦 {k}</b>" for k in avail_komod],
                        horizontal_spacing=0.07
                    )
                    for idx, k in enumerate(avail_komod, 1):
                        sub_data = filtered_df[filtered_df["nama_komoditas"] == k]
                        # Scatter points
                        fig_sub.add_trace(
                            go.Scatter(
                                x=sub_data["harga_satuan_transaksi"],
                                y=sub_data["volume_permintaan"],
                                mode="markers",
                                marker=dict(
                                    size=7,
                                    color=NB_KOMOD.get(k, "#FFD600"),
                                    line=dict(width=1.2, color="#1a1a1a"),
                                    opacity=0.75
                                ),
                                customdata=np.stack((sub_data["fase_musim"], sub_data["curah_hujan_mm"]), axis=-1),
                                hovertemplate=(
                                    "<b>" + k + "</b> (%{customdata[0]})<br>"
                                    "Harga: Rp %{x:,.0f}<br>"
                                    "Volume: %{y:,.1f} Unit Produk<br>"
                                    "Hujan: %{customdata[1]:.1f} mm<extra></extra>"
                                ),
                                name=k,
                                showlegend=False
                            ),
                            row=1, col=idx
                        )
                        # Trendline
                        if len(sub_data) > 1:
                            z = np.polyfit(sub_data["harga_satuan_transaksi"], sub_data["volume_permintaan"], 1)
                            p = np.poly1d(z)
                            x_min = sub_data["harga_satuan_transaksi"].min()
                            x_max = sub_data["harga_satuan_transaksi"].max()
                            x_line = np.linspace(x_min, x_max, 40)
                            fig_sub.add_trace(
                                go.Scatter(
                                    x=x_line, y=p(x_line),
                                    mode="lines",
                                    line=dict(color="#1a1a1a", width=2.5, dash="dot"),
                                    name=f"Tren {k}",
                                    showlegend=False,
                                    hoverinfo="skip"
                                ),
                                row=1, col=idx
                            )
                        fig_sub.update_xaxes(
                            title_text="Harga (Rp)", row=1, col=idx,
                            showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2,
                            tickfont=dict(size=10, color="#1a1a1a"), title_font=dict(size=11, color="#1a1a1a")
                        )
                        fig_sub.update_yaxes(
                            title_text="Volume (Unit Produk)" if idx == 1 else "", row=1, col=idx,
                            showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2,
                            tickfont=dict(size=10, color="#1a1a1a"), title_font=dict(size=11, color="#1a1a1a")
                        )

                    fig_sub.update_layout(
                        height=360,
                        plot_bgcolor="#FAFAFA",
                        paper_bgcolor="#FFFFFF",
                        margin=dict(l=40, r=20, t=40, b=45),
                        font=dict(family="Space Grotesk, sans-serif", size=12, color="#1a1a1a"),
                        hoverlabel=dict(bgcolor="#FFD600", bordercolor="#1a1a1a", font=dict(family="Space Grotesk", color="#1a1a1a"))
                    )
                    st.plotly_chart(fig_sub, use_container_width=True, config={"displayModeBar": False})

                elif sel_fokus:
                    clean_k = sel_fokus.split()[-1]
                    sub_data = filtered_df[filtered_df["nama_komoditas"] == clean_k]
                    if not sub_data.empty:
                        fig_single = px.scatter(
                            sub_data, x="harga_satuan_transaksi", y="volume_permintaan",
                            color="fase_musim", color_discrete_map=NB_MUSIM,
                            marginal_x="box", marginal_y="box",
                            hover_data={
                                "harga_satuan_transaksi": ":.0f",
                                "volume_permintaan": ":.1f",
                                "curah_hujan_mm": ":.1f"
                            }
                        )
                        fig_single.update_traces(
                            marker=dict(size=9, line=dict(width=1.5, color="#1a1a1a"), opacity=0.8)
                        )
                        if len(sub_data) > 1:
                            z = np.polyfit(sub_data["harga_satuan_transaksi"], sub_data["volume_permintaan"], 1)
                            p = np.poly1d(z)
                            x_line = np.linspace(sub_data["harga_satuan_transaksi"].min(), sub_data["harga_satuan_transaksi"].max(), 50)
                            fig_single.add_scatter(
                                x=x_line, y=p(x_line),
                                mode="lines",
                                line=dict(color="#1a1a1a", width=3, dash="dash"),
                                name="Garis Tren",
                                hoverinfo="skip"
                            )
                        nb_layout(fig_single, f"💰 Sebaran & Distribusi {clean_k}", x_title="Harga Satuan (Rp)", y_title="Volume (Unit Produk)")
                        fig_single.update_layout(height=360)
                        st.plotly_chart(fig_single, use_container_width=True, config={"displayModeBar": False})
                        
                        # Mini metrics badge
                        corr_val = sub_data["harga_satuan_transaksi"].corr(sub_data["volume_permintaan"])
                        st.markdown(f"""
                        <div style="display:flex; gap:10px; justify-content:center; font-size:0.85rem; font-weight:600; color:#1a1a1a; margin-top:-5px;">
                            <span class="neo-card" style="padding:4px 12px; margin:0;">💰 Rata-rata: <b>Rp {sub_data['harga_satuan_transaksi'].mean():,.0f}</b></span>
                            <span class="neo-card" style="padding:4px 12px; margin:0;">📦 Volume: <b>{sub_data['volume_permintaan'].mean():,.1f} Unit Produk</b></span>
                            <span class="neo-card" style="padding:4px 12px; margin:0;">📈 Korelasi (r): <b>{corr_val:.3f}</b></span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(f"Tidak ada data untuk {clean_k}.")

            elif chart_view == "📅 Tren Bulanan (Dual-Axis)":
                monthly = (
                    filtered_df
                    .groupby(pd.Grouper(key="tanggal_permintaan", freq="MS"))
                    .agg(vol=("volume_permintaan", "sum"), harga=("harga_satuan_transaksi", "mean"))
                    .reset_index()
                )
                fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
                fig_dual.add_trace(
                    go.Bar(
                        x=monthly["tanggal_permintaan"], y=monthly["vol"],
                        name="Total Volume (Unit Produk)",
                        marker_color="#FFD600", marker_line_color="#1a1a1a", marker_line_width=2,
                        hovertemplate="<b>%{x|%b %Y}</b><br>Volume: %{y:,.1f} Unit Produk<extra></extra>"
                    ),
                    secondary_y=False
                )
                fig_dual.add_trace(
                    go.Scatter(
                        x=monthly["tanggal_permintaan"], y=monthly["harga"],
                        name="Rata-rata Harga (Rp)",
                        mode="lines+markers",
                        line=dict(color="#FF6B9D", width=3.5),
                        marker=dict(size=9, color="#FF6B9D", line=dict(width=2, color="#1a1a1a")),
                        hovertemplate="<b>%{x|%b %Y}</b><br>Harga: Rp %{y:,.0f}<extra></extra>"
                    ),
                    secondary_y=True
                )
                fig_dual.update_xaxes(showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2, tickfont=dict(color="#1a1a1a"))
                fig_dual.update_yaxes(title_text="Volume (Unit Produk)", showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2, secondary_y=False, tickfont=dict(color="#1a1a1a"))
                fig_dual.update_yaxes(title_text="Harga Satuan (Rp)", showgrid=False, linecolor="#1a1a1a", linewidth=2, secondary_y=True, tickfont=dict(color="#1a1a1a"))
                fig_dual.update_layout(
                    title=dict(text="<b>📅 Tren Dinamika: Volume vs Harga Bulanan</b>", font=dict(family="Space Grotesk, sans-serif", size=16, color="#1a1a1a")),
                    height=360, plot_bgcolor="#FAFAFA", paper_bgcolor="#FFFFFF",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="#FFFFFF", bordercolor="#1a1a1a", borderwidth=2, font=dict(color="#1a1a1a")),
                    margin=dict(l=45, r=45, t=65, b=45),
                    hoverlabel=dict(bgcolor="#FFD600", bordercolor="#1a1a1a", font=dict(family="Space Grotesk", color="#1a1a1a"))
                )
                st.plotly_chart(fig_dual, use_container_width=True, config={"displayModeBar": False})

            elif chart_view == "📦 Sebaran Boxplot":
                avail_komod = [k for k in ["GB Propunic", "GB Profeed", "GB Proquatic", "Pendawa Subur POC", "Compossap", "Agen Hayati [Trichogem / Methagem]"] if k in filtered_df["nama_komoditas"].unique()]
                fig_box = make_subplots(rows=1, cols=2, subplot_titles=["<b>💰 Sebaran Harga (Rp)</b>", "<b>📦 Sebaran Volume (Unit Produk)</b>"], horizontal_spacing=0.1)
                for komod in avail_komod:
                    sub = filtered_df[filtered_df["nama_komoditas"] == komod]
                    fig_box.add_trace(
                        go.Box(
                            y=sub["harga_satuan_transaksi"], name=komod,
                            marker_color=NB_KOMOD.get(komod, "#FFD600"),
                            line=dict(color="#1a1a1a", width=2),
                            boxpoints="outliers"
                        ),
                        row=1, col=1
                    )
                    fig_box.add_trace(
                        go.Box(
                            y=sub["volume_permintaan"], name=komod,
                            marker_color=NB_KOMOD.get(komod, "#FFD600"),
                            line=dict(color="#1a1a1a", width=2),
                            boxpoints="outliers",
                            showlegend=False
                        ),
                        row=1, col=2
                    )
                fig_box.update_xaxes(showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2, tickfont=dict(color="#1a1a1a"))
                fig_box.update_yaxes(showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2, tickfont=dict(color="#1a1a1a"))
                fig_box.update_layout(
                    height=360, plot_bgcolor="#FAFAFA", paper_bgcolor="#FFFFFF",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="#FFFFFF", bordercolor="#1a1a1a", borderwidth=2, font=dict(color="#1a1a1a")),
                    margin=dict(l=45, r=25, t=65, b=45),
                    hoverlabel=dict(bgcolor="#FFD600", bordercolor="#1a1a1a", font=dict(family="Space Grotesk", color="#1a1a1a"))
                )
                st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

        # --- Data table ---
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 Lihat Sampel Data", expanded=False):
            show = filtered_df[
                ["tanggal_permintaan", "nama_komoditas", "volume_permintaan",
                 "harga_satuan_transaksi", "fase_musim", "curah_hujan_mm"]
            ].copy()
            show.columns = ["Tanggal", "Komoditas", "Volume (Unit Produk)", "Harga (Rp)", "Fase Musim", "Curah Hujan (mm)"]
            st.dataframe(show.head(20), use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="neo-card-yellow" style="text-align:center;">
            <span style="font-size:3rem;">📊</span><br>
            <b style="font-size:1.1rem;">Pilih filter di sidebar untuk melihat data historis</b>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PREDICTION DATA — dipakai oleh Tab 2 (inferensi) dan Tab 4 (DSS)
# ============================================================
if "pred_df" not in st.session_state:
    st.session_state.pred_df = pd.DataFrame()

st.session_state.pred_df = pd.DataFrame()

if selected_komoditas and st.session_state.prediction_requested:
    pred_rows = []
    historical_df = filtered_df if not filtered_df.empty else df
    
    # Mapping nama komoditas ke ID (sesuai schema)
    komoditas_id_map = {
        "GB Propunic": 1,
        "GB Profeed": 2,
        "GB Proquatic": 3,
        "Pendawa Subur POC": 4,
        "Compossap": 5,
        "Agen Hayati [Trichogem / Methagem]": 6
    }

    selected_channel = jalur_penjualan[0]
    selected_season = selected_musim[0] if selected_musim else "Rendeng"

    for k in selected_komoditas:
        sku_history = historical_df[historical_df["nama_komoditas"] == k]
        
        # Ambil baseline dari data historis
        base_demand = float(sku_history["volume_permintaan"].mean()) if not sku_history.empty else 100.0
        curah_hujan_avg = float(sku_history["curah_hujan_mm"].mean()) if not sku_history.empty else 150.0
        
        raw_input = [{
            'id_poktan': 1,
            'id_komoditas': komoditas_id_map.get(k, 0),
            'harga_satuan_transaksi': simulasi_harga,
            'curah_hujan_mm': curah_hujan_avg,
            'lag_1w': base_demand,
            'lag_4w': base_demand,
            'lag_7w': base_demand,
            'rolling_mean_4w': base_demand,
            'fase_musim': selected_season
        }]
        demand = predictor.predict(raw_input)
            
        buf = round(demand * 0.15, 1)
        stok_aktif = STOK_MOCK.get(k, STOK_DEFAULT)["stok"]
        rekomendasi = max(0.0, round(demand - stok_aktif + buf, 1))
        
        pred_rows.append({
            "Komoditas": k,
            "Unit": UNIT_PRODUK.get(k, "Unit Produk"),
            "Jalur Penjualan": selected_channel,
            "Prediksi Permintaan": demand,
            "Rekomendasi Produksi": rekomendasi,
            "Safety Buffer": buf,
        })
        
    st.session_state.pred_df = pd.DataFrame(pred_rows)

# TAB 2 — SIMULASI & PREDIKSI (WHAT-IF)
# ============================================================
with tab2:
    # --- Flow diagram ---
    st.markdown("""
    <div class="neo-card" style="margin-bottom:1.5rem;">
        <div style="text-align:center; margin-bottom:.8rem;">
            <span class="neo-badge">SPRINT 3 — MOCKUP ALUR INFERENSI</span>
        </div>
        <div class="flow-container">
            <div class="flow-step flow-step-active">
                <div style="font-size:1.4rem;">🎛️</div>
                <div>Input Parameter</div>
                <div style="font-size:.7rem; color:#666;">Harga · Musim · Komoditas</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
                <div style="font-size:1.4rem;">⚙️</div>
                <div>Proses ETL</div>
                <div style="font-size:.7rem; color:#666;">Cleaning & Transform</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
                <div style="font-size:1.4rem;">🧠</div>
                <div>Model ML</div>
                <div style="font-size:.7rem; color:#666;">Sprint 3 🔓</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step flow-step-active">
                <div style="font-size:1.4rem;">📊</div>
                <div>Rekomendasi</div>
                <div style="font-size:.7rem; color:#666;">Produksi + Buffer</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Parameter cards ---
    p1, p2, p3 = st.columns(3)
    p1.markdown(f"""
    <div class="neo-card-yellow" style="text-align:center;">
        <div style="font-size:2rem;">💰</div>
        <div style="font-weight:600; font-size:.85rem;">Harga Simulasi</div>
        <div style="font-weight:700; font-size:1.4rem;">Rp {simulasi_harga:,.0f}</div>
    </div>""", unsafe_allow_html=True)
    p2.markdown(f"""
    <div class="neo-card-green" style="text-align:center;">
        <div style="font-size:2rem;">🌦️</div>
        <div style="font-weight:600; font-size:.85rem;">Fase Musim Aktif</div>
        <div style="font-weight:700; font-size:1.05rem;">{', '.join(selected_musim) or 'Belum Dipilih'}</div>
    </div>""", unsafe_allow_html=True)
    p3.markdown(f"""
    <div class="neo-card-blue" style="text-align:center;">
        <div style="font-size:2rem;">🌾</div>
        <div style="font-weight:600; font-size:.85rem;">Komoditas Terpilih</div>
        <div style="font-weight:700; font-size:1.05rem;">{', '.join(selected_komoditas) or 'Belum Dipilih'}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="neo-card-green" style="padding:14px;">
        <b>✅ Model Machine Learning (XGBoost) Aktif</b><br>
        Visualisasi di bawah merupakan hasil prediksi demand berdasarkan parameter input sidebar.
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Prediction chart ---
    if selected_komoditas and st.session_state.prediction_requested:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Prediksi Permintaan", x=st.session_state.pred_df["Komoditas"],
            y=st.session_state.pred_df["Prediksi Permintaan"],
            text=st.session_state.pred_df["Prediksi Permintaan"].map(lambda value: f"{value:.1f}"),
            textposition="outside",
            marker_color=[NB_KOMOD.get(name, "#88D4FF") for name in st.session_state.pred_df["Komoditas"]],
            marker_line_color="#1a1a1a", marker_line_width=2,
            hovertemplate="<b>%{x}</b><br>Demand: %{y:.1f}<extra></extra>",
            error_y=dict(type='percent', value=5),
        ))
        nb_layout(fig, f"Estimasi Demand pada Harga Rp {simulasi_harga:,.0f}", y_title="Demand (satuan produk)")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("Grafik ini menampilkan hasil inferensi demand. Pita error (±5%) merupakan hampiran (approximation) visual untuk 95% Confidence Interval. Rekomendasi produksi tersedia di Tab 4.")
    else:
        st.markdown("""
        <div class="neo-card-yellow" style="text-align:center;">
            <span style="font-size:3rem;">🔮</span><br>
            <b>Pilih minimal satu komoditas di sidebar untuk melihat simulasi</b>
        </div>""", unsafe_allow_html=True)

# ============================================================
# TAB 3 — MANAJEMEN STOK GUDANG
# ============================================================
with tab3:
    st.markdown("""
    <div class="neo-card" style="padding:14px;">
        <b>📦 Prototipe Pemantauan Stok Gudang</b><br>
        Sinkronisasi dengan <i>Masa Simpan Hari</i> — fitur penurunan mutu mikroba (sesuai schema.sql).
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if selected_komoditas:
        # --- Status cards ---
        for i in range(0, len(selected_komoditas), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(selected_komoditas):
                    k = selected_komoditas[i + j]
                    d = STOK_MOCK.get(k, STOK_DEFAULT)
                    unit = UNIT_PRODUK.get(k, "Unit Produk")
                    ratio = d["stok"] / d["threshold"]
                    if ratio >= 1.2:
                        status, cls, emoji = "Aman", "status-aman", "✅"
                        card = "neo-card-green"
                    elif ratio >= 1.0:
                        status, cls, emoji = "Peringatan", "status-peringatan", "⚠️"
                        card = "neo-card-yellow"
                    else:
                        status, cls, emoji = "Kritis", "status-kritis", "🚨"
                        card = "neo-card-pink"

                    ico = KOMODITAS_ICONS.get(k, "🌱")

                    with cols[j]:
                        st.markdown(f"""
                        <div class="{card}" style="text-align:center;">
                            <div style="font-size:2.5rem;">{ico}</div>
                            <div style="font-weight:700; font-size:1.3rem; margin:6px 0;">{k}</div>
                            <div class="{cls}">{emoji} {status}</div>
                            <div style="margin-top:14px;">
                                <div style="font-size:.78rem; color:#333;">Stok Aktual</div>
                                <div style="font-weight:700; font-size:1.7rem;">{d['stok']} {unit}</div>
                            </div>
                            <div style="margin-top:6px;">
                                <div style="font-size:.78rem; color:#333;">Threshold Min.</div>
                                <div style="font-weight:700; font-size:1.15rem;">{d['threshold']} {unit}</div>
                            </div>
                            <div style="margin-top:6px;">
                                <div style="font-size:.78rem; color:#333;">Sisa Masa Simpan</div>
                                <div style="font-weight:700; font-size:1.15rem;">{d['sisa_hari']} hari</div>
                            </div>
                        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Gauge charts ---
        for i in range(0, len(selected_komoditas), 3):
            gcols = st.columns(3)
            for j in range(3):
                if i + j < len(selected_komoditas):
                    k = selected_komoditas[i + j]
                    d = STOK_MOCK.get(k, STOK_DEFAULT)
                    pct = d["sisa_hari"] / d["masa_simpan"]
                    g_color = "#7BF1A8" if pct > 0.6 else "#FFD600" if pct > 0.3 else "#FF6B9D"

                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=d["sisa_hari"],
                        number=dict(suffix=" hari", font=dict(family="Space Grotesk", size=22, color="#1a1a1a")),
                        delta=dict(reference=d["masa_simpan"], relative=True, valueformat=".0%"),
                        gauge=dict(
                            axis=dict(range=[0, d["masa_simpan"]], tickcolor="#1a1a1a"),
                            bar=dict(color=g_color, line=dict(color="#1a1a1a", width=2)),
                            bgcolor="#FFFFFF",
                            bordercolor="#1a1a1a", borderwidth=2,
                            steps=[
                                dict(range=[0, d["masa_simpan"] * 0.3], color="#FFE4E8"),
                                dict(range=[d["masa_simpan"] * 0.3, d["masa_simpan"] * 0.6], color="#FFF8DC"),
                                dict(range=[d["masa_simpan"] * 0.6, d["masa_simpan"]], color="#E8FFF0"),
                            ],
                        ),
                    ))
                    nb_layout(fig, f"Masa Simpan — {k}")
                    fig.update_layout(height=270, margin=dict(t=55, b=15, l=25, r=25))
                    with gcols[j]:
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # --- Alerts ---
        kritis  = [k for k in selected_komoditas if STOK_MOCK.get(k, STOK_DEFAULT)["stok"] < STOK_MOCK.get(k, STOK_DEFAULT)["threshold"]]
        expiring = [k for k in selected_komoditas if STOK_MOCK.get(k, STOK_DEFAULT)["sisa_hari"] < 30 and k not in kritis]

        if kritis:
            st.markdown(f"""
            <div class="neo-card-pink" style="padding:14px;">
                <b>🚨 PERINGATAN KRITIS:</b> Stok <b>{', '.join(kritis)}</b> di bawah threshold minimum!
                Segera lakukan penambahan stok produksi.
            </div>""", unsafe_allow_html=True)
        if expiring:
            st.markdown(f"""
            <div class="neo-card-yellow" style="padding:14px;">
                <b>⚠️ PERHATIAN:</b> Komoditas <b>{', '.join(expiring)}</b> mendekati batas masa simpan.
                Prioritaskan distribusi untuk menghindari penurunan mutu.
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="neo-card-yellow" style="text-align:center;">
            <span style="font-size:3rem;">📦</span><br>
            <b>Pilih komoditas di sidebar untuk melihat data stok</b>
        </div>""", unsafe_allow_html=True)

# ============================================================
# TAB 4 — REKOMENDASI PRODUKSI (DSS)
# ============================================================
with tab4:
    st.markdown("""
    <div class="neo-card-green" style="padding:14px;">
        <b>📊 Rekomendasi Produksi (DSS)</b><br>
        Formula: <i>Demand - Stok + Safety Buffer</i>, dengan safety buffer 15% dari demand.
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.pred_df.empty:
        st.dataframe(
            st.session_state.pred_df[["Komoditas", "Unit", "Jalur Penjualan", "Prediksi Permintaan", "Safety Buffer", "Rekomendasi Produksi"]],
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        for i in range(0, len(st.session_state.pred_df), 3):
            dss_cols = st.columns(3)
            for j in range(3):
                if i + j < len(st.session_state.pred_df):
                    row = st.session_state.pred_df.iloc[i + j]
                    ico = KOMODITAS_ICONS.get(row["Komoditas"], "🌱")
                    with dss_cols[j]:
                        st.markdown(f"""
                        <div class="neo-card" style="padding:14px; text-align:center;">
                            <div style="font-size:2rem;">{ico}</div>
                            <div style="font-weight:700;">{row['Komoditas']}</div>
                            <div style="font-size:.75rem; margin-top:6px;">{row['Jalur Penjualan']}</div>
                            <div style="font-size:.8rem; margin-top:8px;">Produksi yang disarankan</div>
                            <div style="font-size:1.35rem; font-weight:700; color:#16a34a;">
                                {row['Rekomendasi Produksi']} {row['Unit']}
                            </div>
                        </div>""", unsafe_allow_html=True)
    else:
        st.info("Pilih minimal satu komoditas di sidebar untuk melihat rekomendasi produksi.")

# ============================================================
# TAB 5 — PANDUAN LITERASI DIGITAL
# ============================================================
with tab5:
    st.markdown("""
    <div class="neo-card-blue" style="padding:14px;">
        <b>📚 Ringkasan Panduan Dosis Produk Mitra</b><br>
        Gunakan produk sesuai dosis pada label kemasan dan SOP mitra untuk komoditas sasaran.
        Jangan mencampur produk atau menaikkan dosis tanpa arahan pendamping lapangan.
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    dosis_rows = [
        ["GB Propunic", "Liter", "Ikuti dosis label/SOP; encerkan sesuai petunjuk penggunaan."],
        ["GB Profeed", "Liter", "Ikuti dosis label/SOP; gunakan pada sasaran pakan sesuai petunjuk."],
        ["GB Proquatic", "Liter", "Ikuti dosis label/SOP; aplikasikan pada media perairan sesuai petunjuk."],
        ["Pendawa Subur POC", "Liter", "Ikuti dosis label/SOP; encerkan sebelum aplikasi ke tanaman."],
        ["Compossap", "Zak", "Ikuti dosis label/SOP; sesuaikan dengan luas lahan dan jenis tanaman."],
        ["Agen Hayati [Trichogem / Methagem]", "Saset/Kg", "Ikuti dosis label/SOP; simpan dan aplikasikan sesuai arahan mitra."],
    ]
    st.dataframe(
        pd.DataFrame(dosis_rows, columns=["Produk", "Satuan", "Panduan Pemakaian"]),
        use_container_width=True,
        hide_index=True,
    )
