mport pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="국가별 MBTI 비율 분석",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.write("국가를 선택하면 MBTI 비율을 막대그래프로 확인할 수 있어요.")

# CSV 파일 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# 국가 컬럼 자동 찾기
country_col = df.columns[0]

# MBTI 컬럼
mbti_cols = df.columns[1:]

# 국가 선택
country = st.selectbox(
    "국가를 선택하세요",
    sorted(df[country_col].unique())
)

# 선택한 국가 데이터
selected = df[df[country_col] == country].iloc[0]

# MBTI 데이터 정리
mbti_data = pd.DataFrame({
    "MBTI": mbti_cols,
    "비율": [selected[col] for col in mbti_cols]
})

# 내림차순 정렬
mbti_data = mbti_data.sort_values(by="비율", ascending=False)

# 색상 설정
colors = []

max_value = mbti_data["비율"].max()

for i, value in enumerate(mbti_data["비율"]):
    if i == 0:
        colors.append("#FFD700")  # 1등 노란색
    else:
        # 하늘색 그라데이션
        alpha = max(0.25, 1 - (i * 0.05))
        colors.append(f"rgba(135, 206, 235, {alpha})")

# 그래프 생성
fig = go.Figure()

fig.add_trace(go.Bar(
    x=mbti_data["MBTI"],
    y=mbti_data["비율"],
    marker_color=colors,
    text=mbti_data["비율"].round(2),
    textposition="outside"
))

fig.update_layout(
    title=f"{country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    height=600,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# 가장 높은 MBTI 출력
top_mbti = mbti_data.iloc[0]

st.success(
    f"✨ {country}에서 가장 높은 MBTI는 "
    f"**{top_mbti['MBTI']}** "
    f"({top_mbti['비율']:.2f}%) 입니다."
