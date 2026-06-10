import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# 페이지 설정
# -----------------------
st.set_page_config(
    page_title="서울시 지하철 이용객 분석",
    page_icon="🚇",
    layout="wide"
)

# -----------------------
# 제목
# -----------------------
st.title("🚇 서울시 지하철 호선별 역별 승하차 인원 분석")
st.markdown("### 호선을 선택하면 이용객이 가장 많은 TOP 10 역을 확인할 수 있습니다.")

# -----------------------
# 데이터 불러오기
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "서울시 지하철호선별 역별 승하차 인원 정보.csv",
        encoding="cp949"
    )

df = load_data()

# 컬럼명 정리
df.columns = df.columns.str.strip()

# 총 승객수 계산
df["총승객수"] = (
    df["승차총승객수"] +
    df["하차총승객수"]
)

# -----------------------
# 호선 선택
# -----------------------
line_list = sorted(df["호선명"].unique())

selected_line = st.selectbox(
    "🚉 지하철 호선을 선택하세요",
    line_list
)

# 선택한 호선 데이터
line_df = df[df["호선명"] == selected_line]

# -----------------------
# 역별 승객수 집계
# -----------------------
station_df = (
    line_df.groupby("역명")["총승객수"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# -----------------------
# 1위 역 정보
# -----------------------
top_station = station_df.iloc[0]["역명"]
top_count = station_df.iloc[0]["총승객수"]

st.metric(
    label="👑 이용객 1위 역",
    value=top_station,
    delta=f"{top_count:,}명"
)

# -----------------------
# 그래프
# -----------------------
fig = px.line(
    station_df,
    x="역명",
    y="총승객수",
    markers=True,
    title=f"{selected_line} 이용객 TOP 10 역"
)

# 핫핑크 색상
fig.update_traces(
    line_color="hotpink",
    marker=dict(size=10)
)

# 그래프 꾸미기
fig.update_layout(
    xaxis_title="지하철역",
    yaxis_title="승객수",
    hovermode="x unified",
    height=600
)

# 가로 구분선
fig.update_yaxes(
    showgrid=True,
    gridwidth=1
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------
# 순위표
# -----------------------
st.subheader("🏆 TOP 10 순위")

table_df = station_df.copy()

table_df.insert(
    0,
    "순위",
    range(1, len(table_df) + 1)
)

table_df.columns = [
    "순위",
    "지하철역",
    "승객수"
]

table_df["승객수"] = table_df["승객수"].apply(
    lambda x: f"{x:,}"
)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------
# 설명
# -----------------------
st.info(
    f"👑 {selected_line}에서 가장 이용객이 많은 역은 "
    f"'{top_station}'이며 총 {top_count:,}명이 이용했습니다."
)
