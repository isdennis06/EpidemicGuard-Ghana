import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="EpidemicGuard Ghana",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# PROFESSIONAL DARK THEME
# ==========================================================

st.markdown("""
<style>

/* Main App */
.stApp{
    background:linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#111827;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Headers */

.header{
    font-size:3rem;
    text-align:center;
    font-weight:800;
    background:linear-gradient(to right,#38bdf8,#818cf8);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subheader{
    text-align:center;
    color:#cbd5e1;
    font-size:1.2rem;
}

/* Metric Cards */

[data-testid="stMetric"]{
    background:#1e293b;
    border-radius:15px;
    padding:18px;
    border:1px solid #334155;
    box-shadow:0px 5px 15px rgba(0,0,0,.35);
}

[data-testid="stMetricLabel"]{
    color:#94a3b8 !important;
}

[data-testid="stMetricValue"]{
    color:white !important;
    font-size:30px;
}

/* Buttons */

.stButton button{
    background:#2563eb;
    color:white;
    border:none;
    border-radius:8px;
    font-weight:bold;
}

.stButton button:hover{
    background:#3b82f6;
}

/* Radio */

.stRadio label{
    color:white !important;
}

/* Tabs */

button[data-baseweb="tab"]{
    font-weight:bold;
    color:#cbd5e1;
}

button[data-baseweb="tab"][aria-selected="true"]{
    color:#38bdf8 !important;
}

/* Dataframe */

div[data-testid="stDataFrame"]{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# TITLE
# ==========================================================

st.markdown(
    '<h1 class="header">🦠 EpidemicGuard Ghana</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subheader">Disease Outbreak Early Warning & Pattern Recognition Dashboard</p>',
    unsafe_allow_html=True
)

# ==========================================================
# GHANA REGIONS
# ==========================================================

REGIONS = [
    "Ahafo",
    "Ashanti",
    "Bono",
    "Bono East",
    "Central",
    "Eastern",
    "Greater Accra",
    "North East",
    "Northern",
    "Oti",
    "Savannah",
    "Upper East",
    "Upper West",
    "Volta",
    "Western",
    "Western North"
]

# ==========================================================
# DATA GENERATION
# ==========================================================

@st.cache_data(show_spinner=False)
def load_data():

    np.random.seed(42)

    dates = pd.date_range(
        end=datetime.today(),
        periods=120
    )

    data = []

    for region in REGIONS:

        base = np.random.randint(50,150)

        trend = np.random.uniform(0.95,1.05)

        for i,date in enumerate(dates):

            seasonal = np.sin(i/8)*8

            noise = np.random.randint(-5,6)

            cases = max(
                5,
                int(base*trend + seasonal + noise)
            )

            data.append({

                "date":date,
                "region":region,
                "new_cases":cases

            })

    df = pd.DataFrame(data)

    df.sort_values(
        ["region","date"],
        inplace=True
    )

    df["weekly_growth"] = (
        df.groupby("region")["new_cases"]
        .pct_change(7)
        *100
    )

    df["moving_average"] = (
        df.groupby("region")["new_cases"]
        .transform(lambda x: x.rolling(7).mean())
    )

    return df

df = load_data()
# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("⚙ Dashboard Filters")

selected_regions = st.sidebar.multiselect(
    "🗺 Select Regions",
    REGIONS,
    default=REGIONS
)

start_date = st.sidebar.date_input(
    "📅 Start Date",
    value=df["date"].min().date()
)

end_date = st.sidebar.date_input(
    "📅 End Date",
    value=df["date"].max().date()
)

st.sidebar.divider()

st.sidebar.markdown("### 🌐 Project Links")

st.sidebar.link_button(
    "🚀 Live Dashboard",
    "https://epidemicguard-ghana.streamlit.app"
)

st.sidebar.link_button(
    "💻 GitHub Repository",
    "https://github.com/isdennis06/EpidemicGuard-Ghana"
)

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = df[
    (df["region"].isin(selected_regions))
    &
    (df["date"] >= pd.to_datetime(start_date))
    &
    (df["date"] <= pd.to_datetime(end_date))
]

latest = (
    filtered_df
    .sort_values("date")
    .groupby("region")
    .last()
    .reset_index()
)

# ==========================================================
# KPI CARDS
# ==========================================================

total_cases = int(filtered_df["new_cases"].sum())

average_cases = round(
    filtered_df["new_cases"].mean(),
    1
)

highest_region = latest.loc[
    latest["new_cases"].idxmax(),
    "region"
]

highest_cases = int(
    latest["new_cases"].max()
)

growth_rate = round(
    latest["weekly_growth"]
    .fillna(0)
    .max(),
    1
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🦠 Total Cases",
    f"{total_cases:,}"
)

col2.metric(
    "📊 Average Daily Cases",
    average_cases
)

col3.metric(
    "🔥 Highest Region",
    f"{highest_region} ({highest_cases})"
)

col4.metric(
    "📈 Highest Growth",
    f"{growth_rate}%"
)

# ==========================================================
# MAIN TABS
# ==========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🚨 Early Warning",
        "📊 Analytics",
        "🔍 Pattern Recognition",
        "🧠 Knowledge Quiz"
    ]
)
# ==========================================================
# TAB 1 - EARLY WARNING SYSTEM
# ==========================================================

with tab1:

    st.subheader("🚨 Disease Outbreak Early Warning")

    st.write(
        "The system monitors weekly disease growth and automatically classifies each region according to outbreak risk."
    )

    for _, row in latest.iterrows():

        growth = row["weekly_growth"]

        if pd.isna(growth):
            growth = 0

        if growth >= 25:

            st.error(
                f"🔴 HIGH RISK: {row['region']} | Weekly Growth: {growth:.1f}% | Immediate intervention recommended."
            )

        elif growth >= 10:

            st.warning(
                f"🟠 MODERATE RISK: {row['region']} | Weekly Growth: {growth:.1f}% | Monitor closely."
            )

        else:

            st.success(
                f"🟢 LOW RISK: {row['region']} | Weekly Growth: {growth:.1f}%"
            )

    st.divider()

    st.subheader("📋 Summary")

    high = (latest["weekly_growth"].fillna(0) >= 25).sum()
    medium = ((latest["weekly_growth"].fillna(0) >= 10) &
              (latest["weekly_growth"].fillna(0) < 25)).sum()
    low = (latest["weekly_growth"].fillna(0) < 10).sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("🔴 High Risk", high)
    c2.metric("🟠 Moderate Risk", medium)
    c3.metric("🟢 Low Risk", low)


# ==========================================================
# TAB 2 - ANALYTICS
# ==========================================================

with tab2:

    st.subheader("📊 Disease Trend Analytics")

    daily_cases = (
        filtered_df
        .groupby("date")["new_cases"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily_cases,
        x="date",
        y="new_cases",
        markers=True,
        title="National Daily Disease Cases"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Date",
        yaxis_title="Cases"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    fig2 = px.bar(
        latest.sort_values("new_cases", ascending=False),
        x="region",
        y="new_cases",
        color="new_cases",
        title="Latest Reported Cases by Region"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Region",
        yaxis_title="Cases"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    fig3 = px.pie(
        latest,
        names="region",
        values="new_cases",
        title="Distribution of Cases Across Regions"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )
    # ==========================================================
# TAB 3 - PATTERN RECOGNITION
# ==========================================================

with tab3:

    st.subheader("🔍 Pattern Recognition Engine")

    pattern_df = latest[
        [
            "region",
            "new_cases",
            "moving_average",
            "weekly_growth"
        ]
    ].copy()

    pattern_df["Risk Level"] = np.where(
        pattern_df["weekly_growth"] >= 25,
        "🔴 High",
        np.where(
            pattern_df["weekly_growth"] >= 10,
            "🟠 Medium",
            "🟢 Low"
        )
    )

    st.dataframe(
        pattern_df.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🔥 Hotspot Detection")

    hotspots = pattern_df[
        pattern_df["weekly_growth"] >= 25
    ]

    if hotspots.empty:

        st.success(
            "✅ No outbreak hotspots detected."
        )

    else:

        st.error(
            "⚠️ Potential outbreak hotspots detected:"
        )

        for _, row in hotspots.iterrows():

            st.markdown(
                f"""
**{row['region']}**

• Current Cases: **{int(row['new_cases'])}**

• Weekly Growth: **{row['weekly_growth']:.1f}%**

• Status: **High Risk**
"""
            )

    st.divider()

    st.subheader("📊 Weekly Growth Comparison")

    growth_chart = px.bar(
        pattern_df.sort_values(
            "weekly_growth",
            ascending=False
        ),
        x="region",
        y="weekly_growth",
        color="weekly_growth",
        title="Weekly Growth Rate by Region"
    )

    growth_chart.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        growth_chart,
        use_container_width=True
    )

    st.divider()

    st.subheader("💡 Automated Recommendations")

    if hotspots.empty:

        st.info(
            """
• Continue routine surveillance.

• Maintain disease prevention education.

• Encourage regular reporting from health facilities.
"""
        )

    else:

        st.warning(
            """
Recommended Actions

• Increase disease surveillance.

• Deploy rapid response teams.

• Intensify public awareness campaigns.

• Ensure hospitals are adequately supplied.

• Begin contact tracing where necessary.
"""
        )
        