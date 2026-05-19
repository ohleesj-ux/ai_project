# app.py

import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# ---------------------------------------------------
# 페이지 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🌏",
    layout="wide"
)

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("핑크 마커로 표시된 서울의 대표 관광지를 확인해보세요.")

# ---------------------------------------------------
# 관광지 데이터
# ---------------------------------------------------
tourist_spots = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "description": "조선 시대의 대표 궁궐",
        "subway": "경복궁역 (3호선)",
        "detail": """
- 광화문과 근정전 등 한국 전통 건축을 가까이에서 볼 수 있습니다.
- 한복 대여 후 사진 촬영을 즐기는 외국인 관광객이 많습니다.
- 근처 서촌 카페거리와 국립민속박물관까지 함께 관광하기 좋습니다.
"""
    },
    {
        "name": "N서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "description": "서울 야경 명소",
        "subway": "명동역 (4호선)",
        "detail": """
- 남산 케이블카를 타고 서울 전경을 감상할 수 있습니다.
- 사랑의 자물쇠 포토존이 유명합니다.
- 밤에는 서울의 화려한 야경을 볼 수 있는 대표 관광지입니다.
"""
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "description": "쇼핑과 길거리 음식의 중심지",
        "subway": "명동역 (4호선)",
        "detail": """
- 한국 화장품과 패션 쇼핑으로 유명한 거리입니다.
- 길거리 음식과 다양한 디저트를 맛볼 수 있습니다.
- 외국인을 위한 환전소와 글로벌 브랜드 매장이 많습니다.
"""
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "description": "전통 한옥 거리",
        "subway": "안국역 (3호선)",
        "detail": """
- 전통 한옥 골목길 산책이 유명합니다.
- 감성적인 카페와 공방 체험을 즐길 수 있습니다.
- 한국 전통문화를 느끼기에 좋은 장소입니다.
"""
    },
    {
        "name": "홍대거리",
        "lat": 37.556336,
        "lon": 126.922647,
        "description": "젊음과 예술의 거리",
        "subway": "홍대입구역 (2호선)",
        "detail": """
- 버스킹 공연과 스트리트 문화를 경험할 수 있습니다.
- 감성 카페와 다양한 술집이 밀집해 있습니다.
- 쇼핑, 클럽, 맛집 탐방을 동시에 즐길 수 있습니다.
"""
    },
    {
        "name": "롯데월드타워",
        "lat": 37.513068,
        "lon": 127.102486,
        "description": "서울 랜드마크 초고층 빌딩",
        "subway": "잠실역 (2호선)",
        "detail": """
- 서울스카이 전망대에서 서울 전체를 조망할 수 있습니다.
- 롯데월드몰과 아쿠아리움이 연결되어 있습니다.
- 야경과 쇼핑을 동시에 즐기기 좋은 장소입니다.
"""
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566526,
        "lon": 127.009223,
        "description": "현대적 건축 명소",
        "subway": "동대문역사문화공원역 (2호선)",
        "detail": """
- 미래적인 건축 디자인으로 유명한 랜드마크입니다.
- 야간 LED 장미정원이 인기 포토존입니다.
- 근처 동대문 쇼핑타운과 함께 둘러보기 좋습니다.
"""
    },
    {
        "name": "인사동",
        "lat": 37.574019,
        "lon": 126.986647,
        "description": "전통 문화와 기념품 거리",
        "subway": "안국역 (3호선)",
        "detail": """
- 전통 찻집과 한식 맛집이 많습니다.
- 한국 기념품 쇼핑에 적합한 거리입니다.
- 거리 공연과 전통 공예품 구경이 가능합니다.
"""
    },
    {
        "name": "한강공원",
        "lat": 37.528316,
        "lon": 126.932598,
        "description": "서울 시민들의 대표 휴식 공간",
        "subway": "여의나루역 (5호선)",
        "detail": """
- 한강 자전거 라이딩과 피크닉이 유명합니다.
- 치킨과 라면을 먹으며 한강 야경을 즐길 수 있습니다.
- 밤에는 달빛무지개분수와 야경이 아름답습니다.
"""
    },
    {
        "name": "코엑스 별마당도서관",
        "lat": 37.510215,
        "lon": 127.059207,
        "description": "SNS 인기 실내 관광 명소",
        "subway": "삼성역 (2호선)",
        "detail": """
- 초대형 서가 포토존으로 유명합니다.
- 코엑스몰 쇼핑과 맛집 탐방을 함께 즐길 수 있습니다.
- 실내 관광지라 날씨 영향 없이 방문 가능합니다.
"""
    }
]

# ---------------------------------------------------
# Folium 지도 생성
# ---------------------------------------------------
seoul_center = [37.5665, 126.9780]

m = folium.Map(
    location=seoul_center,
    zoom_start=11,
    tiles="OpenStreetMap"
)

marker_cluster = MarkerCluster().add_to(m)

# ---------------------------------------------------
# 핑크 마커 추가
# ---------------------------------------------------
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
            color="pink",
            icon="heart"
        )
    ).add_to(marker_cluster)

# ---------------------------------------------------
# 지도 크기 80%
# ---------------------------------------------------
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st_folium(
        m,
        width=900,
        height=600
    )

# ---------------------------------------------------
# 관광지 선택
# ---------------------------------------------------
st.subheader("📍 관광지 상세 정보")

spot_names = [spot["name"] for spot in tourist_spots]

selected_spot = st.selectbox(
    "관광지를 선택하세요",
    spot_names
)

# 선택된 관광지 정보 표시
selected_data = next(
    spot for spot in tourist_spots
    if spot["name"] == selected_spot
)

st.markdown(f"## {selected_data['name']}")
st.markdown(f"🚇 가까운 지하철역: **{selected_data['subway']}**")
st.markdown(selected_data["detail"])

# ---------------------------------------------------
# 하단 리스트
# ---------------------------------------------------
st.subheader("🗺️ 서울 관광지 TOP10")

for idx, spot in enumerate(tourist_spots, start=1):
    st.markdown(
        f"""
        **{idx}. {spot['name']}**  
        - {spot['description']}
        """
    )

st.success("Streamlit Cloud에서 바로 실행 가능합니다.")
