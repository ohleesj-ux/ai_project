
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# ---------------------------
# 한글 폰트 설정
# ---------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ---------------------------
# 데이터 불러오기
# ---------------------------
df = pd.read_csv("population.csv", encoding="cp949")

# 불필요한 컬럼 제거 및 컬럼 정리
df.columns = [col.strip() for col in df.columns]

# 자치구 컬럼명 찾기
region_col = df.columns[0]

# 연령 컬럼 추출
age_columns = df.columns[3:]

# 숫자형 변환
for col in age_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(int)
    )

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("서울시 자치구별 연령 인구 분석")

districts = df[region_col].tolist()

selected_region = st.selectbox(
    "행정구를 선택하세요",
    districts
)

# 선택된 행정구 데이터
selected_data = df[df[region_col] == selected_region]

# 연령 / 인구 추출
ages = list(range(len(age_columns)))
population = selected_data.iloc[0, 3:].values

# ---------------------------
# 그래프
# ---------------------------
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    ages,
    population,
    color="hotpink",
    linewidth=2.5
)

# 제목 및 라벨
ax.set_title(f"{selected_region} 연령별 인구수", fontsize=16)
ax.set_xlabel("나이", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)

# x축 10살 단위 구분선
ax.set_xticks(range(0, len(age_columns), 10))
ax.grid(axis='x', linestyle='--', alpha=0.5)

# 보기 좋게
plt.tight_layout()

# 출력
st.pyplot(fig)
