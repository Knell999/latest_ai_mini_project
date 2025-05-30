# 🤖 AI 코드 리뷰 챗봇

AI 기반의 지능형 코드 리뷰 서비스입니다. OpenAI GPT를 활용하여 코드의 오류, 스타일, 성능, 리팩토링 제안 등 종합적인 코드 리뷰를 제공합니다.

## ✨ 주요 기능

- 🔍 **종합적인 코드 분석**: 오류, 스타일, 성능, 리팩토링 제안
- 🧪 **자동 테스트 케이스 생성**: 단위 테스트 코드 자동 생성
- ⚡ **빠른 수정 제안**: 특정 이슈에 대한 즉시 수정 방안 제공
- 📊 **복잡도 분석**: 시간/공간 복잡도 자동 분석
- 💬 **사용자 피드백 시스템**: 서비스 품질 지속 개선
- 📈 **분석 대시보드**: 사용 통계 및 인사이트 제공
- 🌐 **다중 언어 지원**: Python, JavaScript, Java, C++ 등

## 🏗️ 프로젝트 구조

```
code_chatbot/
├── app.py                 # Streamlit 메인 애플리케이션
├── config.py              # 설정 파일
├── code_reviewer.py       # AI 코드 리뷰 모듈
├── feedback_collector.py  # 피드백 수집 모듈
├── pipeline.py            # 코드 리뷰 파이프라인
├── run.py                 # 실행 스크립트
├── requirements.txt       # 필요한 패키지 목록
├── .env.example          # 환경변수 예시 파일
└── README.md             # 프로젝트 문서
```

## 🚀 설치 및 실행

### UV 환경 (권장)
```bash
# UV 설치 (필요시)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치 및 실행
./run_uv.sh

# 또는 수동 실행
uv sync
uv run streamlit run app.py --server.port 8501
```

### 기존 pip 환경
```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python run.py

# 또는 직접 실행
streamlit run app.py
```

### 환경 변수 설정
```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일에 OpenAI API 키 설정
# OPENAI_API_KEY=your_openai_api_key_here
```

## 💻 사용 방법

### 1. 코드 리뷰
1. 프로그래밍 언어 선택
2. 리뷰 타입 선택 (종합 리뷰 / 테스트 케이스 생성)
3. 코드 입력 후 "코드 리뷰 시작" 클릭
4. AI가 생성한 종합적인 리뷰 결과 확인

### 2. 빠른 수정
1. 코드 리뷰 후 "빠른 수정" 섹션 이용
2. 수정하고 싶은 이슈 설명 입력
3. 구체적인 수정 제안 확인

### 3. 피드백 제출
1. 리뷰 완료 후 "피드백" 페이지 이동
2. 평점 및 유용성 평가
3. 개선 제안사항 입력 (선택사항)

## 📊 모듈 설명

### `CodeReviewHelper`
- OpenAI API를 활용한 코드 분석
- 카테고리별 상세 리뷰 제공
- 테스트 케이스 자동 생성
- 빠른 수정 제안 기능

### `FeedbackCollector`
- 사용자 피드백 수집 및 저장
- 서비스 품질 통계 분석
- 개선 인사이트 제공

### `CodeReviewPipeline`
- 전체 리뷰 프로세스 통합 관리
- 세션 관리 및 히스토리 추적
- 입력 유효성 검증
- 에러 처리 및 복구

## 🎯 리뷰 카테고리

1. **🚨 오류 및 버그**: 논리적 오류, 런타임 에러 가능성
2. **📝 스타일 및 컨벤션**: 코딩 스타일, 네이밍 컨벤션
3. **⚡ 성능 최적화**: 알고리즘 효율성, 메모리 최적화
4. **🔧 리팩토링 제안**: 코드 구조 개선, 중복 제거
5. **🧪 테스트 케이스**: 단위 테스트, 엣지 케이스
6. **📊 복잡도 분석**: 시간/공간 복잡도 평가

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-3.5-turbo
- **Data Processing**: Pandas
- **Configuration**: python-dotenv
- **Language**: Python 3.8+

## 📈 주요 특징

### 모듈화된 아키텍처
- 각 기능별로 독립적인 모듈 설계
- 유지보수성과 확장성 고려
- 명확한 책임 분리

### 파이프라인 설계
- 전체 프로세스의 통합 관리
- 에러 처리 및 복구 메커니즘
- 세션 기반 상태 관리

### 사용자 경험 최적화
- 직관적인 웹 인터페이스
- 실시간 피드백 및 프로그레스 표시
- 반응형 디자인

### 데이터 기반 개선
- 사용자 피드백 자동 수집
- 서비스 품질 메트릭 추적
- 지속적인 서비스 개선

## 🔧 개발자 가이드

### 새로운 리뷰 카테고리 추가
```python
# config.py에서 REVIEW_CATEGORIES 수정
REVIEW_CATEGORIES.append("🆕 새로운 카테고리")

# code_reviewer.py에서 프롬프트 수정
system_prompt += "**🆕 새로운 카테고리**\n- 새로운 분석 기준\n"
```

### 새로운 프로그래밍 언어 지원
```python
# config.py에서 SUPPORTED_LANGUAGES 수정
SUPPORTED_LANGUAGES.append("새로운언어")
```

### 커스텀 메트릭 추가
```python
# feedback_collector.py의 get_feedback_statistics 수정
def get_feedback_statistics(self):
    # 기존 메트릭 + 새로운 메트릭
    return stats
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🙋‍♂️ 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 등록해주세요.

---

**⚠️ 주의사항**: OpenAI API 키가 필요하며, API 사용에 따른 비용이 발생할 수 있습니다.
