import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# -------------------------
# 한글 설정
# -------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# -------------------------
# 데이터 불러오기
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    df["날짜"] = pd.to_datetime(df["날짜"])
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

st.title("서울 기온 변화 분석")

# -------------------------
# 월, 일 선택
# -------------------------
col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "월 선택",
        sorted(df["월"].unique())
    )

available_days = sorted(
    df[df["월"] == selected_month]["일"].unique()
)

with col2:
    selected_day = st.selectbox(
        "일 선택",
        available_days
    )

# -------------------------
# 선택 날짜 데이터
# -------------------------
filtered = df[
    (df["월"] == selected_month)
    & (df["일"] == selected_day)
].copy()

filtered = filtered.sort_values("연도")

# -------------------------
# 그래프
# -------------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    filtered["연도"],
    filtered["최고기온(℃)"],
    color="red",
    label="최고기온",
    linewidth=2
)

ax.plot(
    filtered["연도"],
    filtered["최저기온(℃)"],
    color="blue",
    label="최저기온",
    linewidth=2
)

ax.set_title(
    f"{selected_month}월 {selected_day}일 연도별 최고·최저기온 변화",
    fontsize=14
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")
ax.legend()

ax.grid(True, alpha=0.3)

st.pyplot(fig)

# -------------------------
# 데이터 표
# -------------------------
st.subheader("선택 날짜 데이터")

st.dataframe(
    filtered[
        ["연도", "최저기온(℃)", "최고기온(℃)"]
    ],
    use_container_width=True
)
