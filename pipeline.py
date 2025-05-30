"""
코드 리뷰 챗봇 파이프라인
전체 코드 리뷰 프로세스를 관리하는 파이프라인
"""
from typing import Dict, List, Optional, Tuple
from code_reviewer import CodeReviewHelper
from feedback_collector import FeedbackCollector, SessionManager
from datetime import datetime


class CodeReviewPipeline:
    """코드 리뷰 전체 파이프라인 관리 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        파이프라인 초기화
        
        Args:
            api_key: OpenAI API 키
        """
        self.reviewer = CodeReviewHelper(api_key)
        self.feedback_collector = FeedbackCollector()
        self.session_manager = SessionManager()
        self.current_session_id = None
        
    def start_new_session(self) -> str:
        """새로운 리뷰 세션 시작"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        self.session_manager.start_session(session_id)
        self.current_session_id = session_id
        return session_id
    
    def process_code_review(self, 
                           code_snippet: str, 
                           language: str = "Python",
                           review_type: str = "comprehensive") -> Dict:
        """
        코드 리뷰 프로세스 실행
        
        Args:
            code_snippet: 리뷰할 코드
            language: 프로그래밍 언어
            review_type: 리뷰 유형 ("comprehensive", "quick_fix", "test_cases")
            
        Returns:
            리뷰 결과 딕셔너리
        """
        if not self.current_session_id:
            self.start_new_session()
        
        try:
            # 코드 유효성 검증
            validation_result = self._validate_code_input(code_snippet, language)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "timestamp": datetime.now().isoformat()
                }
            
            # 리뷰 타입에 따른 처리
            if review_type == "comprehensive":
                review_result = self.reviewer.analyze_code(code_snippet, language)
            elif review_type == "test_cases":
                review_result = self.reviewer.generate_test_cases(code_snippet, language)
            else:
                review_result = self.reviewer.analyze_code(code_snippet, language)
            
            # 결과 데이터 구성
            result_data = {
                "success": True,
                "review_result": review_result,
                "code_snippet": code_snippet,
                "language": language,
                "review_type": review_type,
                "timestamp": datetime.now().isoformat(),
                "session_id": self.current_session_id,
                "code_stats": self._analyze_code_stats(code_snippet)
            }
            
            # 세션에 추가
            self.session_manager.add_review_to_session(
                self.current_session_id, 
                result_data
            )
            
            return result_data
            
        except Exception as e:
            return {
                "success": False,
                "error": f"리뷰 처리 중 오류가 발생했습니다: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def process_quick_fix(self, 
                         code_snippet: str, 
                         issue_description: str,
                         language: str = "Python") -> Dict:
        """
        빠른 수정 제안 프로세스
        
        Args:
            code_snippet: 원본 코드
            issue_description: 수정할 이슈 설명
            language: 프로그래밍 언어
            
        Returns:
            수정 제안 결과
        """
        try:
            fix_result = self.reviewer.get_quick_fix(
                code_snippet, 
                issue_description, 
                language
            )
            
            return {
                "success": True,
                "fix_result": fix_result,
                "original_code": code_snippet,
                "issue": issue_description,
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"수정 제안 중 오류가 발생했습니다: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def collect_user_feedback(self, 
                             review_result: str,
                             user_code: str,
                             language: str,
                             rating: int,
                             helpful: bool,
                             suggestions: str = "") -> Dict:
        """
        사용자 피드백 수집 프로세스
        
        Args:
            review_result: 리뷰 결과
            user_code: 사용자 코드
            language: 프로그래밍 언어
            rating: 평점 (1-5)
            helpful: 도움됨 여부
            suggestions: 개선 제안사항
            
        Returns:
            피드백 수집 결과
        """
        try:
            feedback_data = self.feedback_collector.collect_feedback(
                review_result=review_result,
                user_code=user_code,
                language=language,
                rating=rating,
                helpful=helpful,
                suggestions=suggestions
            )
            
            return {
                "success": True,
                "message": "피드백이 성공적으로 수집되었습니다.",
                "feedback_data": feedback_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"피드백 수집 중 오류가 발생했습니다: {str(e)}"
            }
    
    def get_session_history(self) -> List[Dict]:
        """현재 세션의 리뷰 히스토리 반환"""
        if self.current_session_id:
            return self.session_manager.get_session_history(self.current_session_id)
        return []
    
    def get_feedback_statistics(self) -> Dict:
        """피드백 통계 정보 반환"""
        return self.feedback_collector.get_feedback_statistics()
    
    def get_improvement_insights(self) -> List[str]:
        """서비스 개선 인사이트 반환"""
        return self.feedback_collector.get_improvement_insights()
    
    def _validate_code_input(self, code_snippet: str, language: str) -> Dict:
        """코드 입력 유효성 검증"""
        if not code_snippet or not code_snippet.strip():
            return {
                "valid": False,
                "error": "코드가 입력되지 않았습니다."
            }
        
        if len(code_snippet) > 10000:  # 10KB 제한
            return {
                "valid": False,
                "error": "코드가 너무 깁니다. (최대 10,000자)"
            }
        
        if not language:
            return {
                "valid": False,
                "error": "프로그래밍 언어를 선택해주세요."
            }
        
        return {"valid": True}
    
    def _analyze_code_stats(self, code_snippet: str) -> Dict:
        """코드 통계 분석"""
        lines = code_snippet.split('\n')
        
        return {
            "total_lines": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "total_characters": len(code_snippet),
            "estimated_complexity": self._estimate_complexity(code_snippet)
        }
    
    def _estimate_complexity(self, code_snippet: str) -> str:
        """코드 복잡도 추정 (간단한 휴리스틱)"""
        # 간단한 복잡도 추정 로직
        lines = len(code_snippet.split('\n'))
        
        if lines < 10:
            return "낮음"
        elif lines < 50:
            return "보통"
        elif lines < 100:
            return "높음"
        else:
            return "매우 높음"
