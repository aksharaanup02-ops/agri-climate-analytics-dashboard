import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page tab titles and layout initialization
st.set_page_config(page_title="Agricultural Climate Analytics Platform", layout="wide")

# Custom interface typography and layout presentation configurations
st.markdown("""
<style>
.main-title { font-size: 34px; font-weight: 800; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif; margin-bottom: 6px; }
.subtitle { font-size: 15px; color: #B0B0B0; font-family: 'Helvetica Neue', sans-serif; margin-bottom: 25px; }
.section-header { font-size: 22px; font-weight: 600; color: #FFFFFF; margin-top: 32px; margin-bottom: 16px; border-bottom: 1px solid #444; padding-bottom: 8px; }

/* High-contrast presentation container for regional field suggestions */
.precaution-card { background-color: #FFFFFF; padding: 26px; border-radius: 8px; border-left: 6px solid #FF4B4B; margin-bottom: 20px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3); }
.precaution-card b { color: #000000; font-size: 16px; }
.precaution-text { color: #111111; font-size: 15px; font-family: 'Helvetica Neue', sans-serif; line-height: 1.6; }

/* High-contrast status blocks for macro environmental impact descriptions */
.impact-good-card { background-color: #E6F4EA; padding: 22px; border-radius: 8px; border-left: 6px solid #137333; margin-bottom: 16px; }
.impact-bad-card { background-color: #FCE8E6; padding: 22px; border-radius: 8px; border-left: 6px solid #C5221F; margin-bottom: 16px; }
.impact-title { font-weight: 700; font-size: 16px; margin-bottom: 8px; }
.impact-desc { color: #202124; font-size: 14.5px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Agricultural Climate Analytics Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle"><b>Primary Objective:</b> Investigating how shifts in weather architectures directly impact structural crop outputs to aid regional decision-making.</div>', unsafe_allow_html=True)

# --- DATABASE HANDSHAKE AND AUTOMATED SCHEMA MAPPING ---
conn = sqlite3.connect("agri_database.db")

# Read a single sample row to extract exact database column case styles automatically
sample_df = pd.read_sql_query("SELECT * FROM crop_data LIMIT 1;", conn)
cols = sample_df.columns

# The layout pipeline scans structural column patterns to secure executions from system errors
db_year = [c for c in cols if 'year' in c.lower()][0]
db_crop = [c for c in cols if 'crop' in c.lower()][0]
db_rain = [c for c in cols if 'rain' in c.lower() or 'avg' in c.lower()][0]
db_yield = [c for c in cols if 'yield' in c.lower()][0]
db_temp = [c for c in cols if 'temp' in c.lower() or 'mean' in c.lower()][0]
db_state = [c for c in cols if 'state' in c.lower() or 'district' in c.lower()][0]
db_prod = [c for c in cols if 'produc' in c.lower()][0]

# --- CONTROL INTERFACE CONFIGURATION ---
st.sidebar.markdown("### Regional Configuration")
states_df = pd.read_sql_query(f"SELECT DISTINCT {db_state} FROM crop_data WHERE {db_state} IS NOT NULL ORDER BY {db_state};", conn)
selected_state = st.sidebar.selectbox("Select State or District", states_df[db_state])


# --- CORE ANALYTIC 1: REGIONAL CROP PRODUCTION BALANCE ANALYSIS ---
st.markdown(f'<div class="section-header">Crop Cultivation Profile: {selected_state}</div>', unsafe_allow_html=True)
st.markdown(f"This section isolates the structural breakdown of production volumes recorded within {selected_state} to determine local crop priorities.")

crop_query = f"SELECT {db_crop} as Crop, SUM({db_prod}) as Total_Production FROM crop_data WHERE {db_state} = '{selected_state}' GROUP BY Crop ORDER BY Total_Production DESC;"
state_crop_data = pd.read_sql_query(crop_query, conn)

fig_state_bar = px.bar(
state_crop_data,
x="Crop",
y="Total_Production",
labels={"Crop": "Crop Type", "Total_Production": "Total Production Volume"},
template="plotly_dark",
color="Total_Production",
color_continuous_scale="Tealrose"
)
fig_state_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False, margin=dict(t=10, b=10, l=10, r=10))
st.plotly_chart(fig_state_bar, use_container_width=True)


# --- ADAPTIVE INTERFACE 2: FIELD PRECAUTIONS AND SOIL MANAGEMENT SUGGESTIONS ---
st.markdown(f'<div class="section-header">Agricultural Precautions and Strategic Guidelines for {selected_state}</div>', unsafe_allow_html=True)
st.markdown(f"Recommended operational strategies designed to preserve soil matrix metrics and navigate climate volatility inside {selected_state}:")

st.markdown(f"""
<div class="precaution-card">
<span class="precaution-text">
<b>1. Targeted Soil Optimization:</b> Execute systematic testing protocols to map localized soil pH levels and underlying nutrient reserves before planting to prevent severe mineral depletion.<br><br>
<b>2. Climate-Adaptive Water Controls:</b> Calibrate sub-surface drainage maps and local irrigation frequencies to balance seasonal waterlogging threats during high-volume monsoons.<br><br>
<b>3. Specialized Crop Scouting:</b> Deploy field scouting loops tuned to regional ambient shifts to intercept and counter insect patterns before they compromise harvest fields.<br><br>
<b>4. Structural Crop Rotation:</b> Rotate heavy-nutrient feeding plants alongside deep-rooting leguminous variations to naturally rebuild organic soil compounds over time.<br><br>
<b>5. Micro-Weather Vigilance:</b> Coordinate fertilizer schedules with real-time geographic climate models to prevent applying nutrient top-dressings immediately preceding major storms.
</span>
</div>
""", unsafe_allow_html=True)


# --- CORE ANALYTIC 3: MULTI-AXIS WEATHER CORRELATION ENGINE ---
st.markdown(f'<div class="section-header">Climate and Weather Analytics: {selected_state}</div>', unsafe_allow_html=True)

st.markdown(f"### Climate Trends: Average Rainfall vs. Mean Temperature in {selected_state}")
st.markdown(f"Evaluating localized rain volumes and thermal variations side-by-side to understand environmental trends in {selected_state}.")

weather_query = f"SELECT {db_year} as Year, AVG({db_rain}) as Avg_Rainfall, AVG({db_temp}) as Avg_Temp FROM crop_data WHERE {db_state} = '{selected_state}' GROUP BY Year ORDER BY Year;"
weather_df = pd.read_sql_query(weather_query, conn)

fig_corr = make_subplots(specs=[[{"secondary_y": True}]])

fig_corr.add_trace(
go.Scatter(x=weather_df["Year"], y=weather_df["Avg_Rainfall"], name="Average Rainfall (mm)", line=dict(color="#00F0FF", width=3, shape='spline')),
secondary_y=False,
)
fig_corr.add_trace(
go.Scatter(x=weather_df["Year"], y=weather_df["Avg_Temp"], name="Mean Temperature (°C)", line=dict(color="#FFD700", width=3, dash='dash', shape='spline')),
secondary_y=True,
)

fig_corr.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend=dict(x=0.01, y=1.15, orientation="h"), margin=dict(t=20, b=20, l=10, r=10), xaxis=dict(showgrid=False))
fig_corr.update_yaxes(title_text="Average Rainfall (mm)", color="#00F0FF", showgrid=True, gridcolor="#2D2D2D", secondary_y=False)
fig_corr.update_yaxes(title_text="Mean Temperature (°C)", color="#FFD700", showgrid=False, secondary_y=True)
st.plotly_chart(fig_corr, use_container_width=True)


# --- DYNAMIC STRUCTURAL REPORTING PANELS ---
st.markdown(f"### Evaluating Climate Fluctuations and Field Balance in {selected_state}")

st.markdown(f"""
<div class="impact-good-card">
<div class="impact-title" style="color: #137333;">Positive Environmental Impacts (Favorable Conditions)</div>
<div class="impact-desc">
• <b>Optimized Moisture Reservoirs:</b> Balanced, predictable precipitation distributions maintain natural soil hydration tables, significantly dropping operational irrigation expenses for farmers.<br><br>
• <b>Thermal Lifecycle Acceleration:</b> Steady, moderate warm periods facilitate healthy vegetative respiration, allowing regional crops to scale optimal structural yields efficiently.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="impact-bad-card">
<div class="impact-title" style="color: #C5221F;">Negative Environmental Impacts (Adverse Conditions)</div>
<div class="impact-desc">
• <b>Nutrient Leaching and Erosion:</b> Extreme rain surges overload natural fields, causing subsoil waterlogging while washing out key chemical fertilizer additions.<br><br>
• <b>Thermal Stress and Evaporation:</b> Sustained spikes in seasonal temperatures rapidly elevate soil evaporation speeds, creating soil cracking risks and reducing plant development thresholds.
</div>
</div>
""", unsafe_allow_html=True)


# --- CORE ANALYTIC 4: THERMAL ANOMALY TIMELINE MATRIX ---
st.markdown(f"### Historical Temperature Risk Matrix for {selected_state}")
st.markdown(f"Tracking seasonal ambient shifts across separate historic cropping timelines inside {selected_state}.")

temp_query = f"SELECT {db_year} as Year, {db_crop} as Crop, AVG({db_temp}) as Avg_Temp FROM crop_data WHERE {db_state} = '{selected_state}' AND {db_temp} IS NOT NULL GROUP BY Year, Crop;"
temp_df = pd.read_sql_query(temp_query, conn)

temp_matrix = temp_df.pivot_table(index="Crop", columns="Year", values="Avg_Temp", aggfunc='mean').fillna(28.0)

fig_heat = px.imshow(temp_matrix, labels=dict(x="Timeline (Years)", y="Crop Type", color="Mean Temp (°C)"), color_continuous_scale="Magma", template="plotly_dark")
fig_heat.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=20, l=10, r=10))
st.plotly_chart(fig_heat, use_container_width=True)


# --- REPORT OUTCOME METRIC FOOTER ---
st.write("---")
st.markdown('<div class="section-header">Analytical Application and Stakeholder Utility Summaries</div>', unsafe_allow_html=True)

st.markdown(f"### Farmers in {selected_state}")
st.write(f"Provides empirical timing data to adjust planting periods, minimizing exposure to severe climate stress peaks.")

st.markdown(f"### Government Planning in {selected_state}")
st.write(f"Offers predictive tracking profiles to flag upcoming crop stress patterns early, ensuring resource deployments target the highest risk zones first.")

st.markdown(f"### Long-term Environmental Tracking")
st.write(f"Creates transparent history paths detailing how ongoing micro-climate baseline movements reshape regional agricultural safety profiles over the span of decades.")
# --- OPTION B: LIVE DATABASE PARTITION INSPECTOR (RAW AUDITING) ---
st.write("---")
with st.expander("Inspect Raw SQL Database Partition Matrix"):
    sample_raw_data = pd.read_sql_query(f"SELECT * FROM crop_data WHERE {db_state} = '{selected_state}' LIMIT 5;", conn)
    st.dataframe(sample_raw_data, use_container_width=True)
# Closing the file stream cleanly
conn.close()