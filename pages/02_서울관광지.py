import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🌏",
    layout="wide"
)

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("Folium 지도를 활용하여 서울의 대표 관광지를 표시합니다.")

# 관광지 데이터
tourist_spots = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "description": "조선 시대의 대표 궁궐"
    },
    {
        "name": "N서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "description": "서울 야경 명소"
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "description": "쇼핑과 길거리 음식의 중심지"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "description": "전통 한옥 거리"
    },
    {
        "name": "홍대거리",
        "lat": 37.556336,
        "lon": 126.922647,
        "description": "젊음과 예술의 거리"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.513068,
        "lon": 127.102486,
        "description": "서울 랜드마크 초고층 빌딩"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566526,
        "lon": 127.009223,
        "description": "현대적 건축 명소"
    },
    {
        "name": "인사동",
        "lat": 37.574019,
        "lon": 126.986647,
        "description": "전통 문화와 기념품 거리"
    },
    {
        "name": "한강공원",
        "lat": 37.528316,
        "lon": 126.932598,
        "description": "서울 시민들의 대표 휴식 공간"
    },
    {
        "name": "코엑스 별마당도서관",
        "lat": 37.510215,
        "lon": 127.059207,
        "description": "SNS 인기 실내 관광 명소"
    }
]

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]

# Folium 지도 생성
m = folium.Map(
    location=seoul_center,
    zoom_start=11,
    tiles="OpenStreetMap"
)

# 마커 클러스터 추가
marker_cluster = MarkerCluster().add_to(m)

# 관광지 마커 추가
for idx, spot in enumerate(tourist_spots, start=1):

    popup_html = f"""
    <h4>{idx}. {spot['name']}</h4>
    <p>{spot['description']}</p>
    """

    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=spot["name"],
        icon=folium.Icon(
            color="red",
            icon="star"
        )
    ).add_to(marker_cluster)

# 지도 출력
st_data = st_folium(
    m,
    width=1200,
    height=700
)

# 관광지 리스트 출력
st.subheader("📍 서울 관광지 리스트")

for idx, spot in enumerate(tourist_spots, start=1):
    st.markdown(
        f"""
        **{idx}. {spot['name']}**  
        - {spot['description']}
        """
    )

st.success("Streamlit Cloud에서 바로 실행 가능한 앱입니다.")
