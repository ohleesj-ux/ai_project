import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform

st.set_page_config(
    page_title="서울시 지하철 이용객 분석",
    layout="wide"
)

# 한글 깨짐 방지
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
elif platform.system() == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"
else:
    plt.rcParams["font.family"] = "NanumGothic"

plt.rcParams["axes.unicode_minus"] = False

st.title("🚇 서울시 지하철 호선별 역별 승하차 인원 분석")

# CSV 자동 불러오기
@st.cache_data
def load_data():
    return pd.read_csv(
        "서울시 지하철호선별 역별 승하차 인원 정보.csv",
        encoding="cp949"
    )

df = load_data()

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 총 승객수 계산
df["총승객수"] = (
    df["승차총승객수"] +
    df["하차총승객수"]
)

# 호선 선택
line_list = sorted(df["호선명"].unique())

selected_line = st.selectbox(
    "지하철 호선을 선택하세요",
    line_list
)

# 선택한 호선 데이터
line_df = df[df["호선명"] == selected_line]

# 역별 승객수 집계
station_df = (
    line_df.groupby("역명")["총승객수"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.subheader(f"🚉 {selected_line} 역별 승하차 인원")

fig, ax = plt.subplots(figsize=(15, 6))

ax.plot(
    station_df["역명"],
    station_df["총승객수"],
    color="hotpink",
    linewidth=3,
    marker="o"
)

ax.set_title(f"{selected_line} 역별 승하차 인원")
ax.set_xlabel("지하철역")
ax.set_ylabel("승객수")

# 인구(승객수) 단위 구분선
ax.grid(
    True,
    axis="y",
    linestyle="--",
    alpha=0.6
)

plt.xticks(rotation=90)

st.pyplot(fig)

st.subheader("📊 역별 승객수 데이터")

st.dataframe(
    station_df.rename(
        columns={
            "역명": "지하철역",
            "총승객수": "승객수"
        }
    ),
    use_container_width=True
)
