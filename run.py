#!/usr/bin/env python3
"""
코드 리뷰 챗봇 실행 스크립트
"""
import sys
import subprocess
import os

def check_requirements():
    """필요한 패키지 설치 확인"""
    try:
        import streamlit
        import openai
        import pandas
        from dotenv import load_dotenv
        print("✅ 모든 필요한 패키지가 설치되어 있습니다.")
        return True
    except ImportError as e:
        print(f"❌ 패키지 누락: {e}")
        print("UV 환경에서 패키지를 설치해주세요:")
        print("uv add streamlit openai python-dotenv pandas")
        print("또는 requirements.txt 사용:")
        print("uv pip install -r requirements.txt")
        return False

def check_env_file():
    """환경 변수 파일 확인"""
    if not os.path.exists('.env'):
        print("⚠️  .env 파일이 없습니다.")
        print("다음 단계를 따라주세요:")
        print("1. .env.example을 복사하여 .env 파일 생성")
        print("2. .env 파일에 OpenAI API 키 설정")
        print("   OPENAI_API_KEY=your_api_key_here")
        return False
    
    print("✅ .env 파일이 존재합니다.")
    return True

def run_app():
    """Streamlit 앱 실행"""
    print("🚀 코드 리뷰 챗봇을 시작합니다...")
    print("브라우저가 자동으로 열립니다.")
    print("종료하려면 Ctrl+C를 누르세요.")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 코드 리뷰 챗봇을 종료합니다.")
    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")

def main():
    """메인 함수"""
    print("=" * 50)
    print("🤖 AI 코드 리뷰 챗봇")
    print("=" * 50)
    
    # 요구사항 확인
    if not check_requirements():
        sys.exit(1)
    
    # 환경 변수 파일 확인
    if not check_env_file():
        print("\n계속 진행하시겠습니까? (API 키는 앱에서 입력 가능)")
        response = input("y/N: ").lower()
        if response != 'y':
            sys.exit(1)
    
    # 앱 실행
    run_app()

if __name__ == "__main__":
    main()
