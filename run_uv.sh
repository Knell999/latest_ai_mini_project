#!/bin/bash
# UV 환경에서 코드 리뷰 챗봇 실행 스크립트

echo "🤖 AI 코드 리뷰 챗봇 (UV 환경)"
echo "=================================="

# UV 설치 확인
if ! command -v uv &> /dev/null; then
    echo "❌ UV가 설치되지 않았습니다."
    echo "UV 설치: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ UV가 설치되어 있습니다."

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다."
    if [ -f ".env.example" ]; then
        echo "📋 .env.example을 복사하여 .env 파일을 생성합니다..."
        cp .env.example .env
        echo "✅ .env 파일이 생성되었습니다."
        echo "📝 필요시 .env 파일에서 API 키를 수정해주세요."
    else
        echo "📝 .env 파일을 생성하고 다음을 추가해주세요:"
        echo "OPENAI_API_KEY=your_openai_api_key_here"
    fi
fi

# 의존성 설치
echo "📦 의존성을 설치합니다..."
if [ -f "pyproject.toml" ]; then
    uv sync
else
    uv pip install streamlit openai python-dotenv pandas
fi

# 애플리케이션 실행
echo "🚀 코드 리뷰 챗봇을 시작합니다..."
echo "브라우저가 자동으로 열립니다."
echo "종료하려면 Ctrl+C를 누르세요."

uv run streamlit run app.py --server.port 8501
