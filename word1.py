import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("world-happiness-2024.csv")
    df.columns = [col.replace('Explained by: ', '').replace(' ', '_').lower() for col in df.columns]
    df = df.rename(columns={'country_name': 'Country', 'ladder_score': 'Happiness_Score'})
    return df

df = load_data()

st.title("🌍 2024 World Happiness Dashboard")
st.markdown("📊 세계 행복지수를 다양한 시각으로 한눈에 분석합니다.")

# -------------------- 1. 지도 --------------------
st.subheader("🗺️ 국가별 행복 점수 지도")
fig_map = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Happiness_Score",
    hover_name="Country",
    color_continuous_scale="YlGnBu",
    title="2024 세계 행복 점수"
)
st.plotly_chart(fig_map, use_container_width=True)

# -------------------- 2. 상위 국가 그래프 --------------------
st.subheader("🏆 행복 점수 상위 10개국")
top10 = df.sort_values("Happiness_Score", ascending=False).head(10)
fig_bar = px.bar(
    top10,
    x="Happiness_Score",
    y="Country",
    orientation="h",
    color="Happiness_Score",
    color_continuous_scale="Blues",
    title="Top 10 Happiest Countries"
)
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------- 3. 상관관계 분석 --------------------
st.subheader("📈 행복 점수와 요인 간 관계")
numeric_cols = ["Happiness_Score", "log_gdp_per_capita", "social_support",
                "healthy_life_expectancy", "freedom_to_make_life_choices",
                "generosity", "perceptions_of_corruption"]

selected_x = st.selectbox("X축 변수 선택", numeric_cols, index=1)
selected_y = st.selectbox("Y축 변수 선택", numeric_cols, index=0)

fig_corr = px.scatter(
    df,
    x=selected_x,
    y=selected_y,
    text="Country",
    trendline="ols",
    title=f"{selected_x} vs {selected_y}"
)
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("📌 선형 추세선을 통해 변수 간 관계를 시각적으로 파악할 수 있습니다.")
