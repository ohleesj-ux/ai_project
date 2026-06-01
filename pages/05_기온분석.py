import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

# 한글 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    df = df.dropna(subset=["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# 최고·최저기온 컬럼 자동 탐색
max_col = None
min_col = None

for col in df.columns:
    if "최고기온" in col:
        max_col = col

    if "최저기온" in col:
        min_col = col

if max_col is None or min_col is None:
    st.error("최고기온 또는 최저기온 컬럼을 찾을 수 없습니다.")
    st.stop()

st.title("🌡️ 서울 기온 분석")

month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

available_days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    available_days
)

filtered = df[
    (df["월"] == month)
    & (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

if len(filtered) < 2:
    st.warning("예측에 필요한 데이터가 부족합니다.")
    st.stop()

# ------------------
# 그래프
# ------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    filtered["연도"],
    filtered[max_col],
    color="red",
    linewidth=2,
    label="최고기온"
)

ax.plot(
    filtered["연도"],
    filtered[min_col],
    color="blue",
    linewidth=2,
    label="최저기온"
)

ax.set_title(
    f"{month}월 {day}일 연도별 최고기온·최저기온"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# ------------------
# 미래 기온 예측
# ------------------
st.subheader("🔮 미래 기온 예측")

future_year = st.number_input(
    "예측할 연도",
    min_value=int(filtered["연도"].max()) + 1,
    max_value=2100,
    value=2030
)

X = filtered["연도"].values.reshape(-1, 1)

# 최고기온 모델
max_model = LinearRegression()
max_model.fit(X, filtered[max_col])

pred_max = max_model.predict(
    np.array([[future_year]])
)[0]

# 최저기온 모델
min_model = LinearRegression()
min_model.fit(X, filtered[min_col])

pred_min = min_model.predict(
    np.array([[future_year]])
)[0]

st.success(
    f"{future_year}년 {month}월 {day}일 예상 최고기온: {pred_max:.1f}℃"
)

st.info(
    f"{future_year}년 {month}월 {day}일 예상 최저기온: {pred_min:.1f}℃"
)

# ------------------
# 기록
# ------------------
st.subheader("📌 역대 기록")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "역대 최고기온",
        f"{filtered[max_col].max():.1f}℃"
    )

with col2:
    st.metric(
        "역대 최저기온",
        f"{filtered[min_col].min():.1f}℃"
    )

# 데이터 표
st.subheader("📋 데이터")

st.dataframe(
    filtered[
        ["연도", min_col, max_col]
    ],
    use_container_width=True
)
