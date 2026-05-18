import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 추천 🌈",
    page_icon="✨",
    layout="centered"
)

st.title("🌟 MBTI 진로 추천 서비스")
st.write("너의 MBTI에 딱 맞는 진로를 찾아보자! 😎")

# MBTI 데이터
mbti_data = {
    "INTJ": [
        {
            "job": "🧠 데이터 사이언티스트",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "논리적이고 분석적인 사람",
            "salary": "평균 연봉 약 6,500만원 💰"
        },
        {
            "job": "📊 전략 컨설턴트",
            "major": "경영학과, 경제학과",
            "personality": "계획 세우기 좋아하는 사람",
            "salary": "평균 연봉 약 7,000만원 💸"
        }
    ],

    "INTP": [
        {
            "job": "💻 프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "호기심 많고 창의적인 사람",
            "salary": "평균 연봉 약 5,500만원 💰"
        },
        {
            "job": "🔬 연구원",
            "major": "물리학과, 화학과",
            "personality": "탐구심 강한 사람",
            "salary": "평균 연봉 약 5,800만원 💸"
        }
    ],

    "ENTJ": [
        {
            "job": "🏢 CEO",
            "major": "경영학과",
            "personality": "리더십 강하고 추진력 있는 사람",
            "salary": "평균 연봉 약 8,000만원 💰"
        },
        {
            "job": "📈 마케팅 디렉터",
            "major": "광고홍보학과",
            "personality": "도전 좋아하는 사람",
            "salary": "평균 연봉 약 6,000만원 💸"
        }
    ],

    "ENTP": [
        {
            "job": "🚀 스타트업 창업가",
            "major": "경영학과",
            "personality": "아이디어 넘치는 사람",
            "salary": "평균 연봉 다양함 😎"
        },
        {
            "job": "🎤 방송 기획자",
            "major": "미디어학과",
            "personality": "재치 있고 말 잘하는 사람",
            "salary": "평균 연봉 약 5,000만원 💰"
        }
    ],

    "INFJ": [
        {
            "job": "💖 상담심리사",
            "major": "심리학과",
            "personality": "공감 능력 뛰어난 사람",
            "salary": "평균 연봉 약 4,500만원 💰"
        },
        {
            "job": "📚 작가",
            "major": "국문학과",
            "personality": "상상력 풍부한 사람",
            "salary": "평균 연봉 개인차 있음 ✍️"
        }
    ],

    "INFP": [
        {
            "job": "🎨 일러스트레이터",
            "major": "디자인학과",
            "personality": "감수성 풍부한 사람",
            "salary": "평균 연봉 약 4,000만원 💰"
        },
        {
            "job": "🎬 영화감독",
            "major": "영상학과",
            "personality": "창의적인 사람",
            "salary": "평균 연봉 다양함 🎥"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과",
            "personality": "사람 도와주는 걸 좋아하는 사람",
            "salary": "평균 연봉 약 5,200만원 💰"
        },
        {
            "job": "🤝 HR 매니저",
            "major": "경영학과",
            "personality": "사교적이고 배려심 있는 사람",
            "salary": "평균 연봉 약 6,000만원 💸"
        }
    ],

    "ENFP": [
        {
            "job": "📱 콘텐츠 크리에이터",
            "major": "미디어학과",
            "personality": "에너지 넘치는 사람",
            "salary": "평균 연봉 다양함 😆"
        },
        {
            "job": "🎉 이벤트 플래너",
            "major": "관광경영학과",
            "personality": "활발하고 창의적인 사람",
            "salary": "평균 연봉 약 4,500만원 💰"
        }
    ],

    "ISTJ": [
        {
            "job": "🏦 회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 책임감 강한 사람",
            "salary": "평균 연봉 약 7,000만원 💰"
        },
        {
            "job": "⚖️ 공무원",
            "major": "행정학과",
            "personality": "성실한 사람",
            "salary": "평균 연봉 약 5,000만원 💸"
        }
    ],

    "ISFJ": [
        {
            "job": "🏥 간호사",
            "major": "간호학과",
            "personality": "배려심 깊은 사람",
            "salary": "평균 연봉 약 5,000만원 💰"
        },
        {
            "job": "👶 유치원 교사",
            "major": "유아교육과",
            "personality": "따뜻하고 친절한 사람",
            "salary": "평균 연봉 약 3,500만원 💸"
        }
    ],

    "ESTJ": [
        {
            "job": "📋 프로젝트 매니저",
            "major": "경영학과",
            "personality": "체계적인 사람",
            "salary": "평균 연봉 약 6,500만원 💰"
        },
        {
            "job": "🏛️ 경찰 간부",
            "major": "경찰행정학과",
            "personality": "리더십 강한 사람",
            "salary": "평균 연봉 약 5,500만원 💸"
        }
    ],

    "ESFJ": [
        {
            "job": "🩺 의료 코디네이터",
            "major": "보건행정학과",
            "personality": "친절하고 사교적인 사람",
            "salary": "평균 연봉 약 4,500만원 💰"
        },
        {
            "job": "🏨 호텔 매니저",
            "major": "호텔관광학과",
            "personality": "서비스 정신 뛰어난 사람",
            "salary": "평균 연봉 약 5,000만원 💸"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 기계 엔지니어",
            "major": "기계공학과",
            "personality": "문제 해결 좋아하는 사람",
            "salary": "평균 연봉 약 6,000만원 💰"
        },
        {
            "job": "✈️ 파일럿",
            "major": "항공운항학과",
            "personality": "침착한 사람",
            "salary": "평균 연봉 약 8,000만원 💸"
        }
    ],

    "ISFP": [
        {
            "job": "🎵 음악 프로듀서",
            "major": "실용음악과",
            "personality": "감각적인 사람",
            "salary": "평균 연봉 다양함 🎶"
        },
        {
            "job": "🖌️ 그래픽 디자이너",
            "major": "시각디자인학과",
            "personality": "예술 감각 뛰어난 사람",
            "salary": "평균 연봉 약 4,500만원 💰"
        }
    ],

    "ESTP": [
        {
            "job": "💼 영업 전문가",
            "major": "경영학과",
            "personality": "활동적이고 자신감 있는 사람",
            "salary": "평균 연봉 약 5,500만원 💰"
        },
        {
            "job": "🏎️ 스포츠 마케터",
            "major": "스포츠산업학과",
            "personality": "도전 좋아하는 사람",
            "salary": "평균 연봉 약 5,000만원 💸"
        }
    ],

    "ESFP": [
        {
            "job": "🎤 연예인",
            "major": "연극영화과",
            "personality": "사람들 앞에 서는 걸 좋아하는 사람",
            "salary": "평균 연봉 다양함 🌟"
        },
        {
            "job": "📺 쇼호스트",
            "major": "방송연예과",
            "personality": "밝고 에너지 넘치는 사람",
            "salary": "평균 연봉 약 5,000만원 💰"
        }
    ]
}

# 선택 박스
selected_mbti = st.selectbox(
    "👉 너의 MBTI를 골라봐!",
    list(mbti_data.keys())
)

st.divider()

# 결과 출력
st.subheader(f"✨ {selected_mbti}에게 추천하는 진로!")

for career in mbti_data[selected_mbti]:
    st.markdown(f"""
    ## {career['job']}
    
    🎓 **추천 학과**  
    {career['major']}
    
    💡 **잘 맞는 성격**  
    {career['personality']}
    
    💰 **평균 연봉**  
    {career['salary']}
    
    ---
    """)

st.success("🌈 미래의 멋진 너를 응원할게!")
