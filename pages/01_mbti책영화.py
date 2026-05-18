import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI 책 & 영화 추천 🎬📚",
    page_icon="🌈",
    layout="centered"
)

# 제목
st.title("🌈 MBTI별 책 & 영화 추천")
st.write("너의 MBTI에 딱 맞는 책📚과 영화🎬를 추천해줄게 😆")

# 데이터
mbti_data = {
    "INTJ": {
        "books": [
            {
                "title": "📘 사피엔스",
                "reason": "깊게 생각하고 세상을 분석하는 INTJ에게 딱 어울리는 책이야 🧠"
            },
            {
                "title": "📗 데미안",
                "reason": "자기만의 길을 찾고 싶은 INTJ 감성에 잘 맞아 ✨"
            }
        ],
        "movies": [
            {
                "title": "🎬 인터스텔라",
                "reason": "과학과 철학적인 메시지를 좋아하는 INTJ에게 추천 🚀"
            },
            {
                "title": "🎬 인셉션",
                "reason": "복잡한 스토리와 추리하는 재미가 있어서 몰입감 최고 😎"
            }
        ]
    },

    "INFP": {
        "books": [
            {
                "title": "📘 어린 왕자",
                "reason": "감수성이 풍부한 INFP 마음을 따뜻하게 해줘 🌙"
            },
            {
                "title": "📗 미드나잇 라이브러리",
                "reason": "삶과 선택에 대해 생각하게 만드는 감성 책 📖"
            }
        ],
        "movies": [
            {
                "title": "🎬 코코",
                "reason": "가족과 꿈에 대한 따뜻한 메시지가 INFP와 잘 어울려 🎸"
            },
            {
                "title": "🎬 라라랜드",
                "reason": "감성적이고 예술적인 분위기를 좋아한다면 추천 💃"
            }
        ]
    },

    "ENFP": {
        "books": [
            {
                "title": "📘 아몬드",
                "reason": "사람의 감정과 관계를 중요하게 생각하는 ENFP에게 추천 💛"
            },
            {
                "title": "📗 트렌드 코리아",
                "reason": "새로운 아이디어 좋아하는 ENFP 스타일에 딱 😆"
            }
        ],
        "movies": [
            {
                "title": "🎬 스파이더맨: 뉴 유니버스",
                "reason": "자유롭고 개성 넘치는 분위기가 ENFP와 찰떡 🕷️"
            },
            {
                "title": "🎬 위대한 쇼맨",
                "reason": "열정과 꿈을 향해 달려가는 모습이 너무 잘 어울려 🎤"
            }
        ]
    },

    "ISTJ": {
        "books": [
            {
                "title": "📘 총, 균, 쇠",
                "reason": "체계적이고 논리적인 ISTJ가 흥미롭게 읽을 수 있어 📚"
            },
            {
                "title": "📗 공부의 본질",
                "reason": "성실하고 계획적인 성향과 잘 맞는 책 ✍️"
            }
        ],
        "movies": [
            {
                "title": "🎬 변호인",
                "reason": "책임감과 원칙을 중요하게 생각하는 ISTJ에게 추천 ⚖️"
            },
            {
                "title": "🎬 포레스트 검프",
                "reason": "꾸준함과 성실함의 힘을 보여주는 영화 🏃"
            }
        ]
    },

    "ENTP": {
        "books": [
            {
                "title": "📘 넛지",
                "reason": "아이디어와 심리전을 좋아하는 ENTP에게 딱 🧠"
            },
            {
                "title": "📗 역행자",
                "reason": "도전적이고 새로운 방식 좋아하는 성향과 잘 맞아 🚀"
            }
        ],
        "movies": [
            {
                "title": "🎬 아이언맨",
                "reason": "재치 있고 창의적인 주인공이 ENTP 느낌이야 😎"
            },
            {
                "title": "🎬 나우 유 씨 미",
                "reason": "반전과 두뇌 플레이 좋아하면 완전 추천 🎩"
            }
        ]
    }
}

# 나머지 MBTI 자동 생성
all_mbti = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISTP", "ESTJ", "ESTP",
    "ISFJ", "ISFP", "ESFJ", "ESFP"
]

# 없는 MBTI는 기본 추천 데이터 넣기
for mbti in all_mbti:
    if mbti not in mbti_data:
        mbti_data[mbti] = {
            "books": [
                {
                    "title": "📘 해리포터",
                    "reason": f"{mbti} 유형이 재미있게 몰입할 수 있는 판타지 세계관 ⚡"
                },
                {
                    "title": "📗 죽고 싶지만 떡볶이는 먹고 싶어",
                    "reason": "청소년들이 공감하기 좋은 감성 책 💭"
                }
            ],
            "movies": [
                {
                    "title": "🎬 어벤져스",
                    "reason": "팀워크와 개성 넘치는 캐릭터들이 매력적 🦸"
                },
                {
                    "title": "🎬 인사이드 아웃",
                    "reason": "감정에 대해 생각하게 만드는 따뜻한 영화 😊"
                }
            ]
        }

# MBTI 선택
selected_mbti = st.selectbox(
    "👉 너의 MBTI를 골라봐!",
    all_mbti
)

st.divider()

# 결과 출력
st.subheader(f"✨ {selected_mbti}에게 추천하는 책 & 영화!")

# 책 추천
st.markdown("## 📚 추천 책 2권")

for book in mbti_data[selected_mbti]["books"]:
    st.markdown(f"""
### {book['title']}
💡 추천 이유  
{book['reason']}
""")

st.divider()

# 영화 추천
st.markdown("## 🎬 추천 영화 2편")

for movie in mbti_data[selected_mbti]["movies"]:
    st.markdown(f"""
### {movie['title']}
🍿 추천 이유  
{movie['reason']}
""")

st.success("🌟 오늘 추천 어땠어? 재미있게 즐겨봐 😆")
