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

st.title("🚇 서울시 지하철 호선별 역 이용객 분석")
st.markdown("### 호선을 선택하면 역별 이용객 TOP10과 비교 분석을 확인할 수 있습니다.")

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

# 컬럼 정리
df.columns = df.columns.str.strip()

# 총 승객수
df["총승객수"] = df["승차총승객수"] + df["하차총승객수"]

# -----------------------
# 호선 선택
# -----------------------
line_list = sorted(df["호선명"].unique())

selected_line = st.selectbox(
    "🚉 지하철 호선을 선택하세요",
    line_list
)

# -----------------------
# 선택 호선 데이터
# -----------------------
line_df = df[df["호선명"] == selected_line]

# 역별 집계
station_df = (
    line_df.groupby("역명")["총승객수"]
    .sum()
    .reset_index()
)

# 정렬
station_df = station_df.sort_values("총승객수", ascending=False)

# TOP10
station_top10 = station_df.head(10)

# -----------------------
# 1위 / 10위 / 평균
# -----------------------
top_station = station_top10.iloc[0]
bottom_station = station_top10.iloc[-1]
avg_value = station_top10["총승객수"].mean()

diff = top_station["총승객수"] - bottom_station["총승객수"]

# -----------------------
# 핵심 요약 카드
# -----------------------
st.subheader("📌 핵심 요약")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🥇 1위 역", top_station["역명"])

with col2:
    st.metric("🥉 10위 역", bottom_station["역명"])

with col3:
    st.metric("📊 평균 이용객", f"{int(avg_value):,}명")

st.info(f"📊 1위와 10위 차이: {diff:,}명")

# -----------------------
# TOP10 그래프
# -----------------------
st.subheader("📊 역별 이용객 TOP10")

fig = px.bar(
    station_top10,
    x="역명",
    y="총승객수",
    title=f"{selected_line} TOP10 역 이용객"
)

fig.update_layout(
    font=dict(family="Malgun Gothic"),
    height=500,
    xaxis_title="역명",
    yaxis_title="총승객수"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 순위 카드형 비교
# -----------------------
st.subheader("🏆 TOP10 순위 비교")

medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7

for i, row in enumerate(station_top10.itertuples(), start=0):
    st.markdown(
        f"""
        ### {medals[i]} {i+1}위 : {row.역명}
        **{row.총승객수:,}명**
        """
    )

# -----------------------
# 비교 분석
# -----------------------
st.subheader("📊 역별 비교 분석")

st.warning(
    f"🥇 1위 역 '{top_station['역명']}'과 "
    f"🥉 10위 역 '{bottom_station['역명']}'의 차이는 "
    f"{diff:,}명입니다."
)

st.info(
    f"📌 평균 대비 1위 역은 "
    f"{top_station['총승객수'] - avg_value:,.0f}명 더 많습니다."
)

# -----------------------
# 전체 순위 테이블
# -----------------------
st.subheader("📋 전체 순위")

table_df = station_top10.copy()
table_df.insert(0, "순위", range(1, len(table_df) + 1))

table_df = table_df.rename(columns={
    "역명": "지하철역",
    "총승객수": "승객수"
})

table_df["승객수"] = table_df["승객수"].apply(lambda x: f"{x:,}")

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------
# 설명
# -----------------------
st.success(
    f"🚇 {selected_line}에서 가장 이용객이 많은 역은 "
    f"'{top_station['역명']}'이며 "
    f"{diff:,}명 차이로 다른 역들과 차이가 있습니다."
)
