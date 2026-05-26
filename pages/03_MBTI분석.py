import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="국가별 MBTI 비율 분석",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.write("국가를 선택하면 MBTI 비율을 막대그래프로 확인할 수 있어요.")

# 데이터 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# 첫 번째 컬럼 = 국가명
country_col = df.columns[0]

# MBTI 컬럼들
mbti_cols = df.columns[1:]

# 국가 선택
country = st.selectbox(
    "국가를 선택하세요",
    sorted(df[country_col].unique())
)

# 선택한 국가 데이터
selected_row = df[df[country_col] == country].iloc[0]

# MBTI 데이터프레임 생성
mbti_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "비율": [selected_row[col] for col in mbti_cols]
})

# 내림차순 정렬
mbti_df = mbti_df.sort_values(by="비율", ascending=False)

# 색상 설정
colors = []

for i in range(len(mbti_df)):
    if i == 0:
        colors.append("#FFD700")  # 1위 노란색
    else:
        opacity = max(0.2, 1 - (i * 0.05))
        colors.append(f"rgba(135,206,235,{opacity})")

# 그래프 생성
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=mbti_df["MBTI"],
        y=mbti_df["비율"],
        marker_color=colors,
        text=mbti_df["비율"].round(2),
        textposition="outside"
    )
)

fig.update_layout(
    title=f"{country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# 최고 비율 MBTI
top_mbti = mbti_df.iloc[0]

st.success(
    f"✨ {country}에서 가장 높은 MBTI는 "
    f"{top_mbti['MBTI']} ({top_mbti['비율']:.2f}%) 입니다."
)
