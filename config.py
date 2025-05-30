"""
코드 리뷰 서비스를 위한 설정 파일
"""
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    """앱 설정 클래스"""
    
    # OpenAI API 설정
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # Streamlit 앱 설정
    APP_TITLE = "🤖 AI 코드 리뷰 챗봇"
    APP_DESCRIPTION = "AI가 제공하는 전문적인 코드 리뷰 서비스"
    
    # 코드 리뷰 카테고리
    REVIEW_CATEGORIES = [
        "🚨 오류 및 버그",
        "📝 스타일 및 컨벤션", 
        "⚡ 성능 최적화",
        "🔧 리팩토링 제안",
        "🧪 테스트 케이스",
        "📊 복잡도 분석"
    ]
    
    # 지원 언어
    SUPPORTED_LANGUAGES = [
        "Python", "JavaScript", "Java", "C++", "C#", 
        "Go", "Rust", "TypeScript", "PHP", "Ruby", "기타"
    ]
