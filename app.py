"""
AI 코드 리뷰 챗봇 - Streamlit 메인 애플리케이션
"""
import streamlit as st
import os
from datetime import datetime
import time

from config import Config
from pipeline import CodeReviewPipeline

# 페이지 설정
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사용자 정의 CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .review-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .code-container {
        background-color: #2d3748;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stats-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """세션 상태 초기화"""
    if 'pipeline' not in st.session_state:
        try:
            st.session_state.pipeline = CodeReviewPipeline()
            st.session_state.session_started = True
        except ValueError as e:
            st.session_state.pipeline = None
            st.session_state.session_started = False
            st.error(f"초기화 오류: {e}")
    
    if 'review_history' not in st.session_state:
        st.session_state.review_history = []
    
    if 'current_review' not in st.session_state:
        st.session_state.current_review = None


def main():
    """메인 애플리케이션"""
    
    # 헤더
    st.markdown(f"""
    <div class="main-header">
        <h1>{Config.APP_TITLE}</h1>
        <p>{Config.APP_DESCRIPTION}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 사이드바
    setup_sidebar()
    
    # API 키 확인
    if not check_api_key():
        return
    
    # 메인 컨텐츠
    if st.session_state.get('current_page', 'review') == 'review':
        show_code_review_page()
    elif st.session_state.current_page == 'history':
        show_history_page()
    elif st.session_state.current_page == 'analytics':
        show_analytics_page()
    elif st.session_state.current_page == 'feedback':
        show_feedback_page()


def setup_sidebar():
    """사이드바 설정"""
    with st.sidebar:
        st.header("🛠️ 메뉴")
        
        # 네비게이션
        page = st.selectbox(
            "페이지 선택",
            options=['review', 'history', 'analytics', 'feedback'],
            format_func=lambda x: {
                'review': '🔍 코드 리뷰',
                'history': '📜 리뷰 히스토리', 
                'analytics': '📊 분석 대시보드',
                'feedback': '💬 피드백'
            }[x],
            key='current_page'
        )
        
        st.divider()
        
        # 세션 정보
        if st.session_state.get('session_started'):
            st.success("✅ 세션 활성화")
            if st.button("🔄 새 세션 시작"):
                st.session_state.pipeline.start_new_session()
                st.session_state.review_history = []
                st.rerun()
        else:
            st.error("❌ 세션 비활성화")
        
        st.divider()
        
        # 통계 정보
        if st.session_state.get('pipeline'):
            stats = st.session_state.pipeline.get_feedback_statistics()
            
            st.subheader("📈 서비스 통계")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("총 리뷰", stats.get('total_reviews', 0))
                st.metric("평균 평점", f"{stats.get('average_rating', 0):.1f}")
            
            with col2:
                st.metric("도움됨 비율", f"{stats.get('helpful_percentage', 0):.1f}%")
                
            # 언어 분포
            if stats.get('language_distribution'):
                st.subheader("🔥 인기 언어")
                for lang, count in list(stats['language_distribution'].items())[:3]:
                    st.write(f"• {lang}: {count}회")


def check_api_key():
    """API 키 확인 및 설정"""
    if not Config.OPENAI_API_KEY:
        st.error("⚠️ OpenAI API 키가 설정되지 않았습니다.")
        st.info("""
        API 키를 설정하는 방법:
        1. `.env` 파일을 생성하고 `OPENAI_API_KEY=your_key_here` 추가
        2. 또는 환경변수로 설정
        """)
        
        # 임시 API 키 입력
        api_key = st.text_input("임시 API 키 입력", type="password")
        if api_key:
            try:
                st.session_state.pipeline = CodeReviewPipeline(api_key)
                st.session_state.session_started = True
                st.success("✅ API 키가 설정되었습니다!")
                st.rerun()
            except Exception as e:
                st.error(f"API 키 설정 실패: {e}")
        return False
    
    return True


def show_code_review_page():
    """코드 리뷰 페이지"""
    st.header("🔍 코드 리뷰")
    
    # 입력 섹션
    col1, col2 = st.columns([3, 1])
    
    with col1:
        language = st.selectbox(
            "프로그래밍 언어 선택",
            Config.SUPPORTED_LANGUAGES,
            index=0
        )
    
    with col2:
        review_type = st.selectbox(
            "리뷰 타입",
            ["종합 리뷰", "테스트 케이스 생성"],
            index=0
        )
    
    # 코드 입력
    code_input = st.text_area(
        "코드를 입력하세요",
        height=300,
        placeholder="여기에 리뷰받고 싶은 코드를 붙여넣으세요..."
    )
    
    # 리뷰 실행 버튼
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🚀 코드 리뷰 시작", type="primary", use_container_width=True):
            if code_input.strip():
                process_code_review(code_input, language, review_type)
            else:
                st.error("코드를 입력해주세요!")
    
    # 빠른 수정 섹션
    if st.session_state.current_review:
        st.divider()
        show_quick_fix_section(code_input, language)
    
    # 리뷰 결과 표시
    if st.session_state.current_review:
        show_review_result(st.session_state.current_review)


def process_code_review(code_input, language, review_type):
    """코드 리뷰 처리"""
    review_type_map = {
        "종합 리뷰": "comprehensive",
        "테스트 케이스 생성": "test_cases"
    }
    
    with st.spinner("🤖 AI가 코드를 분석중입니다..."):
        # 프로그레스 바
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        result = st.session_state.pipeline.process_code_review(
            code_snippet=code_input,
            language=language,
            review_type=review_type_map[review_type]
        )
        
        progress_bar.empty()
        
        if result['success']:
            st.session_state.current_review = result
            st.session_state.review_history.append(result)
            st.success("✅ 코드 리뷰가 완료되었습니다!")
        else:
            st.error(f"❌ 리뷰 실패: {result.get('error', '알 수 없는 오류')}")


def show_review_result(review_data):
    """리뷰 결과 표시"""
    st.divider()
    st.subheader("📋 리뷰 결과")
    
    # 코드 통계
    stats = review_data.get('code_stats', {})
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("전체 라인", stats.get('total_lines', 0))
    with col2:
        st.metric("코드 라인", stats.get('non_empty_lines', 0))
    with col3:
        st.metric("문자 수", stats.get('total_characters', 0))
    with col4:
        st.metric("복잡도", stats.get('estimated_complexity', 'N/A'))
    
    # 리뷰 내용
    st.markdown(f"""
    <div class="review-container">
        {review_data['review_result'].replace('\n', '<br>')}
    </div>
    """, unsafe_allow_html=True)
    
    # 원본 코드
    with st.expander("🔍 원본 코드 보기"):
        st.code(review_data['code_snippet'], language=review_data['language'].lower())


def show_quick_fix_section(code_input, language):
    """빠른 수정 섹션"""
    st.subheader("⚡ 빠른 수정")
    
    issue_description = st.text_input(
        "수정하고 싶은 이슈를 설명해주세요",
        placeholder="예: 초기값 설정 문제, 예외 처리 추가 등..."
    )
    
    if st.button("🔧 수정 제안 받기") and issue_description:
        with st.spinner("수정 제안을 생성중입니다..."):
            fix_result = st.session_state.pipeline.process_quick_fix(
                code_snippet=code_input,
                issue_description=issue_description,
                language=language
            )
            
            if fix_result['success']:
                st.success("✅ 수정 제안이 생성되었습니다!")
                st.markdown(f"""
                <div class="review-container">
                    {fix_result['fix_result'].replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ 수정 제안 실패: {fix_result.get('error')}")


def show_history_page():
    """히스토리 페이지"""
    st.header("📜 리뷰 히스토리")
    
    if not st.session_state.review_history:
        st.info("아직 리뷰 히스토리가 없습니다.")
        return
    
    # 히스토리 필터
    col1, col2 = st.columns(2)
    with col1:
        language_filter = st.selectbox(
            "언어 필터",
            ["전체"] + list(set([r['language'] for r in st.session_state.review_history]))
        )
    
    with col2:
        review_type_filter = st.selectbox(
            "리뷰 타입 필터", 
            ["전체"] + list(set([r['review_type'] for r in st.session_state.review_history]))
        )
    
    # 필터링된 히스토리 표시
    filtered_history = st.session_state.review_history
    
    if language_filter != "전체":
        filtered_history = [r for r in filtered_history if r['language'] == language_filter]
    
    if review_type_filter != "전체":
        filtered_history = [r for r in filtered_history if r['review_type'] == review_type_filter]
    
    # 히스토리 아이템 표시
    for i, review in enumerate(reversed(filtered_history)):
        with st.expander(f"리뷰 #{len(filtered_history)-i} - {review['language']} ({review['timestamp'][:16]})"):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.code(review['code_snippet'][:200] + "..." if len(review['code_snippet']) > 200 else review['code_snippet'])
            
            with col2:
                st.write(f"**언어**: {review['language']}")
                st.write(f"**타입**: {review['review_type']}")
                st.write(f"**시간**: {review['timestamp'][11:16]}")
            
            st.markdown("**리뷰 결과:**")
            st.write(review['review_result'][:500] + "..." if len(review['review_result']) > 500 else review['review_result'])


def show_analytics_page():
    """분석 대시보드 페이지"""
    st.header("📊 분석 대시보드")
    
    if not st.session_state.pipeline:
        st.error("파이프라인이 초기화되지 않았습니다.")
        return
    
    # 통계 정보
    stats = st.session_state.pipeline.get_feedback_statistics()
    insights = st.session_state.pipeline.get_improvement_insights()
    
    # KPI 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 리뷰 수",
            value=stats.get('total_reviews', 0),
            delta=f"+{len(st.session_state.review_history)} (현재 세션)"
        )
    
    with col2:
        st.metric(
            label="평균 평점",
            value=f"{stats.get('average_rating', 0):.1f}/5.0",
            delta="⭐" * int(stats.get('average_rating', 0))
        )
    
    with col3:
        st.metric(
            label="도움됨 비율",
            value=f"{stats.get('helpful_percentage', 0):.1f}%"
        )
    
    with col4:
        st.metric(
            label="현재 세션 리뷰",
            value=len(st.session_state.review_history)
        )
    
    # 인사이트
    st.subheader("💡 개선 인사이트")
    for insight in insights:
        st.info(insight)
    
    # 언어별 분포
    if stats.get('language_distribution'):
        st.subheader("📈 언어별 사용 분포")
        
        import pandas as pd
        df = pd.DataFrame(
            list(stats['language_distribution'].items()),
            columns=['언어', '사용 횟수']
        )
        st.bar_chart(df.set_index('언어'))
    
    # 최근 제안사항
    if stats.get('recent_suggestions'):
        st.subheader("💬 최근 사용자 제안사항")
        for i, suggestion in enumerate(stats['recent_suggestions'], 1):
            st.write(f"{i}. {suggestion}")


def show_feedback_page():
    """피드백 페이지"""
    st.header("💬 피드백")
    
    if not st.session_state.current_review:
        st.info("먼저 코드 리뷰를 받아보세요!")
        return
    
    st.subheader("🌟 리뷰에 대한 평가를 해주세요")
    
    # 피드백 폼
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            rating = st.slider("평점 (1-5)", 1, 5, 3)
            helpful = st.radio("이 리뷰가 도움이 되었나요?", ["예", "아니오"]) == "예"
        
        with col2:
            suggestions = st.text_area(
                "개선 제안사항 (선택사항)",
                placeholder="더 나은 서비스를 위한 제안을 해주세요...",
                height=100
            )
        
        submitted = st.form_submit_button("📝 피드백 제출", type="primary")
        
        if submitted:
            result = st.session_state.pipeline.collect_user_feedback(
                review_result=st.session_state.current_review['review_result'],
                user_code=st.session_state.current_review['code_snippet'],
                language=st.session_state.current_review['language'],
                rating=rating,
                helpful=helpful,
                suggestions=suggestions
            )
            
            if result['success']:
                st.success("✅ 피드백이 성공적으로 제출되었습니다! 감사합니다.")
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"❌ 피드백 제출 실패: {result.get('error')}")


if __name__ == "__main__":
    main()
