import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import time
from predict import DemandPredictor

t_rerun_start = time.perf_counter()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Sistem Operasional Produksi & Stok | CV Pandawa Kencana",
    page_icon="📦",
    layout="wide",
)

# ============================================================
# NEO-BRUTALISM CSS
# ============================================================
st.markdown("""
<style>
/* ---------- Google Fonts ---------- */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ---------- Global ---------- */
.stApp {
    background-color: #FFF8E7 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.main .block-container {
    padding-top: 1.5rem;
    max-width: 1400px;
}
h1, h2, h3, h4, p, label,
div:not([data-testid="stIconMaterial"]):not([data-testid="stSidebarCollapseButton"]):not([data-testid="stBaseButton-headerNoPadding"]):not([data-testid="collapsedControl"]),
span:not([data-testid="stIconMaterial"]) {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Force hide any raw text ligature spill on header/sidebar collapse buttons */
header button span,
[data-testid="stSidebarCollapseButton"] span,
[data-testid="collapsedControl"] span,
[data-testid="stBaseButton-headerNoPadding"] span,
[data-testid="stSidebarHeader"] button span,
button[kind="header"] span,
button[kind="headerNoPadding"] span,
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

/* Failsafe: if Streamlit renders text node directly inside button */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
[data-testid="stBaseButton-headerNoPadding"],
[data-testid="stSidebarHeader"] button {
    font-size: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="collapsedControl"] svg,
[data-testid="stBaseButton-headerNoPadding"] svg,
[data-testid="stSidebarHeader"] button svg {
    width: 24px !important;
    height: 24px !important;
}
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="collapsedControl"] [data-testid="stIconMaterial"],
[data-testid="stBaseButton-headerNoPadding"] [data-testid="stIconMaterial"] {
    font-size: 24px !important;
    line-height: 1 !important;
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

/* --- Sidebar: Slider Styling & High-Visibility Track Rail --- */
[data-testid="stSlider"] {
    padding: 0 2px !important;
}
[data-testid="stSidebar"] .stSlider > div {
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div {
    color: #1a1a1a !important;
}

/* Slider Track Rail - High Contrast Black Border & Fill */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div,
[data-testid="stSlider"] div[data-rac="SliderTrack"],
[data-testid="stSlider"] div[role="presentation"],
[data-testid="stSlider"] div[data-rac][data-orientation="horizontal"] > div:first-child,
[data-testid="stSlider"] [class*="efbyxod5"],
[data-testid="stSlider"] .st-emotion-cache-1ijtkbd {
    background-color: #ffffff !important;
    border: 2px solid #1a1a1a !important;
    height: 10px !important;
    border-radius: 6px !important;
}

/* Slider Active Track (Filled portion) */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div,
[data-testid="stSlider"] div[data-rac="SliderTrack"] > div {
    background-color: #1a1a1a !important;
    height: 10px !important;
}

/* Slider Thumb Knob - Big, tactile 24px knob */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSlider"] div[data-rac][style*="position: absolute"],
[data-testid="stSlider"] .st-emotion-cache-r084rb,
[data-testid="stSlider"] [class*="efbyxod3"] {
    background-color: #1a1a1a !important;
    border: 3px solid #ffffff !important;
    box-shadow: 2px 2px 0px #1a1a1a !important;
    width: 24px !important;
    height: 24px !important;
    border-radius: 50% !important;
    cursor: grab !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    top: -7px !important;
}

/* Slider Thumb Value — Display with neo-brutalism styling */
[data-testid="stSliderThumbValue"] {
    color: #1a1a1a !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Slider Tick Bar — Show min/max anchor labels for operational context */
[data-testid="stSlider"] [data-testid="stSliderTickBar"] {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
}

/* Responsive Button Spacing & Clearance */
[data-testid="stSidebar"] .stButton > button {
    margin-top: 1.2rem !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    background-color: #1a1a1a !important;
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 4px 4px 0px #ffffff !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px #ffffff !important;
    background-color: #333333 !important;
}
[data-testid="stSidebar"] .stButton > button * {
    color: #FFD600 !important;
    -webkit-text-fill-color: #FFD600 !important;
    font-weight: 700 !important;
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

/* Symmetrical alignment for price display card in sidebar */
[data-testid="stSidebar"] .neo-card {
    margin: 0.4rem 0 1rem 0 !important;
    box-sizing: border-box !important;
}

/* ---------- Metrics (with Compensatory Margin Clearance) ---------- */
[data-testid="stMetric"] {
    border: 3px solid #1a1a1a;
    border-radius: 16px;
    padding: 16px 20px;
    box-shadow: 5px 5px 0px #1a1a1a;
    margin: 0.3rem 0.5rem 0.9rem 0;
    transition: transform 0.15s, box-shadow 0.15s;
}
[data-testid="stMetric"]:hover {
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0px #1a1a1a;
}
/* Rotate colours for metric cards */
[data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetric"] { background-color: #7BF1A8; }
[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] { background-color: #88D4FF; }
[data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] { background-color: #FFD600; }
[data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] { background-color: #C4B5FD; }
/* Alternate row colors for 2x2 grid */
.kpi-row-2 > div:nth-child(1) [data-testid="stMetric"] { background-color: #FFD600 !important; }
.kpi-row-2 > div:nth-child(2) [data-testid="stMetric"] { background-color: #C4B5FD !important; }
[data-testid="stMetric"] label, [data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

.stTabs button[role="tab"],
.stTabs [data-baseweb="tab"],
.stTabs [data-testid="stTab"] {
    background: #FFD600 !important;
    background-color: #FFD600 !important;
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    box-shadow: 4px 4px 0px #1a1a1a;
    font-weight: 700 !important;
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    padding: 10px 20px !important;
    transition: all 0.15s;
}
.stTabs button[role="tab"] *,
.stTabs [data-baseweb="tab"] * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    font-weight: 700 !important;
}
.stTabs button[role="tab"] p,
.stTabs [data-baseweb="tab"] p {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    font-weight: 700 !important;
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

/* ---------- Custom classes with Compensatory Margin Clearance ---------- */
.neo-card {
    background: #fff; border: 3px solid #1a1a1a; border-radius: 16px;
    padding: 20px 22px; box-shadow: 5px 5px 0px #1a1a1a;
    margin: 0.4rem 0.5rem 1.2rem 0; color: #1a1a1a !important;
}
.neo-card-yellow {
    background: #FFD600; border: 3px solid #1a1a1a; border-radius: 16px;
    padding: 20px 22px; box-shadow: 5px 5px 0px #1a1a1a;
    margin: 0.4rem 0.5rem 1.2rem 0;
}
.neo-card-green  {
    background: #7BF1A8; border: 3px solid #1a1a1a; border-radius: 16px;
    padding: 20px 22px; box-shadow: 5px 5px 0px #1a1a1a;
    margin: 0.4rem 0.5rem 1.2rem 0;
}
.neo-card-pink   {
    background: #FF6B9D; border: 3px solid #1a1a1a; border-radius: 16px;
    padding: 20px 22px; box-shadow: 5px 5px 0px #1a1a1a;
    margin: 0.4rem 0.5rem 1.2rem 0;
}
.neo-card-blue   {
    background: #88D4FF; border: 3px solid #1a1a1a; border-radius: 16px;
    padding: 20px 22px; box-shadow: 5px 5px 0px #1a1a1a;
    margin: 0.4rem 0.5rem 1.2rem 0;
}
.neo-card-purple {
    background: #C4B5FD; border: 3px solid #1a1a1a; border-radius: 16px;
    padding: 20px 22px; box-shadow: 5px 5px 0px #1a1a1a;
    margin: 0.4rem 0.5rem 1.2rem 0;
}

.neo-title    { font-weight: 700; font-size: 2.1rem; color: #1a1a1a; margin-bottom: .3rem; }
.neo-subtitle { font-weight: 500; font-size: 1rem; color: #4a4a4a; margin-bottom: 1rem; }

.neo-badge       { display:inline-block; background:#FFD600; border:2px solid #1a1a1a; border-radius:8px; padding:4px 12px; font-weight:600; font-size:.85rem; box-shadow:2px 2px 0 #1a1a1a; margin-right:6px; }
.neo-badge-green { display:inline-block; background:#7BF1A8; border:2px solid #1a1a1a; border-radius:8px; padding:4px 12px; font-weight:600; font-size:.85rem; box-shadow:2px 2px 0 #1a1a1a; margin-right:6px; }
.neo-badge-pink  { display:inline-block; background:#FF6B9D; color:#1a1a1a; border:2px solid #1a1a1a; border-radius:8px; padding:4px 12px; font-weight:600; font-size:.85rem; box-shadow:2px 2px 0 #1a1a1a; margin-right:6px; }

.flow-container { display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; margin:1.2rem 0; }
.flow-step {
    background:#fff; border:3px solid #1a1a1a; border-radius:14px;
    padding:14px 18px; box-shadow:4px 4px 0 #1a1a1a; text-align:center;
    font-weight:600; min-width:140px; transition:transform .15s;
}
.flow-step:hover { transform:translate(-2px,-2px); box-shadow:6px 6px 0 #1a1a1a; }
.flow-step-active { background:#FFD600; }
.flow-arrow { font-size:1.8rem; font-weight:700; color:#1a1a1a; }

.status-aman      { display:inline-block; background:#7BF1A8; border:2px solid #1a1a1a; border-radius:8px; padding:4px 14px; font-weight:700; box-shadow:2px 2px 0 #1a1a1a; }
.status-peringatan{ display:inline-block; background:#FFD600; border:2px solid #1a1a1a; border-radius:8px; padding:4px 14px; font-weight:700; box-shadow:2px 2px 0 #1a1a1a; }
.status-kritis    { display:inline-block; background:#FF6B9D; color:#1a1a1a; border:2px solid #1a1a1a; border-radius:8px; padding:4px 14px; font-weight:700; box-shadow:2px 2px 0 #1a1a1a; }

/* Scrollbar */
::-webkit-scrollbar       { width: 8px; }
::-webkit-scrollbar-track { background: #FFF8E7; }
::-webkit-scrollbar-thumb { background: #1a1a1a; border-radius: 4px; }

/* Force dark text for high contrast under sunlight */
.stApp {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
.neo-badge-pink, .neo-badge-pink *,
.status-kritis, .status-kritis * {
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
}
.js-plotly-plot *, .plotly * {
    color: unset !important;
    -webkit-text-fill-color: unset !important;
}

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

.stApp [data-testid="stSegmentedControl"] {
    background: #FFFFFF !important;
    border: 3px solid #1a1a1a !important;
    border-radius: 12px !important;
    padding: 4px !important;
    box-shadow: 4px 4px 0px #1a1a1a !important;
}
.stApp [data-testid="stSegmentedControl"] * {
    background: transparent !important;
    background-color: transparent !important;
    color: #1a1a1a !important;
    -webkit-text-fill-color: #1a1a1a !important;
    font-weight: 600 !important;
}
.stApp [data-testid="stSegmentedControl"] [data-selected="true"],
.stApp [data-testid="stSegmentedControl"] [aria-checked="true"] {
    background: #FFD600 !important;
    background-color: #FFD600 !important;
    border: 2px solid #1a1a1a !important;
    box-shadow: 2px 2px 0px #1a1a1a !important;
    border-radius: 8px !important;
}
.stApp [data-testid="stSegmentedControl"] [data-selected="true"] *,
.stApp [data-testid="stSegmentedControl"] [aria-checked="true"] * {
    background: transparent !important;
    background-color: transparent !important;
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

    # Mapping komoditas resmi mitra CV Pandawa Kencana Multifarm
    komoditas_map = {
        1: "GB Propunic", 
        2: "GB Profeed", 
        3: "GB Proquatic",
        4: "Pendawa Subur POC",
        5: "Compossap",
        6: "Agen Hayati (Trichogem / Methagem)"
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
@st.cache_resource
def get_predictor():
    return DemandPredictor()

# ============================================================
# PALETTE & DOMAIN DICTIONARIES
# ============================================================
NB_MUSIM   = {"Rendeng": "#FFD600", "Gadu": "#7BF1A8", "Bera": "#88D4FF"}
NB_KOMOD   = {
    "GB Propunic": "#FFD600", 
    "GB Profeed": "#7BF1A8", 
    "GB Proquatic": "#FF6B9D",
    "Pendawa Subur POC": "#88D4FF",
    "Compossap": "#C4B5FD",
    "Agen Hayati (Trichogem / Methagem)": "#FFA07A"
}
NB_PALETTE = ["#FFD600", "#7BF1A8", "#FF6B9D", "#88D4FF", "#C4B5FD", "#FFA07A"]

KOMODITAS_ICONS = {
    "GB Propunic": "💧", 
    "GB Profeed": "🐄", 
    "GB Proquatic": "🐟",
    "Pendawa Subur POC": "🌿",
    "Compossap": "📦",
    "Agen Hayati (Trichogem / Methagem)": "🛡️"
}

UNIT_PRODUK = {
    "GB Propunic": "Liter",
    "GB Profeed": "Liter",
    "GB Proquatic": "Liter",
    "Pendawa Subur POC": "Liter",
    "Compossap": "Zak (50 Kg)",
    "Agen Hayati (Trichogem / Methagem)": "Saset / Kg",
}

STOK_MOCK = {
    "GB Propunic":  {"stok": 150.0, "threshold": 100.0, "masa_simpan": 180, "sisa_hari": 120},
    "GB Profeed": {"stok": 80.0,  "threshold": 50.0,  "masa_simpan": 120, "sisa_hari": 45},
    "GB Proquatic":{"stok": 20.0,  "threshold": 30.0,  "masa_simpan": 90,  "sisa_hari": 15},
    "Pendawa Subur POC":{"stok": 50.0,  "threshold": 40.0,  "masa_simpan": 90,  "sisa_hari": 30},
    "Compossap":{"stok": 60.0,  "threshold": 40.0,  "masa_simpan": 90,  "sisa_hari": 30},
    "Agen Hayati (Trichogem / Methagem)":{"stok": 30.0,  "threshold": 20.0,  "masa_simpan": 90,  "sisa_hari": 30},
}
STOK_DEFAULT = {"stok": 50.0, "threshold": 40.0, "masa_simpan": 90, "sisa_hari": 30}

HARGA_ACUAN_MITRA = {
    "GB Propunic": (20000, 40000, 30000),
    "GB Profeed": (25000, 45000, 35000),
    "GB Proquatic": (25000, 45000, 35000),
    "Pendawa Subur POC": (25000, 45000, 35000),
    "Compossap": (15000, 35000, 25000),
    "Agen Hayati (Trichogem / Methagem)": (120000, 180000, 150000)
}

def nb_layout(fig, title="", x_title="", y_title=""):
    """Terapkan Neo-Brutalism layout ke figure Plotly."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family="Space Grotesk, sans-serif", size=18, color="#1a1a1a"),
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
# HELPER: SHOPFLOOR PHYSICAL BATCH CONVERTER
# ============================================================
def format_batch_fisik(komoditas: str, volume: float) -> str:
    """Mengonversi nilai volume desimal ke satuan kemasan fisik pabrik."""
    if volume <= 0:
        return "Stok gudang aman (Tidak perlu batch baru)"
    
    vol = round(volume, 1)
    
    # Produk Cair (Liter)
    if any(cair in komoditas for cair in ["Propunic", "Profeed", "Proquatic", "POC"]):
        drum_100l = int(vol // 100)
        sisa_drum = round(vol % 100, 1)
        jeriken_10l = int(sisa_drum // 10)
        sisa_liter = round(sisa_drum % 10, 1)
        
        parts = []
        if drum_100l > 0:
            parts.append(f"{drum_100l} Drum (100 L)")
        if jeriken_10l > 0:
            parts.append(f"{jeriken_10l} Jeriken (10 L)")
        if sisa_liter > 0:
            parts.append(f"{sisa_liter} L Curah")
        return " + ".join(parts) if parts else f"{vol} Liter"

    # Kompos Padat (Zak 50 Kg)
    elif "Compossap" in komoditas:
        zak = int(round(vol))
        tonase = round(zak * 0.05, 2)
        return f"{zak} Zak (50 Kg) ~ {tonase} Ton Kompos Matang"

    # Agens Hayati (Saset 100 Gr / Box Karton)
    elif "Agen Hayati" in komoditas:
        saset = int(round(vol))
        box = int(saset // 10)
        sisa_saset = saset % 10
        if box > 0:
            return f"{box} Box ({saset} Saset @ 100 gr)" if sisa_saset == 0 else f"{box} Box + {sisa_saset} Saset (100 gr)"
        return f"{saset} Saset (100 gr) Formulasi Aktif"

    return f"{vol} Unit Produk"

# ============================================================
# HELPER: QUICK OPERATIONAL STEPPER (TOP BANNER)
# ============================================================
def render_operational_stepper(selected_komoditas, jalur_penjualan, simulasi_harga, pred_df, kritis_count):
    """Menampilkan kompas navigasi operasional berdaya kontras tinggi."""
    status_stok_text = f"{kritis_count} SKU Kritis" if kritis_count > 0 else "Semua SKU Aman"
    status_stok_color = "#FF6B9D" if kritis_count > 0 else "#7BF1A8"
    
    chan_label = jalur_penjualan if jalur_penjualan else "Belum Dipilih"
    pred_status = "Terkalkulasi (Siap)" if not pred_df.empty else "Perlu Dihitung"
    pred_color = "#7BF1A8" if not pred_df.empty else "#FFD600"

    st.markdown(f"""
    <div style="background:#FFFFFF; border:3px solid #1a1a1a; border-radius:14px; padding:14px 18px; box-shadow:5px 5px 0px #1a1a1a; margin-bottom:1.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #1a1a1a; padding-bottom:8px; margin-bottom:10px;">
            <div style="font-size:0.85rem; font-weight:700; color:#1a1a1a; letter-spacing:0.5px;">
                STATUS KENDALI OPERASIONAL PABRIK — CV PANDAWA KENCANA
            </div>
            <div style="font-size:0.75rem; background:#FFD600; border:2px solid #1a1a1a; border-radius:6px; padding:2px 8px; font-weight:700; color:#1a1a1a;">
                GUDANG CANGKRINGAN
            </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:10px;">
            <div style="background:#FAFAFA; border:2px solid #1a1a1a; border-radius:10px; padding:10px 12px;">
                <div style="font-size:0.7rem; color:#555; font-weight:700;">LANGKAH 1: PARAMETER</div>
                <div style="font-size:0.95rem; font-weight:700; color:#1a1a1a;">{len(selected_komoditas)} SKU Terpilih</div>
                <div style="font-size:0.75rem; color:#333;">Kanal: {chan_label}</div>
            </div>
            <div style="background:#FAFAFA; border:2px solid #1a1a1a; border-radius:10px; padding:10px 12px;">
                <div style="font-size:0.7rem; color:#555; font-weight:700;">LANGKAH 2: GUDANG</div>
                <div style="font-size:0.95rem; font-weight:700; color:{status_stok_color};">{status_stok_text}</div>
                <div style="font-size:0.75rem; color:#333;">Evaluasi Batas Minimum</div>
            </div>
            <div style="background:#FAFAFA; border:2px solid #1a1a1a; border-radius:10px; padding:10px 12px;">
                <div style="font-size:0.7rem; color:#555; font-weight:700;">LANGKAH 3: SIMULASI</div>
                <div style="font-size:0.95rem; font-weight:700; color:#1a1a1a;">Rp {simulasi_harga:,.0f} / Unit</div>
                <div style="font-size:0.75rem; color:#333;">Sensitivitas Harga Acuan</div>
            </div>
            <div style="background:#FAFAFA; border:2px solid #1a1a1a; border-radius:10px; padding:10px 12px;">
                <div style="font-size:0.7rem; color:#555; font-weight:700;">LANGKAH 4: SPK DSS</div>
                <div style="font-size:0.95rem; font-weight:700; color:{pred_color};">{pred_status}</div>
                <div style="font-size:0.75rem; color:#333;">Batch Drum / Jeriken / Zak</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# HELPER: UPGRADED DSS PRODUCTION CARDS
# ============================================================
def render_dss_production_cards(pred_df):
    """Menampilkan kartu kerja fisik yang dapat langsung dieksekusi mandor."""
    if pred_df.empty:
        st.info("Kalkulasi kebutuhan belum dijalankan. Klik tombol 'Hitung Kebutuhan Produksi Pabrik' di panel sebelah kiri.")
        return

    st.markdown("""
    <div class="neo-card-green" style="padding:14px; margin-bottom:1.2rem;">
        <div style="font-weight:700; font-size:1.1rem; color:#1a1a1a;">PERINTAH KERJA PRODUKSI PABRIK (SPK)</div>
        <div style="font-size:0.85rem; color:#1a1a1a; margin-top:3px;">
            Kebutuhan bersih dihitung berdasarkan formula: <b>(Perkiraan Pesanan Pasar - Stok Fisik Gudang) + Cadangan Pengaman 15%</b>.
            Nilai wadah fisik menunjukkan takaran kemasan yang harus disiapkan oleh mandor gudang pengemasan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    for i in range(0, len(pred_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(pred_df):
                row = pred_df.iloc[i + j]
                k = row["Komoditas"]
                rekom_val = row["Rekomendasi Produksi"]
                unit_str = row["Unit"]
                batch_text = format_batch_fisik(k, rekom_val)
                ico = KOMODITAS_ICONS.get(k, "📦")
                
                with cols[j]:
                    st.markdown(f"""
                    <div class="neo-card" style="padding:16px; text-align:center; min-height:240px; display:flex; flex-direction:column; justify-content:space-between;">
                        <div>
                            <div style="font-size:1.8rem; margin-bottom:2px;">{ico}</div>
                            <div style="font-weight:700; font-size:1.15rem; color:#1a1a1a; margin-top:2px;">{k}</div>
                            <div style="font-size:0.75rem; color:#555; margin-top:2px;">Kanal: {row.get('Jalur Penjualan', 'Wholesale')}</div>
                        </div>
                        <div style="margin:10px 0; padding:8px 10px; background:#FAFAFA; border:2px solid #1a1a1a; border-radius:10px;">
                            <div style="font-size:0.75rem; font-weight:700; color:#333;">TARGET VOLUME PABRIK:</div>
                            <div style="font-size:1.45rem; font-weight:700; color:#1a1a1a;">
                                {rekom_val:,.1f} <span style="font-size:0.9rem;">{unit_str}</span>
                            </div>
                        </div>
                        <div style="background:#FFD600; border:2px solid #1a1a1a; border-radius:8px; padding:6px 8px;">
                            <div style="font-size:0.7rem; font-weight:700; color:#1a1a1a;">WADAH & KEMASAN FISIK:</div>
                            <div style="font-size:0.85rem; font-weight:700; color:#1a1a1a;">{batch_text}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ============================================================
# PREDICTION CACHED FUNCTION
# ============================================================
@st.cache_data
def run_predictions_cached(komoditas_tuple, sim_harga, channel, season, _hist_df):
    pred_rows = []
    komoditas_id_map = {
        "GB Propunic": 1,
        "GB Profeed": 2,
        "GB Proquatic": 3,
        "Pendawa Subur POC": 4,
        "Compossap": 5,
        "Agen Hayati (Trichogem / Methagem)": 6
    }
    predictor_model = get_predictor()

    for k in komoditas_tuple:
        sku_history = _hist_df[_hist_df["nama_komoditas"] == k]
        base_demand = float(sku_history["volume_permintaan"].mean()) if not sku_history.empty else 100.0
        curah_hujan_avg = float(sku_history["curah_hujan_mm"].mean()) if not sku_history.empty else 150.0
        
        raw_input = [{
            'id_poktan': 1, 'id_komoditas': komoditas_id_map.get(k, 0),
            'harga_satuan_transaksi': sim_harga, 'curah_hujan_mm': curah_hujan_avg,
            'lag_1w': base_demand, 'lag_4w': base_demand, 'lag_7w': base_demand,
            'rolling_mean_4w': base_demand, 'fase_musim': season
        }]
        try:
            demand = float(predictor_model.predict(raw_input))
        except Exception:
            demand = base_demand
            
        buf = round(demand * 0.15, 1)
        stok_aktif = STOK_MOCK.get(k, STOK_DEFAULT)["stok"]
        rekomendasi = max(0.0, round(demand - stok_aktif + buf, 1))
        
        rmse_sku = 12.5
        margin_ci = round(1.96 * rmse_sku, 1)
        lower_bound = max(0.0, round(demand - margin_ci, 1))
        upper_bound = round(demand + margin_ci, 1)

        pred_rows.append({
            "Komoditas": k,
            "Unit": UNIT_PRODUK.get(k, "Unit Produk"),
            "Jalur Penjualan": channel,
            "Prediksi Permintaan": demand,
            "Lower Bound (95%)": lower_bound,
            "Upper Bound (95%)": upper_bound,
            "Rekomendasi Produksi": rekomendasi,
            "Safety Buffer": buf,
        })
        
    return pd.DataFrame(pred_rows)

# ============================================================
# CACHED VISUALIZATION ROUTINES (RUNTIME PERFORMANCE OPTIMIZATION)
# ============================================================
@st.cache_data(show_spinner=False)
def generate_cached_gauge_figures(selected_komoditas_tuple):
    """
    Cached routine for static warehouse inventory gauges in Tab 1.
    Eliminates redundant Plotly gauge indicator recreation during sidebar slider adjustments.
    """
    gauge_figs = {}
    for k in selected_komoditas_tuple:
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
        nb_layout(fig, f"Sisa Umur Bakteri Aktif — {k}")
        fig.update_layout(height=270, margin=dict(t=55, b=15, l=25, r=25))
        gauge_figs[k] = fig
    return gauge_figs


@st.cache_data(show_spinner=False)
def generate_cached_historical_figures(df_sub):
    """
    Cached routine to generate heavy historical figures (Area Chart, Horizontal Bar, Donut Chart).
    Eliminates redundant Plotly figure recreation during sidebar slider adjustments.
    """
    if df_sub.empty:
        return None, None, None

    # 1. Dynamic Area Chart (Trend per month & commodity)
    trend = (
        df_sub
        .groupby([pd.Grouper(key="tanggal_permintaan", freq="ME"), "nama_komoditas"])["volume_permintaan"]
        .sum()
        .reset_index()
    )
    trend["Satuan"] = trend["nama_komoditas"].map(UNIT_PRODUK)
    fig_trend = px.area(
        trend, x="tanggal_permintaan", y="volume_permintaan",
        color="nama_komoditas", color_discrete_map=NB_KOMOD,
        markers=True, facet_row="Satuan"
    )
    fig_trend.update_traces(
        line_width=3,
        marker=dict(size=7, line=dict(width=2, color="#1a1a1a")),
        fillcolor=None,
    )
    for trace in fig_trend.data:
        hex_c = trace.line.color or "#FFD600"
        trace.fillcolor = hex_c.replace(")", ",0.15)").replace("rgb", "rgba") if "rgb" in str(hex_c) else None

    fig_trend.update_yaxes(matches=None, showticklabels=True)
    fig_trend.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    nb_layout(fig_trend, "Dinamika Permintaan Produk per Periode Waktu", x_title="", y_title="Volume Penyaluran")

    fig_trend.update_layout(
        height=600,
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
    )
    fig_trend.update_xaxes(title_text="Bulan", row=1, col=1)

    # 2. Horizontal Bar Chart (Volume distribution)
    vol = df_sub.groupby("nama_komoditas")["volume_permintaan"].sum().reset_index()
    vol["nama_pendek"] = vol["nama_komoditas"].replace({
        "Agen Hayati (Trichogem / Methagem)": "Agen Hayati",
        "Pendawa Subur POC": "Pendawa POC"
    })
    vol = vol.sort_values(["volume_permintaan"], ascending=True)

    fig_bar = px.bar(
        vol, y="nama_pendek", x="volume_permintaan",
        color="nama_komoditas", color_discrete_map=NB_KOMOD,
        orientation="h", text="volume_permintaan"
    )
    fig_bar.update_traces(
        marker_line_color="#1a1a1a", marker_line_width=2,
        texttemplate="%{text:,.0f}", textposition="auto",
        textfont=dict(family="Space Grotesk", size=13, color="#1a1a1a"),
    )

    fig_bar.update_layout(showlegend=False)
    nb_layout(fig_bar, "Akumulasi Penyaluran per Komoditas", x_title="Total Volume Terdistribusi", y_title="")
    fig_bar.update_layout(height=600)

    # 3. Donut Pie Chart (Proportion by season)
    mcount = df_sub.groupby("fase_musim")["volume_permintaan"].sum().reset_index()
    fig_donut = px.pie(
        mcount, values="volume_permintaan", names="fase_musim",
        color="fase_musim", color_discrete_map=NB_MUSIM, hole=0.45,
    )
    fig_donut.update_traces(
        textinfo="label+percent",
        textfont=dict(family="Space Grotesk", size=14, color="#1a1a1a"),
        marker_line=dict(color="#1a1a1a", width=2.5),
        pull=[0.03, 0.03, 0.03],
    )
    nb_layout(fig_donut, "Proporsi Permintaan Berdasarkan Musim Tanam")
    fig_donut.update_layout(height=400)

    return fig_trend, fig_bar, fig_donut


@st.cache_data(show_spinner=False)
def generate_cached_scatter_figure(df_sub, chart_view, sel_fokus=None):
    """
    Cached routine for heavy scatter and correlation subplots in Tab 4.
    """
    if df_sub.empty:
        return None

    if chart_view == "Sebaran & Korelasi":
        avail_komod = [k for k in ["GB Propunic", "GB Profeed", "GB Proquatic", "Pendawa Subur POC", "Compossap", "Agen Hayati (Trichogem / Methagem)"] if k in df_sub["nama_komoditas"].unique()]
        
        if sel_fokus == "Bandingkan Semua Komoditas" or (sel_fokus is None and len(avail_komod) > 1):
            cols_count = len(avail_komod)
            short_names = {
                "Agen Hayati (Trichogem / Methagem)": "Agen Hayati",
                "Pendawa Subur POC": "Pendawa POC"
            }
            short_avail = [short_names.get(k, k) for k in avail_komod]
            fig_sub = make_subplots(
                rows=1, cols=cols_count,
                subplot_titles=[f"<b>{k}</b>" for k in short_avail],
                horizontal_spacing=0.07
            )
            for idx, k in enumerate(avail_komod, 1):
                sub_data = df_sub[df_sub["nama_komoditas"] == k]
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
                            "Volume: %{y:,.1f}<br>"
                            "Hujan: %{customdata[1]:.1f} mm<extra></extra>"
                        ),
                        name=k,
                        showlegend=False
                    ),
                    row=1, col=idx
                )
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
                    title_text="Volume Pesanan" if idx == 1 else "", row=1, col=idx,
                    showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2,
                    tickfont=dict(size=10, color="#1a1a1a"), title_font=dict(size=11, color="#1a1a1a")
                )

            fig_sub.update_annotations(font_size=11)
            fig_sub.update_layout(
                height=400,
                plot_bgcolor="#FAFAFA",
                paper_bgcolor="#FFFFFF",
                margin=dict(l=40, r=20, t=40, b=45),
                font=dict(family="Space Grotesk, sans-serif", size=12, color="#1a1a1a"),
                hoverlabel=dict(bgcolor="#FFD600", bordercolor="#1a1a1a", font=dict(family="Space Grotesk", color="#1a1a1a"))
            )
            return fig_sub

        elif sel_fokus:
            clean_k = sel_fokus
            sub_data = df_sub[df_sub["nama_komoditas"] == clean_k]
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
                nb_layout(fig_single, f"Distribusi Transaksi & Sensitivitas Harga: {clean_k}", x_title="", y_title="")
                fig_single.update_layout(
                    xaxis_title="Harga Satuan (Rp)",
                    yaxis_title="Volume Pesanan",
                    height=480,
                    margin=dict(t=80, b=80),
                    legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5)
                )
                return fig_single

    elif chart_view == "Dinamika Bulanan (Dual-Axis)":
        monthly = (
            df_sub
            .groupby(pd.Grouper(key="tanggal_permintaan", freq="MS"))
            .agg(vol=("volume_permintaan", "sum"), harga=("harga_satuan_transaksi", "mean"))
            .reset_index()
        )
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        fig_dual.add_trace(
            go.Bar(
                x=monthly["tanggal_permintaan"], y=monthly["vol"],
                name="Total Volume Penyaluran",
                marker_color="#FFD600", marker_line_color="#1a1a1a", marker_line_width=2,
                hovertemplate="<b>%{x|%b %Y}</b><br>Volume: %{y:,.1f}<extra></extra>"
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
        fig_dual.update_yaxes(title_text="Total Volume Penyaluran", showgrid=True, gridcolor="#E8E8E8", linecolor="#1a1a1a", linewidth=2, secondary_y=False, tickfont=dict(color="#1a1a1a"))
        fig_dual.update_yaxes(title_text="Rata-rata Harga Satuan (Rp)", showgrid=False, linecolor="#1a1a1a", linewidth=2, secondary_y=True, tickfont=dict(color="#1a1a1a"))
        fig_dual.update_layout(
            title=dict(text="<b>Dinamika Fluktuasi: Permintaan vs Harga Bulanan</b>", font=dict(family="Space Grotesk, sans-serif", size=16, color="#1a1a1a")),
            height=450, plot_bgcolor="#FAFAFA", paper_bgcolor="#FFFFFF",
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, bgcolor="#FFFFFF", bordercolor="#1a1a1a", borderwidth=2, font=dict(color="#1a1a1a")),
            margin=dict(l=45, r=45, t=65, b=45),
            hoverlabel=dict(bgcolor="#FFD600", bordercolor="#1a1a1a", font=dict(family="Space Grotesk", color="#1a1a1a"))
        )
        return fig_dual

    elif chart_view == "Rentang Variasi (Boxplot)":
        avail_komod = [k for k in ["GB Propunic", "GB Profeed", "GB Proquatic", "Pendawa Subur POC", "Compossap", "Agen Hayati (Trichogem / Methagem)"] if k in df_sub["nama_komoditas"].unique()]
        fig_box = make_subplots(rows=1, cols=2, subplot_titles=["<b>Sebaran Variasi Harga Transaksi (Rp)</b>", "<b>Sebaran Volume Permintaan</b>"], horizontal_spacing=0.1)
        for komod in avail_komod:
            sub = df_sub[df_sub["nama_komoditas"] == komod]
            short_komod = komod.replace("Agen Hayati (Trichogem / Methagem)", "Agen Hayati").replace("Pendawa Subur POC", "Pendawa POC")
            fig_box.add_trace(
                go.Box(
                    y=sub["harga_satuan_transaksi"], name=short_komod,
                    marker_color=NB_KOMOD.get(komod, "#FFD600"),
                    line=dict(color="#1a1a1a", width=2),
                    boxpoints="outliers"
                ),
                row=1, col=1
            )
            fig_box.add_trace(
                go.Box(
                    y=sub["volume_permintaan"], name=short_komod,
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
            showlegend=False,
            height=450, plot_bgcolor="#FAFAFA", paper_bgcolor="#FFFFFF",
            margin=dict(l=45, r=25, t=65, b=45),
            hoverlabel=dict(bgcolor="#FFD600", bordercolor="#1a1a1a", font=dict(family="Space Grotesk", color="#1a1a1a"))
        )
        return fig_box

    return None

# ============================================================
# SIDEBAR — PANEL KONTROL OPERASIONAL PABRIK
# ============================================================
st.sidebar.markdown("""
<div style="text-align:center; margin-bottom:.8rem;">
    <div class="neo-title" style="font-size:1.35rem; margin-top:.4rem;">KONTROL OPERASIONAL PABRIK</div>
    <div class="neo-subtitle" style="font-size:.82rem;">Konfigurasi batch produksi, kanal distribusi, & harga acuan</div>
</div>
""", unsafe_allow_html=True)

# Bootstrap session state with True so app never starts blank
if "prediction_requested" not in st.session_state:
    st.session_state.prediction_requested = True

if "pred_df" not in st.session_state:
    st.session_state.pred_df = pd.DataFrame()

selected_komoditas = []
selected_musim     = []
simulasi_harga     = 0.0
jalur_penjualan    = ""
filtered_df        = pd.DataFrame()

if not df.empty:
    # 1. Komoditas (Default: Semua SKU terpilih)
    st.sidebar.markdown("### 1. Komoditas Pupuk & Pakan")
    komoditas_list = list(KOMODITAS_ICONS.keys())
    selected_komoditas = st.sidebar.multiselect(
        "Pilih Komoditas", komoditas_list, default=komoditas_list, label_visibility="collapsed"
    )

    # 2. Jalur Distribusi (Default: Langsung ke Poktan)
    st.sidebar.markdown("### 2. Kirim ke Mana?")
    jalur_penjualan = st.sidebar.radio(
        "Pilih Jalur Distribusi",
        ["Langsung ke Poktan (Grosir)", "Marketplace Online (Eceran)"],
        index=0,
        help="Poktan = pesanan partai besar dari gudang. Marketplace = pesanan eceran via Shopee/Tokopedia.",
    )

    # 3. Kalender Musim
    st.sidebar.markdown("### 3. Kalender Musim Tanam (Sleman)")
    musim_list = (
        sorted(df["fase_musim"].unique().tolist())
        if "fase_musim" in df.columns
        else ["Rendeng", "Gadu", "Bera"]
    )
    selected_musim = st.sidebar.multiselect(
        "Pilih Fase Musim", musim_list, default=musim_list, label_visibility="collapsed"
    )

    # 4. Rentang Tanggal Audit
    st.sidebar.markdown("### 4. Periode Audit Data Historis")
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

    # 5. Simulasi Harga Satuan Acuan
    st.sidebar.markdown("### 5. Simulasi Harga Satuan Acuan")
    st.sidebar.markdown(
        '<div style="font-size:0.8rem; color:#333; margin-top:-8px; margin-bottom:8px;">'
        'Uji dampak harga terhadap perkiraan pesanan (Grosir vs Eceran)</div>',
        unsafe_allow_html=True,
    )
    sku_ref = selected_komoditas[0] if selected_komoditas else "GB Propunic"
    p_min, p_max, p_default = HARGA_ACUAN_MITRA.get(sku_ref, (10000, 100000, 30000))

    simulasi_harga = st.sidebar.slider(
        f"Harga Satuan Acuan — {sku_ref}",
        min_value=p_min,
        max_value=p_max,
        value=p_default,
        step=1000,
        help=f"Geser ke kiri = harga grosir untuk Poktan. Geser ke kanan = harga eceran marketplace. Berlaku untuk: {sku_ref}.",
    )

    # Anchor markers: Grosir (kiri) ↔ Eceran (kanan)
    anchor_left, anchor_right = st.sidebar.columns(2)
    anchor_left.markdown(
        f'<div style="font-size:0.72rem; font-weight:600; color:#1a1a1a;">← Grosir Poktan<br>Rp {p_min:,.0f}</div>',
        unsafe_allow_html=True,
    )
    anchor_right.markdown(
        f'<div style="font-size:0.72rem; font-weight:600; color:#1a1a1a; text-align:right;">Eceran Pasar →<br>Rp {p_max:,.0f}</div>',
        unsafe_allow_html=True,
    )

    # Dynamic status indicator
    if simulasi_harga == p_min:
        harga_status = "💡 Skenario Diskon / Grosir Poktan"
    elif simulasi_harga == p_default:
        harga_status = "💡 Skenario Harga Standar Kemitraan"
    elif simulasi_harga == p_max:
        harga_status = "💡 Skenario Margin Tertinggi (Retail)"
    else:
        harga_status = "💡 Skenario Uji Sensitivitas Pasar"

    st.sidebar.markdown(
        f"""
        <div class="neo-card" style="text-align:center; padding:12px; margin-bottom:1rem;">
            <div style="font-size:.78rem; font-weight:700; color:#555;">HARGA SATUAN SIMULASI (PER UNIT)</div>
            <div style="font-size:1.4rem; font-weight:700; color:#1a1a1a;">Rp {simulasi_harga:,.0f}</div>
            <div style="font-size:.78rem; font-weight:600; color:#333; margin-top:4px;">{harga_status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    prediksi_diklik = st.sidebar.button("Hitung Kebutuhan Produksi Pabrik", type="primary", use_container_width=True)
    if prediksi_diklik:
        validation_errors = []
        if not selected_komoditas:
            validation_errors.append("[Langkah 1] Pilih minimal satu produk pupuk/pakan")
        if not jalur_penjualan:
            validation_errors.append("[Langkah 2] Pilih jalur distribusi penjualan (Wholesale/Retail)")
        if not isinstance(date_range, tuple) or len(date_range) != 2:
            validation_errors.append("[Langkah 4] Lengkapi rentang tanggal awal dan akhir audit")

        if validation_errors:
            st.session_state.prediction_requested = False
            st.sidebar.error("Lengkapi parameter berikut:\n\n" + "\n".join(f"- {e}" for e in validation_errors))
        else:
            st.session_state.prediction_requested = True
            st.sidebar.success("Kalkulasi selesai. Rekomendasi batch produksi dan estimasi permintaan telah diperbarui.")

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
    st.sidebar.warning("Data transaksi tidak tersedia.")

# ============================================================
# PREDICTION COMPUTATION & PRE-RENDER DATA PREPARATION
# ============================================================
t_pred_start = time.perf_counter()
if selected_komoditas and st.session_state.prediction_requested:
    try:
        historical_df = filtered_df if not filtered_df.empty else df
        selected_channel = jalur_penjualan if jalur_penjualan else "Langsung ke Poktan (Grosir)"
        selected_season = selected_musim[0] if selected_musim else "Rendeng"
        
        st.session_state.pred_df = run_predictions_cached(
            tuple(selected_komoditas),
            simulasi_harga,
            selected_channel,
            selected_season,
            historical_df
        )
    except Exception as exc:
        st.warning(f"Kalkulasi estimasi mengalami kendala: {exc}. Menampilkan data cadangan historis.")
        st.session_state.pred_df = pd.DataFrame()
t_pred_dur = (time.perf_counter() - t_pred_start) * 1000

# Count critical stock SKUs for stepper status
kritis_list = [k for k in selected_komoditas if STOK_MOCK.get(k, STOK_DEFAULT)["stok"] < STOK_MOCK.get(k, STOK_DEFAULT)["threshold"]]
kritis_count = len(kritis_list)

# ============================================================
# MAIN HEADER & OPERATIONAL STEPPER
# ============================================================
st.markdown("""
<div class="neo-title">Sistem Kendali Produksi & Distribusi Pupuk/Pakan</div>
<div class="neo-subtitle">Sistem Pendukung Keputusan (DSS) Operasional Pabrik — CV Pandawa Kencana Multifarm (Cangkringan, Sleman)</div>
""", unsafe_allow_html=True)

render_operational_stepper(selected_komoditas, jalur_penjualan, simulasi_harga, st.session_state.pred_df, kritis_count)

# Re-architected 5 tabs matching shopfloor reality
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. 🏭 Stok Gudang & Umur Produk",
    "2. 📋 Perintah Produksi Pabrik",
    "3. 🔮 Simulasi Permintaan Pasar",
    "4. 📊 Riwayat Penjualan",
    "5. 📖 SOP & Dosis Pemakaian",
])

# ============================================================
# TAB 1 — STOK & MUTU GUDANG
# ============================================================
t_tab1_start = time.perf_counter()
with tab1:
    st.markdown("""
    <div class="neo-card" style="padding:14px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <b>Pemantauan Masa Aktif Bakteri Pengurai & Ketersediaan Stok Gudang</b>
            <span class="neo-badge-pink">[DATA SIMULASI]</span>
        </div>
        Cek ketersediaan fisik produk di gudang Cangkringan dan sisa umur bakteri pengurai/probiotik sebelum terjadi penurunan kualitas.
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
                        status, cls, emoji = "STOK AMAN", "status-aman", "✅"
                        card = "neo-card-green"
                    elif ratio >= 1.0:
                        status, cls, emoji = "SIAGA BUFFER", "status-peringatan", "⚠️"
                        card = "neo-card-yellow"
                    else:
                        status, cls, emoji = "KRITIS", "status-kritis", "🚨"
                        card = "neo-card-pink"

                    ico = KOMODITAS_ICONS.get(k, "📦")

                    with cols[j]:
                        st.markdown(f"""
                        <div class="{card}" style="text-align:center;">
                            <div style="font-size:2.2rem;">{ico}</div>
                            <div style="font-weight:700; font-size:1.25rem; margin:6px 0;">{k}</div>
                            <div class="{cls}">{emoji} {status}</div>
                            <div style="margin-top:14px;">
                                <div style="font-size:.78rem; color:#333;">Stok Aktual</div>
                                <div style="font-weight:700; font-size:1.7rem;">{d['stok']} {unit}</div>
                            </div>
                            <div style="margin-top:6px;">
                                <div style="font-size:.78rem; color:#333;">Batas Minimum Gudang</div>
                                <div style="font-weight:700; font-size:1.15rem;">{d['threshold']} {unit}</div>
                            </div>
                            <div style="margin-top:6px;">
                                <div style="font-size:.78rem; color:#333;">Sisa Masa Efektif Hayati</div>
                                <div style="font-weight:700; font-size:1.15rem;">{d['sisa_hari']} hari</div>
                            </div>
                        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Gauge charts (Cached) ---
        gauge_figs = generate_cached_gauge_figures(tuple(selected_komoditas))
        for i in range(0, len(selected_komoditas), 3):
            gcols = st.columns(3)
            for j in range(3):
                if i + j < len(selected_komoditas):
                    k = selected_komoditas[i + j]
                    fig = gauge_figs.get(k)
                    if fig is not None:
                        with gcols[j]:
                            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # --- Alerts ---
        kritis  = [k for k in selected_komoditas if STOK_MOCK.get(k, STOK_DEFAULT)["stok"] < STOK_MOCK.get(k, STOK_DEFAULT)["threshold"]]
        expiring = [k for k in selected_komoditas if STOK_MOCK.get(k, STOK_DEFAULT)["sisa_hari"] < 30 and k not in kritis]

        if kritis:
            st.markdown(f"""
            <div class="neo-card-pink" style="padding:14px;">
                <b>PERINGATAN DEFISIT STOK:</b> Ketersediaan fisik <b>{', '.join(kritis)}</b> berada di bawah batas minimum operasional gudang.
                Segera terbitkan Surat Perintah Kerja (SPK) untuk siklus fermentasi/pengemasan baru.
            </div>""", unsafe_allow_html=True)
        if expiring:
            st.markdown(f"""
            <div class="neo-card-yellow" style="padding:14px;">
                <b>PERINGATAN DEGRADASI HAYATI:</b> Masa aktif mikroba <b>{', '.join(expiring)}</b> tersisa kurang dari 30 hari.
                Segera terapkan rotasi stok FIFO (First-In First-Out) dan utamakan pengiriman ke Poktan binaan.
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="neo-card-yellow" style="text-align:center;">
            <b style="font-size:1.1rem;">Pilih minimal satu komoditas pada panel kontrol sebelah kiri untuk memantau status gudang.</b>
        </div>""", unsafe_allow_html=True)
t_tab1_dur = (time.perf_counter() - t_tab1_start) * 1000

# ============================================================
# TAB 2 — RENCANA PRODUKSI (DSS)
# ============================================================
t_tab2_start = time.perf_counter()
with tab2:
    render_dss_production_cards(st.session_state.pred_df)
    
    if not st.session_state.pred_df.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        summary_display = st.session_state.pred_df[["Komoditas", "Unit", "Jalur Penjualan", "Prediksi Permintaan", "Safety Buffer", "Rekomendasi Produksi"]].copy()
        summary_display["Alokasi Wadah Pabrik"] = summary_display.apply(
            lambda r: format_batch_fisik(r["Komoditas"], r["Rekomendasi Produksi"]), axis=1
        )
        st.dataframe(
            summary_display,
            use_container_width=True,
            hide_index=True,
        )
        csv_data = summary_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Unduh Rencana Batch Pabrik (CSV)",
            data=csv_data,
            file_name="rencana_batch_pandawa.csv",
            mime="text/csv",
            use_container_width=False,
        )
    else:
        st.info("Rekomendasi alokasi batch belum dapat dihitung. Pastikan produk dipilih dan klik tombol 'Hitung Kebutuhan Produksi Pabrik' pada panel sebelah kiri.")
t_tab2_dur = (time.perf_counter() - t_tab2_start) * 1000

# ============================================================
# TAB 3 — SIMULASI KEBUTUHAN PASAR (WHAT-IF SENSITIVITY)
# ============================================================
t_tab3_start = time.perf_counter()
with tab3:
    # --- Flow diagram ---
    st.markdown("""
    <div class="neo-card" style="margin-bottom:1.5rem;">
        <div class="flow-container">
            <div class="flow-step flow-step-active">
                <div style="font-weight:700; font-size:1.05rem; margin-bottom:4px;">1. Parameter Operasional</div>
                <div style="font-size:.75rem; color:#444;">Harga Acuan · Musim Tanam · Kanal</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
                <div style="font-weight:700; font-size:1.05rem; margin-bottom:4px;">2. Validasi Data Pabrik</div>
                <div style="font-size:.75rem; color:#444;">Sinkronisasi Transaksi & BMKG</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">
                <div style="font-weight:700; font-size:1.05rem; margin-bottom:4px;">3. Kalkulasi Estimasi Permintaan</div>
                <div style="font-size:.75rem; color:#444;">Proyeksi Kebutuhan Lapangan</div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-step flow-step-active">
                <div style="font-weight:700; font-size:1.05rem; margin-bottom:4px;">4. Alokasi Batch Produksi</div>
                <div style="font-size:.75rem; color:#444;">Output Drum / Jeriken / Zak</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Parameter cards ---
    p1, p2, p3 = st.columns(3)
    p1.markdown(f"""
    <div class="neo-card-yellow" style="text-align:center;">
        <div style="font-weight:700; font-size:.85rem; color:#555;">Harga Satuan Acuan</div>
        <div style="font-weight:700; font-size:1.4rem; color:#1a1a1a;">Rp {simulasi_harga:,.0f}</div>
    </div>""", unsafe_allow_html=True)
    p2.markdown(f"""
    <div class="neo-card-green" style="text-align:center;">
        <div style="font-weight:700; font-size:.85rem; color:#555;">Kalender Musim Aktif</div>
        <div style="font-weight:700; font-size:1.05rem; color:#1a1a1a;">{', '.join(selected_musim) or 'Belum Dipilih'}</div>
    </div>""", unsafe_allow_html=True)
    p3.markdown(f"""
    <div class="neo-card-blue" style="text-align:center;">
        <div style="font-weight:700; font-size:.85rem; color:#555;">Komoditas dalam Analisis</div>
        <div style="font-weight:700; font-size:1.05rem; color:#1a1a1a;">{', '.join(selected_komoditas) or 'Belum Dipilih'}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="neo-card-green" style="padding:14px;">
        <b>Status Sistem: Estimasi Permintaan Terverifikasi</b><br>
        Proyeksi kebutuhan pasar dihitung berdasarkan kalender musim tanam aktif dan elastisitas harga satuan acuan CV Pandawa Kencana.
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Prediction chart ---
    if selected_komoditas and not st.session_state.pred_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Prediksi Permintaan", x=st.session_state.pred_df["Komoditas"],
            y=st.session_state.pred_df["Prediksi Permintaan"],
            text=st.session_state.pred_df["Prediksi Permintaan"].map(lambda value: f"{value:.1f}"),
            textposition="outside",
            marker_color=[NB_KOMOD.get(name, "#88D4FF") for name in st.session_state.pred_df["Komoditas"]],
            marker_line_color="#1a1a1a", marker_line_width=2,
            hovertemplate="<b>%{x}</b><br>Estimasi: %{y:.1f}<extra></extra>",
            error_y=dict(
                type='data',
                symmetric=False,
                array=st.session_state.pred_df["Upper Bound (95%)"] - st.session_state.pred_df["Prediksi Permintaan"],
                arrayminus=st.session_state.pred_df["Prediksi Permintaan"] - st.session_state.pred_df["Lower Bound (95%)"],
                visible=True,
                color='#1a1a1a',
                thickness=2
            ),
        ))
        nb_layout(fig, f"Proyeksi Penyerapan Pasar pada Harga Rp {simulasi_harga:,.0f}", y_title="Estimasi Kebutuhan (Satuan Resmi)")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("Rentang batas atas dan bawah (garis vertikal) menunjukkan batas toleransi fluktuasi pasar (±25 unit). Jika pesanan mendekati batas atas, siapkan kapasitas drum fermentasi cadangan.")
    else:
        st.markdown("""
        <div class="neo-card-yellow" style="text-align:center;">
            <b style="font-size:1.1rem;">Kalkulasi simulasi belum dijalankan. Klik tombol 'Hitung Kebutuhan Produksi Pabrik' pada panel sebelah kiri untuk memproses data.</b>
        </div>""", unsafe_allow_html=True)
t_tab3_dur = (time.perf_counter() - t_tab3_start) * 1000

# ============================================================
# TAB 4 — TREN PENJUALAN HISTORIS
# ============================================================
t_tab4_start = time.perf_counter()
with tab4:
    if not filtered_df.empty:
        # --- KPI row (Rebalanced 2x2 grid for optimal visual balance & legibility) ---
        kpi_r1_c1, kpi_r1_c2 = st.columns(2)
        kpi_r1_c1.metric("Volume Transaksi Tercatat", f"{len(filtered_df):,}")
        total_nilai = (
            filtered_df["volume_permintaan"]
            * filtered_df["harga_satuan_transaksi"]
        ).sum()
        kpi_r1_c2.metric("Estimasi Omzet Historis", f"Rp {total_nilai:,.0f}")

        st.markdown('<div class="kpi-row-2">', unsafe_allow_html=True)
        kpi_r2_c1, kpi_r2_c2 = st.columns(2)
        kpi_r2_c1.metric("Rata-rata Harga Jual", f"Rp {filtered_df['harga_satuan_transaksi'].mean():,.0f}")
        kpi_r2_c2.metric("Curah Hujan Rata-rata", f"{filtered_df['curah_hujan_mm'].mean():,.1f} mm")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Generate cached historical figures (Area Chart, Horizontal Bar, Donut Chart) ---
        fig_trend, fig_bar, fig_donut = generate_cached_historical_figures(filtered_df)

        # --- Row: trend + bar ---
        left, right = st.columns([3, 2])

        with left:
            if fig_trend is not None:
                st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

        with right:
            if fig_bar is not None:
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Row: donut + scatter ---
        left2, right2 = st.columns([2, 3])

        with left2:
            if fig_donut is not None:
                st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

        with right2:
            # Header & Mode Switcher
            r_head1, r_head2 = st.columns([1, 1])
            with r_head1:
                st.markdown('<div style="font-size:1.05rem; font-weight:700; color:#1a1a1a; padding-top:4px;">Evaluasi Harga vs Volume Pesanan</div>', unsafe_allow_html=True)
            with r_head2:
                chart_view = st.pills(
                    "Mode Tampilan",
                    options=["Sebaran & Korelasi", "Dinamika Bulanan (Dual-Axis)", "Rentang Variasi (Boxplot)"],
                    default="Sebaran & Korelasi",
                    label_visibility="collapsed"
                )

            sel_fokus = None
            if chart_view == "Sebaran & Korelasi":
                avail_komod = [k for k in ["GB Propunic", "GB Profeed", "GB Proquatic", "Pendawa Subur POC", "Compossap", "Agen Hayati (Trichogem / Methagem)"] if k in filtered_df["nama_komoditas"].unique()]
                if len(avail_komod) > 1:
                    fokus_opts = ["Bandingkan Semua Komoditas"] + avail_komod
                    sel_fokus = st.segmented_control(
                        "Fokus Komoditas:",
                        options=fokus_opts,
                        default="Bandingkan Semua Komoditas",
                        label_visibility="collapsed"
                    )
                elif len(avail_komod) == 1:
                    sel_fokus = avail_komod[0]

            fig_scatter = generate_cached_scatter_figure(filtered_df, chart_view, sel_fokus)
            if fig_scatter is not None:
                st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

            # Mini metrics badge for single SKU focus
            if chart_view == "Sebaran & Korelasi" and sel_fokus and sel_fokus != "Bandingkan Semua Komoditas":
                sub_data = filtered_df[filtered_df["nama_komoditas"] == sel_fokus]
                if not sub_data.empty and len(sub_data) > 1:
                    corr_val = sub_data["harga_satuan_transaksi"].corr(sub_data["volume_permintaan"])
                    st.markdown(f"""
                    <div style="display:flex; gap:10px; justify-content:center; font-size:0.85rem; font-weight:600; color:#1a1a1a; margin-top:-5px;">
                        <span class="neo-card" style="padding:4px 12px; margin:0;">Rata-rata Harga: <b>Rp {sub_data['harga_satuan_transaksi'].mean():,.0f}</b></span>
                        <span class="neo-card" style="padding:4px 12px; margin:0;">Rata-rata Pesanan: <b>{sub_data['volume_permintaan'].mean():,.1f}</b></span>
                        <span class="neo-card" style="padding:4px 12px; margin:0;">Koefisien Korelasi (r): <b>{corr_val:.3f}</b></span>
                    </div>
                    """, unsafe_allow_html=True)

        # --- Data table ---
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Log Transaksi Lapangan", expanded=False):
            show = filtered_df[
                ["tanggal_permintaan", "nama_komoditas", "volume_permintaan",
                 "harga_satuan_transaksi", "fase_musim", "curah_hujan_mm"]
            ].copy()
            show.columns = ["Tanggal Pesanan", "Nama Produk", "Jumlah Pesanan", "Harga Satuan Transaksi (Rp)", "Musim Tanam", "Curah Hujan (mm)"]
            st.dataframe(show.head(20), use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="neo-card-yellow" style="text-align:center;">
            <b style="font-size:1.1rem;">Data transaksi tidak ditemukan. Pastikan minimal satu komoditas tercentang pada panel kontrol sebelah kiri.</b>
        </div>
        """, unsafe_allow_html=True)
t_tab4_dur = (time.perf_counter() - t_tab4_start) * 1000

# ============================================================
# TAB 5 — PANDUAN DOSIS & SOP APLIKASI PRODUK MITRA
# ============================================================
with tab5:
    st.markdown("""
    <div class="neo-card-blue" style="padding:14px;">
        <b>Standar Operasional Prosedur (SOP) Aplikasi & Takaran Produk Lapangan</b><br>
        Petunjuk teknis resmi takaran pakai produk untuk perwakilan Kelompok Tani (Poktan) dan tim pendamping lapangan CV Pandawa Kencana Multifarm.
        Gunakan produk sesuai dosis label kemasan. Dilarang mencampur formula atau menaikkan dosis tanpa rekomendasi tertulis tim teknis.
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    dosis_rows = [
        ["GB Propunic (Pupuk Hayati Cair)", "Liter", "Dekomposisi pupuk kompos: 1 Liter untuk 1.000 Kg bahan organik. Perawatan septictank: 1 Kg/Liter per 1-2 m³ limbah."],
        ["GB Profeed (Nutrisi & Probiotik Ternak)", "Liter", "Sapi potong/perah: 0.3 - 0.5 Liter per 200 Kg konsentrat. Ayam/Bebek: 1 Liter per 400 Kg pakan. Fermentasi jerami: 3 Liter per 1 Ton jerami (siklus 6 hari)."],
        ["GB Proquatic (Biosecurity Tambak)", "Liter", "Persiapan dasar kolam: 5 - 6 Liter/Ha (rendam 7-10 hari). Pembentukan plankton pakan alami: 16 Liter/Ha/minggu."],
        ["Pendawa Subur POC (Pupuk Organik Cair)", "Liter", "Sayuran: 4 tutup botol per tangki 14 Liter air. Tanaman buah/umbi: 5 tutup per tangki 14 Liter air. Tembakau: 10 tutup per tangki semprot."],
        ["Compossap (Pupuk Organik Padat)", "Zak (50 Kg)", "Tanaman Padi: 1 - 2 Ton/Ha sebelum tanam. Tanaman Cabai: 4 - 5 Ons/lubang tanam. Jeruk/Kopi/Sawit: 5 Kg/pohon (aplikasi tiap 6 bulan)."],
        ["Agen Hayati (Trichogem & Methagem)", "Saset / Kg", "Larutkan 100 gram per tangki semprot untuk pencegahan jamur Fusarium, Phytophthora, dan wereng coklat pada tanaman cabai/padi."]
    ]
    st.dataframe(
        pd.DataFrame(dosis_rows, columns=["Produk", "Satuan Resmi", "Panduan Pemakaian Lapangan"]),
        use_container_width=True,
        hide_index=True,
    )

t_rerun_end = time.perf_counter()
print(f"[PERF LOG] Script execution latency: {(t_rerun_end - t_rerun_start)*1000:.1f}ms | Pred: {t_pred_dur:.1f}ms | Tab1: {t_tab1_dur:.1f}ms | Tab2: {t_tab2_dur:.1f}ms | Tab3: {t_tab3_dur:.1f}ms | Tab4: {t_tab4_dur:.1f}ms (simulasi_harga={simulasi_harga})", flush=True)

