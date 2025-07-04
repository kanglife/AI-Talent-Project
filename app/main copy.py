import streamlit as st
from agents import run_investment_analysis
from prompts import build_prompt
from utils.parser import parse_investment_text
from utils.charts import plot_investment_allocation
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="AI 금융 분석가", layout="wide")

# 환경 변수 유효성 확인
if not os.getenv("AOAI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    st.error("❌ API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY 또는 AOAI_API_KEY를 추가하세요.")
    st.stop()

st.markdown("## ✅ <span style='color:#00d26a'>AI 금융 투자 분석가</span>", unsafe_allow_html=True)
st.markdown("---")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["🧾 투자 정보 입력", "📊 분석 결과", "📈 투자 비중 차트"])

with tab1:
    st.subheader("📥 보유 자산 입력")
    investment_data = st.text_area(
        "예: 삼성전자 30%, 비트코인 20%, 달러 예금 50%",
        height=150
    )

    st.subheader("📊 투자 성향 선택")
    investor_profile = st.radio("선택:", ["보수적", "중립적", "공격적"], horizontal=True)

    if st.button("🔍 분석 시작"):
        st.session_state.result = run_investment_analysis(investment_data, investor_profile)
        st.session_state.data_dict = parse_investment_text(investment_data)
        st.session_state.analyzed = True
    else:
        st.session_state.analyzed = False

with tab2:
    st.subheader("🔎 AI 분석 결과")
    if st.session_state.get("analyzed", False):
        st.markdown(
            f"""<div style='background:#1e1e1e; padding:20px; border-radius:10px; color:#fff'>
            {st.session_state.result}
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.info("먼저 [투자 정보 입력] 탭에서 분석을 실행하세요.")

with tab3:
    st.subheader("📈 투자 비중 차트")
    if st.session_state.get("analyzed", False) and st.session_state.get("data_dict"):
        fig = plot_investment_allocation(st.session_state.data_dict)
        st.pyplot(fig)
    else:
        st.warning("분석을 먼저 진행해야 차트를 표시할 수 있습니다.")
