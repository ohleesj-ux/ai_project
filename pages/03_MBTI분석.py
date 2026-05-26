import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="국가별 MBTI 분석",
    layout="wide"
)

st.title("🌍 국가별 MBTI 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
df = pd.read_csv("countriesMBTI_16types.csv")

# 첫 번째 컬럼 = 국가명
country_col = df.columns[0]

# MBTI 컬럼
mbti_cols = df.columns[1:]

# -----------------------------
# 메뉴 선택
# -----------------------------
menu = st.radio(
    "분석 종류 선택",
    ["국가별 MBTI 비율", "MBTI별 상위 국가"]
)

# =====================================================
# 1. 국가 선택 → MBTI 비율
# =====================================================
if menu == "국가별 MBTI 비율":

    st.subheader("📊 국가별 MBTI 비율")

    # 국가 선택
    country = st.selectbox(
        "국가를 선택하세요",
        sorted(df[country_col].unique())
    )

    # 선택 국가 데이터
    selected_row = df[df[country_col] == country].iloc[0]

    # 데이터프레임 생성
    mbti_df = pd.DataFrame({
        "MBTI": mbti_cols,
        "비율": [selected_row[col] for col in mbti_cols]
    })

    # 높은 순 정렬
    mbti_df = mbti_df.sort_values(
        by="비율",
        ascending=False
    )

    # -----------------------------
    # 색상 설정 (분홍색 그라데이션)
    # -----------------------------
    colors = []

    for i in range(len(mbti_df)):
        if i == 0:
            colors.append("#ff4fa3")  # 1등 진한 핑크
        else:
            opacity = max(0.2, 1 - (i * 0.05))
            colors.append(f"rgba(255,105,180,{opacity})")

    # -----------------------------
    # 그래프 생성
    # -----------------------------
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
        title=f"{country} MBTI 비율 순위",
        xaxis_title="MBTI",
        yaxis_title="비율 (%)",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # 1등 출력
    top_mbti = mbti_df.iloc[0]

    st.success(
        f"🏆 {country}에서 가장 높은 MBTI는 "
        f"{top_mbti['MBTI']} "
        f"({top_mbti['비율']:.2f}%) 입니다."
    )

# =====================================================
# 2. MBTI 선택 → 상위 국가 TOP 10
# =====================================================
elif menu == "MBTI별 상위 국가":

    st.subheader("🌎 MBTI별 상위 국가 TOP 10")

    # MBTI 선택
    selected_mbti = st.selectbox(
        "MBTI를 선택하세요",
        mbti_cols
    )

    # 국가 + 선택 MBTI 비율
    top_df = df[[country_col, selected_mbti]].copy()

    # 컬럼명 변경
    top_df.columns = ["국가", "비율"]

    # 내림차순 정렬
    top_df = top_df.sort_values(
        by="비율",
        ascending=False
    ).head(10)

    # -----------------------------
    # 색상 설정
    # -----------------------------
    colors = []

    for i in range(len(top_df)):
        if i == 0:
            colors.append("#ff4fa3")
        else:
            opacity = max(0.2, 1 - (i * 0.08))
            colors.append(f"rgba(255,105,180,{opacity})")

    # -----------------------------
    # 그래프 생성
    # -----------------------------
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=top_df["국가"],
            y=top_df["비율"],
            marker_color=colors,
            text=top_df["비율"].round(2),
            textposition="outside"
        )
    )

    fig.update_layout(
        title=f"{selected_mbti} 비율이 높은 국가 TOP 10",
        xaxis_title="국가",
        yaxis_title="비율 (%)",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # 1등 국가
    top_country = top_df.iloc[0]

    st.success(
        f"🏆 {selected_mbti} 비율이 가장 높은 국가는 "
        f"{top_country['국가']} "
        f"({top_country['비율']:.2f}%) 입니다."
    )
