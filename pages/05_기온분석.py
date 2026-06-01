import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    df = pd.read_csv("seoul.csv", encoding="cp949")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 변환 실패 행 제거
    df = df.dropna(subset=["날짜"])

    # 연도, 월, 일 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df


df = load_data()

# ------------------------
# 기온 컬럼 자동 찾기
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
    st.stop()

# ------------------------
# 제목
# ------------------------
st.title("🌡️ 서울 기온 분석")
st.write("월과 일을 선택하면 해당 날짜의 연도별 최고기온·최저기온 변화를 확인할 수 있습니다.")

# ------------------------
# 월 선택
# ------------------------
month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

# ------------------------
# 해당 월의 일만 표시
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
    (df["월"] == month)
    & (df["일"] == day)
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
    f"{month}월 {day}일 연도별 최고기온·최저기온 변화"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")

ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# ------------------------
# 기록 표시
# ------------------------
st.subheader("📌 역대 기록")

col1, col2 = st.columns(2)

with col1:
    max_temp = filtered[max_col].max()
    max_year = filtered.loc[
        filtered[max_col].idxmax(),
        "연도"
    ]

    st.metric(
        "역대 최고기온",
        f"{max_temp:.1f}℃",
        f"{int(max_year)}년"
    )

with col2:
    min_temp = filtered[min_col].min()
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
