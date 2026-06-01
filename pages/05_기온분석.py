import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# ------------------------
# 페이지 설정
# ------------------------
st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

# ------------------------
# 한글 설정
# ------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ------------------------
# 데이터 불러오기
# ------------------------
@st.cache_data
def load_data():

    # UTF-8 실패 시 CP949 시도
    try:
        df = pd.read_csv("seoul.csv", encoding="utf-8")
    except:
        df = pd.read_csv("seoul.csv", encoding="cp949")

    # 날짜 컬럼 찾기
    date_col = None
    for col in df.columns:
        if "날짜" in col:
            date_col = col
            break

    if date_col is None:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.stop()

    # 날짜 변환
    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    df = df.dropna(subset=[date_col])

    # 연월일 생성
    df["연도"] = df[date_col].dt.year
    df["월"] = df[date_col].dt.month
    df["일"] = df[date_col].dt.day

    return df

df = load_data()

# ------------------------
# 기온 컬럼 자동 탐색
# ------------------------
max_col = None
min_col = None

for col in df.columns:
    if "최고기온" in col:
        max_col = col

    if "최저기온" in col:
        min_col = col

if max_col is None or min_col is None:
    st.error("최고기온 또는 최저기온 컬럼을 찾을 수 없습니다.")
    st.write("현재 컬럼 목록")
    st.write(df.columns.tolist())
    st.stop()

# 숫자형 변환
df[max_col] = pd.to_numeric(df[max_col], errors="coerce")
df[min_col] = pd.to_numeric(df[min_col], errors="coerce")

# ------------------------
# 제목
# ------------------------
st.title("🌡️ 서울 기온 분석")

st.write(
    "월과 일을 선택하면 해당 날짜의 연도별 최고기온·최저기온을 확인할 수 있습니다."
)

# ------------------------
# 월 선택
# ------------------------
month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

# ------------------------
# 일 선택
# ------------------------
available_days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    available_days
)

# ------------------------
# 데이터 필터링
# ------------------------
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

# ------------------------
# 그래프
# ------------------------
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
ax.grid(True)

st.pyplot(fig)

# ------------------------
# 미래 예측
# ------------------------
st.subheader("🔮 미래 기온 예측")

future_year = st.number_input(
    "예측할 미래 연도",
    min_value=int(filtered["연도"].max()) + 1,
    max_value=2100,
    value=2030
)

predict_df = filtered[
    ["연도", max_col, min_col]
].copy()

predict_df = predict_df.dropna()

if len(predict_df) >= 2:

    X = predict_df["연도"].values.reshape(-1, 1)

    # 최고기온 모델
    max_model = LinearRegression()
    max_model.fit(
        X,
        predict_df[max_col]
    )

    pred_max = max_model.predict(
        np.array([[future_year]])
    )[0]

    # 최저기온 모델
    min_model = LinearRegression()
    min_model.fit(
        X,
        predict_df[min_col]
    )

    pred_min = min_model.predict(
        np.array([[future_year]])
    )[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "예상 최고기온",
            f"{pred_max:.1f}℃"
        )

    with col2:
        st.metric(
            "예상 최저기온",
            f"{pred_min:.1f}℃"
        )

else:
    st.warning("예측에 사용할 데이터가 부족합니다.")

# ------------------------
# 역대 기록
# ------------------------
st.subheader("📌 역대 기록")

record_col1, record_col2 = st.columns(2)

with record_col1:

    valid_max = filtered[max_col].dropna()

    if len(valid_max) > 0:
        max_temp = valid_max.max()

        max_year = filtered.loc[
            filtered[max_col].idxmax(),
            "연도"
        ]

        st.metric(
            "역대 최고기온",
            f"{max_temp:.1f}℃",
            f"{int(max_year)}년"
        )

with record_col2:

    valid_min = filtered[min_col].dropna()

    if len(valid_min) > 0:
        min_temp = valid_min.min()

        min_year = filtered.loc[
            filtered[min_col].idxmin(),
            "연도"
        ]

        st.metric(
            "역대 최저기온",
            f"{min_temp:.1f}℃",
            f"{int(min_year)}년"
        )

# ------------------------
# 데이터 표
# ------------------------
st.subheader("📋 데이터")

st.dataframe(
    filtered[
        ["연도", min_col, max_col]
    ],
    use_container_width=True
)
