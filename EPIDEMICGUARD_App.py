import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime


# ===================== CONFIG =====================

st.set_page_config(
    page_title="EpidemicGuard Ghana",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===================== PROFESSIONAL THEME =====================

st.markdown("""
<style>

/* Application background */
.stApp {
    background: linear-gradient(135deg,#e8eef7,#f8fafc);
}


/* All text */
.stMarkdown p,
.stText,
label,
p {
    color:#1e293b !important;
}


/* Headers */

.header {
    font-size:3rem;
    font-weight:800;
    color:#1e3a8a !important;
    text-align:center;
}


.subheader {
    font-size:1.3rem;
    color:#334155 !important;
    text-align:center;
}



/* KPI Cards */

[data-testid="stMetric"] {

    background:white;
    padding:20px;
    border-radius:15px;
    border:1px solid #cbd5e1;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);

}


[data-testid="stMetricLabel"] {

    color:#475569 !important;
    font-weight:700;

}


[data-testid="stMetricValue"] {

    color:#0f172a !important;
    font-size:35px;
    font-weight:800;

}



/* Sidebar */

section[data-testid="stSidebar"] {

    background:white;

}


section[data-testid="stSidebar"] * {

    color:#1e293b !important;

}



/* Buttons */

.stButton button {

    background:#1e3a8a;
    color:white !important;
    border-radius:10px;
    font-weight:700;

}


.stButton button:hover {

    background:#2563eb;

}



/* Radio buttons */

.stRadio label {

    color:#1e293b !important;

}


/* Tabs */

button[data-baseweb="tab"] {

    font-weight:700;

}


</style>

""", unsafe_allow_html=True)



# ===================== TITLE =====================


st.markdown(
    '<h1 class="header">EpidemicGuard Ghana 🦠</h1>',
    unsafe_allow_html=True
)


st.markdown(
    '<p class="subheader">National Disease Outbreak Early Warning & Pattern Recognition System</p>',
    unsafe_allow_html=True
)



# ===================== REGIONS =====================

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



# ===================== DATA =====================


@st.cache_data
def load_data():

    np.random.seed(42)

    dates = pd.date_range(
        end=datetime.today(),
        periods=120
    )

    data=[]


    for region in REGIONS:

        base=np.random.randint(20,100)


        for date in dates:

            cases=max(
                5,
                int(base*np.random.uniform(0.05,0.15))
            )


            data.append({

                "date":date,
                "region":region,
                "new_cases":cases

            })


    df=pd.DataFrame(data)


    df=df.sort_values(
        ["region","date"]
    )


    df["weekly_growth"]=(

        df.groupby("region")["new_cases"]
        .pct_change()
        *100

    )


    return df



df=load_data()



# ===================== SIDEBAR =====================


st.sidebar.header("⚙️ Dashboard Filters")


selected_regions=st.sidebar.multiselect(

    "🗺 Select Regions",

    REGIONS,

    default=REGIONS[:8]

)



start_date=st.sidebar.date_input(

    "Start Date",

    df.date.min()

)



end_date=st.sidebar.date_input(

    "End Date",

    df.date.max()

)

# ===================== PROJECT LINKS =====================

st.sidebar.divider()

st.sidebar.markdown("### 🔗 Project Links")

st.sidebar.link_button(
    "🌐 Live Dashboard",
    "https://epidemicguard-ghana.streamlit.app"
)

st.sidebar.link_button(
    "📂 GitHub Repository",
    "https://github.com/isdennis06/EpidemicGuard-Ghana"
)

filtered_df=df[

    (df.region.isin(selected_regions)) &
    (df.date>=pd.to_datetime(start_date)) &
    (df.date<=pd.to_datetime(end_date))

]



# ===================== KPI =====================


latest=(

filtered_df
.groupby("region")
.last()
.reset_index()

)



total_cases=int(

filtered_df.new_cases.sum()

)


average_cases=round(

filtered_df.new_cases.mean(),

1

)


highest_region=latest.loc[

latest.new_cases.idxmax(),

"region"

]


highest_cases=int(

latest.new_cases.max()

)


growth=round(

latest.weekly_growth.max(),

1

)



c1,c2,c3,c4=st.columns(4)


c1.metric(
"🦠 Total Cases",
f"{total_cases:,}"
)


c2.metric(
"📊 Average Daily",
average_cases
)


c3.metric(
"⚠️ Highest Region",
highest_region
)


c4.metric(
"📈 Growth Rate",
f"{growth}%"
)
# ===================== MAIN DASHBOARD TABS =====================

tab1, tab2, tab3, tab4 = st.tabs(
[
"🚨 Early Warning",
"📈 Analytics",
"🔍 Pattern Detection",
"🧠 Knowledge Quiz"
]
)



# ===================== EARLY WARNING =====================

with tab1:

    st.subheader("🚨 Outbreak Risk Monitoring")


    for _, row in latest.iterrows():

        risk = row.weekly_growth


        if risk > 25:

            st.error(
                f"🔴 HIGH RISK — {row.region} | Growth: {risk:.1f}%"
            )


        elif risk > 10:

            st.warning(
                f"🟠 WATCH — {row.region} | Growth: {risk:.1f}%"
            )


        else:

            st.success(
                f"🟢 Stable — {row.region}"
            )




# ===================== ANALYTICS =====================

with tab2:

    st.subheader("📈 Disease Trend Analytics")


    daily_cases=(

        filtered_df
        .groupby("date")
        .new_cases
        .sum()
        .reset_index()

    )


    line_chart=px.line(

        daily_cases,

        x="date",

        y="new_cases",

        title="National Daily Cases Trend"

    )


    line_chart.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        line_chart,
        use_container_width=True
    )



    bar_chart=px.bar(

        latest,

        x="region",

        y="new_cases",

        title="Latest Cases By Region"

    )


    bar_chart.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )





# ===================== PATTERN RECOGNITION =====================

with tab3:

    st.subheader(
        "🔍 Pattern Recognition Engine"
    )


    st.dataframe(

        latest[
            [
                "region",
                "new_cases",
                "weekly_growth"
            ]
        ].round(2),

        use_container_width=True,

        hide_index=True

    )


    st.info(
        "Regions above 25% weekly growth are flagged as potential outbreak areas."
    )





# ===================== QUIZ =====================

with tab4:

    st.subheader(
        "🧠 Epidemic Knowledge Quiz"
    )


    questions={

        "What does WHO stand for?":

        [
            "World Health Organization",
            "World Health Office",
            "World Human Organization"
        ],


        "What is an outbreak?":

        [
            "A sudden increase in disease cases",
            "A type of medicine",
            "A hospital building"
        ],


        "Which data helps predict disease spread?":

        [
            "Case trends over time",
            "Random guessing",
            "Population names only"
        ],


        "What does early warning mean?":

        [
            "Detecting risks before they become severe",
            "Ignoring disease data",
            "Stopping all hospitals"
        ]

    }



    score=0



    answers={}



    for i,(question,options) in enumerate(questions.items()):


        answers[question]=st.radio(

            question,

            options,

            key=f"question_{i}"

        )



    if st.button(
        "Submit Quiz",
        key="quiz_submit"
    ):


        for question in questions:

            if answers[question] == questions[question][0]:

                score += 1



        st.success(
            f"🎉 Your score: {score}/{len(questions)}"
        )





# ===================== FOOTER =====================

st.caption(
"Professional Public Health Dashboard | Ghana Focused | Systems Analysis Project"
)