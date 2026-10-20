import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(page_title="설득의 신 - AI 토론 시뮬레이터", page_icon="🎯", layout="centered")

st.title("🎯 AI를 설득해봐! - 설득 왕을 찾아라")
st.markdown("초등학교 5학년 친구들, 여러분의 논리적인 글로 AI 상대를 설득해 보세요!")

# 사이드바에서 API 키 입력받기
with st.sidebar:
    st.subheader("🔑 API 설정")
    api_key = st.text_input("구글 Gemini API 키를 입력하세요:", type="password")
    st.markdown("[Google AI Studio에서 API 키 발급받기](https://aistudio.google.com/)")
    st.markdown("---")
    st.info("💡 **사용 팁:**\n- 먼저 API 키를 입력한 뒤 주제를 고르세요.\n- 5학년 눈높이에 맞는 타당한 근거를 적을수록 AI가 쉽게 설득됩니다!")

# 1. 10가지 주제 리스트
topics = [
    "1. 학교에서 스마트폰 사용을 전면 허용해야 한다",
    "2. 숙제는 완전히 없애거나 아주 줄여야 한다",
    "3. 등교 시간을 지금보다 30분 더 늦춰야 한다",
    "4. 급식 메뉴를 학생들이 직접 일주일에 한 번씩 정해야 한다",
    "5. 쉬는 시간을 지금보다 10분 더 늘려야 한다",
    "6. 초등학생도 교복을 입어야 한다",
    "7. 일기 검사는 학생의 사생활을 위해 없애야 한다",
    "8. 교실에서 반려동물(햄스터, 물고기 등)을 키워야 한다",
    "9. 현장체험학습 장소를 학생들이 직접 투표로 결정해야 한다",
    "10. 체육 시간을 일주일에 3번 이상으로 늘려야 한다"
]

# 사용자 입력 인터페이스
selected_topic = st.selectbox("📌 토론하고 싶은 주제를 선택하세요:", topics)
stance = st.radio("나의 입장은요?", ["찬성", "반대"])

student_argument = st.text_area(
    "💬 AI를 설득할 나만의 주장과 근거를 적어보세요!",
    placeholder="예시: 저는 스마트폰을 쓰게 해줘야 한다고 생각합니다. 왜냐하면 하굣길 안전을 위해 부모님과 연락이 꼭 필요하기 때문입니다."
)

# AI에게 설득 시도 버튼
if st.button("🚀 AI에게 설득 시도하기"):
    if not api_key:
        st.error("⚠️ 사이드바에 구글 Gemini API 키를 먼저 입력해 주세요!")
    elif not student_argument.strip():
        st.warning("⚠️ 먼저 설득하는 글을 작성해 주세요!")
    else:
        with st.spinner("AI 심사위원이 꼼꼼히 읽고 판정하는 중입니다... 🤔"):
            try:
                # 구글 GenAI 클라이언트 초기화
                client = genai.Client(api_key=api_key)
                
                # 초등학교 5학년 눈높이에 맞춘 심판 페르소나 프롬프트
                prompt = f"""
                너는 초등학교 5학년 학생과 대화하는 토론 상대방이자 따뜻한 심사위원이야.
                주제: {selected_topic}
                학생의 입장: {stance}
                학생의 설득 글: "{student_argument}"

                [규칙]
                1. 초등학교 5학년 학생의 눈높이에 맞춰 친근하고 다정한 말투(~해요, ~랍니다)로 대답해 줘.
                2. 학생의 글에서 근거가 얼마나 논리적이고 짜임새 있는지 평가해 줘.
                3. 학생의 글이 충분히 타당하고 설득력이 있다면 대답 맨 처음에 "🎉 설득 성공!"을 외치며 수긍해 줘.
                4. 만약 논리가 부족하거나 억지이거나 근거가 부실하다면 대답 맨 처음에 "🤔 아직은 부족해요! 설득 실패"라고 판정해 줘.
                5. 판정 이유와 함께, 더 멋진 글로 고치려면 어떤 점을 보완해야 할지 다정하게 피드백을 남겨줘.
                """

                # Gemini 모델 호출 (gemini-2.0-flash 모델 사용)
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                )
                
                # 결과 출력
                st.markdown("---")
                st.subheader("📢 AI 심사위원의 판정 결과")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다. API 키를 다시 확인해 주세요.\n상세 내용: {e}")
