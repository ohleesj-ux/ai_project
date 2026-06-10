import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform

# -----------------------
# 페이지 설정
# -----------------------
st.set_page_config(
    page_title="서울시 지하철 이용객 분석",
    page_icon="🚇",
    layout="wide"
)

# -----------------------
# 한글 폰트 설정
# -----------------------
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
elif platform.system() == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"
else:
    plt.rcParams["font.family"] = "NanumGothic"

plt.rcParams["axes.unicode_minus"] = False

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

df.columns = df.columns.str.strip()

# 총 승객수
df["총승객수"] = (
    df["승차총승객수"] +
    df["하차총승객수"]
)

# -----------------------
# 호선 선택
# -----------------------
line_list = sorted(df["호선명"].unique())

selected_line = st.selectbox(
    "🚉 지하철 호선 선택",
    line_list
)

line_df = df[df["호선명"] == selected_line]

# -----------------------
# 역별 집계
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
st.subheader(f"📈 {selected_line} 이용객 TOP 10 역")

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    station_df["역명"],
    station_df["총승객수"],
    color="hotpink",
    marker="o",
    linewidth=3,
    markersize=8
)

# 숫자 표시
for i, v in enumerate(station_df["총승객수"]):
    ax.text(
        i,
        v,
        f"{v:,}",
        ha="center",
        va="bottom",
        fontsize=8
    )

# 1위 역 강조
ax.scatter(
    station_df.iloc[0]["역명"],
    station_df.iloc[0]["총승객수"],
    s=250,
    marker="*"
)

ax.set_title(
    f"{selected_line} 이용객 TOP 10 역",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("지하철역")
ax.set_ylabel("승객수")

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.6
)

plt.xticks(rotation=45)

st.pyplot(fig)

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
    f"{selected_line}에서 가장 이용객이 많은 역은 "
    f"'{top_station}'이며 총 {top_count:,}명이 이용했습니다."
)
