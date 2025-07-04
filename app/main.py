import streamlit as st
from agent_flow import create_agent_flow  # 에이전트 플로우 함수
from rag import load_finance_docs, create_vector_db, load_vector_db, rag_search

st.set_page_config(page_title="AI 금융 투자 분석가", layout="wide")

st.title("💡 AI 금융 투자 추천 시스템")

tab1, tab2 = st.tabs(["📈 AI Agent 투자 분석 ", "📚 문서 기반 질의응답"])


# --- [1] 분석 결과 탭 --- #
with tab1:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("📥 보유 자산 입력")
        investment_data = st.text_area("예: 삼성전자 30%, 비트코인 20%, 달러 예금 50%", height=150)

        st.subheader("📊 투자 성향 선택")
        investor_profile = st.radio("선택:", ["보수적", "중립적", "공격적"], horizontal=True)

        if st.button("🔍 분석 시작") and investment_data:
            with st.spinner("🔎 AI 분석 중... 잠시만 기다려주세요."):
                graph = create_agent_flow()
                result_state = graph.invoke({
                    "investment_data": investment_data,
                    "investor_profile": investor_profile
                })

            # 분석 결과 세션에 저장
            st.session_state["result"] = result_state["final_strategy"]
            st.session_state["wiki_summary"] = result_state.get("wiki_summary", "")
            st.session_state["summary"] = result_state.get("summary", "")
            st.session_state["analyzed"] = True

    with col2:
        st.subheader("📝 분석 결과")
        if st.session_state.get("analyzed"):
            st.markdown("### ✅ 최종 전략 제안")
            st.markdown(st.session_state["result"])
            st.markdown("### 📖 Wikipedia 기반 정보 요약")
            st.markdown(st.session_state.get("wiki_summary", "요약 정보 없음"))
        else:
            st.info("좌측에서 분석을 먼저 진행하세요.")

# --- [1] RAG 탭--- #
with tab2:
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📑 투자 보고서 인덱싱 (최초 1회만)", key="indexing_btn"):
            with st.spinner("보고서 분석 및 인덱싱 중..."):
                docs = load_finance_docs()
                create_vector_db(docs)
            st.success("투자 보고서 인덱싱 완료!")

        category = st.selectbox("📁 문서 유형 선택", ["전체", "reports", "news", "theory", "products"])
        query = st.text_input("질문을 입력하세요")

        if st.button("검색"):
            st.session_state["rag_searched"] = True
            st.session_state["rag_query_text"] = query
            st.session_state["rag_category"] = category

    with col2:
        if st.session_state.get("rag_searched"):
            db = load_vector_db()
            answer = rag_search(
                st.session_state.get("rag_query_text", ""),
                db,
                category_filter=st.session_state.get("rag_category", "전체")
            )
            st.markdown("#### 📄 AI RAG 답변")
            st.markdown(answer if answer else "해당 내용과 유사한 답변이 없습니다.")
            st.session_state["rag_searched"] = False
