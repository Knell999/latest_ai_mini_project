"""
코드 리뷰 도우미 모듈
AI를 활용한 코드 분석 및 리뷰 기능 제공
"""
from openai import OpenAI
from typing import Dict, List, Optional
from config import Config


class CodeReviewHelper:
    """AI 기반 코드 리뷰 도우미 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        코드 리뷰 도우미 초기화
        
        Args:
            api_key: OpenAI API 키 (없으면 환경변수에서 가져옴)
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
        
        # OpenAI 클라이언트 초기화
        self.client = OpenAI(api_key=self.api_key)
        self.model = Config.OPENAI_MODEL
    
    def analyze_code(self, code_snippet: str, language: str = "Python") -> str:
        """
        코드 스니펫을 분석하고 종합적인 리뷰 제공
        
        Args:
            code_snippet: 분석할 코드
            language: 프로그래밍 언어
            
        Returns:
            분석 결과 문자열
        """
        try:
            messages = self._create_review_messages(code_snippet, language)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"코드 분석 중 오류가 발생했습니다: {str(e)}"
    
    def _create_review_messages(self, code_snippet: str, language: str) -> List[Dict]:
        """리뷰 요청을 위한 메시지 생성"""
        
        system_prompt = f"""
        당신은 {language} 전문가이자 시니어 개발자입니다.
        주어진 코드에 대해 다음 카테고리별로 상세하고 건설적인 피드백을 제공해주세요:

        **🚨 오류 및 버그**
        - 논리적 오류, 런타임 에러 가능성
        - 예외 처리 누락
        - 경계 조건 처리 문제

        **📝 스타일 및 컨벤션**
        - 코딩 스타일 가이드 준수
        - 네이밍 컨벤션
        - 코드 가독성 개선점

        **⚡ 성능 최적화**
        - 알고리즘 효율성
        - 메모리 사용량 최적화
        - 불필요한 연산 제거

        **🔧 리팩토링 제안**
        - 코드 구조 개선
        - 중복 코드 제거
        - 함수/클래스 분리

        **🧪 테스트 케이스**
        - 단위 테스트 제안
        - 엣지 케이스 테스트
        - 테스트 시나리오

        **📊 복잡도 분석**
        - 시간 복잡도: O(?)
        - 공간 복잡도: O(?)
        - 순환 복잡도 평가

        각 섹션은 이모지와 함께 명확히 구분하고, 구체적인 개선 코드 예시도 포함해주세요.
        한국어로 응답해주세요.
        """
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"다음 {language} 코드를 리뷰해주세요:\n\n```{language.lower()}\n{code_snippet}\n```"}
        ]
    
    def get_quick_fix(self, code_snippet: str, issue_description: str, language: str = "Python") -> str:
        """
        특정 이슈에 대한 빠른 수정 제안
        
        Args:
            code_snippet: 원본 코드
            issue_description: 수정이 필요한 이슈 설명
            language: 프로그래밍 언어
            
        Returns:
            수정된 코드 및 설명
        """
        try:
            messages = [
                {"role": "system", "content": f"""
                당신은 {language} 전문가입니다. 
                주어진 코드의 특정 이슈를 수정하고, 수정 이유와 함께 개선된 코드를 제공해주세요.
                한국어로 응답해주세요.
                """},
                {"role": "user", "content": f"""
                다음 코드에서 '{issue_description}' 문제를 수정해주세요:
                
                ```{language.lower()}
                {code_snippet}
                ```
                
                수정된 코드와 수정 이유를 설명해주세요.
                """}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"코드 수정 제안 중 오류가 발생했습니다: {str(e)}"
    
    def generate_test_cases(self, code_snippet: str, language: str = "Python") -> str:
        """
        코드에 대한 테스트 케이스 생성
        
        Args:
            code_snippet: 테스트할 코드
            language: 프로그래밍 언어
            
        Returns:
            테스트 케이스 코드
        """
        try:
            messages = [
                {"role": "system", "content": f"""
                당신은 {language} 테스트 전문가입니다.
                주어진 코드에 대해 포괄적인 단위 테스트를 작성해주세요.
                다양한 엣지 케이스를 포함하고, {language}의 표준 테스트 프레임워크를 사용해주세요.
                한국어 주석으로 설명을 추가해주세요.
                """},
                {"role": "user", "content": f"""
                다음 {language} 코드에 대한 테스트 케이스를 작성해주세요:
                
                ```{language.lower()}
                {code_snippet}
                ```
                """}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"테스트 케이스 생성 중 오류가 발생했습니다: {str(e)}"
