"""
피드백 수집 및 분석 모듈
사용자 피드백을 수집하고 서비스 개선에 활용
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


class FeedbackCollector:
    """사용자 피드백 수집 및 관리 클래스"""
    
    def __init__(self, feedback_file: str = "feedback_data.json"):
        """
        피드백 수집기 초기화
        
        Args:
            feedback_file: 피드백 데이터를 저장할 파일 경로
        """
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback_data()
    
    def _load_feedback_data(self) -> List[Dict]:
        """저장된 피드백 데이터 로드"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_feedback_data(self):
        """피드백 데이터 저장"""
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"피드백 저장 중 오류: {e}")
    
    def collect_feedback(self, 
                        review_result: str, 
                        user_code: str, 
                        language: str,
                        rating: int, 
                        helpful: bool, 
                        suggestions: str = "") -> Dict:
        """
        사용자 피드백 수집
        
        Args:
            review_result: AI가 제공한 리뷰 결과
            user_code: 사용자가 제출한 코드
            language: 프로그래밍 언어
            rating: 평점 (1-5)
            helpful: 도움됨 여부
            suggestions: 개선 제안사항
            
        Returns:
            수집된 피드백 데이터
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "language": language,
            "code_length": len(user_code),
            "review_length": len(review_result),
            "rating": rating,
            "helpful": helpful,
            "suggestions": suggestions,
            "session_id": self._generate_session_id()
        }
        
        self.feedback_data.append(feedback_entry)
        self._save_feedback_data()
        
        return feedback_entry
    
    def _generate_session_id(self) -> str:
        """세션 ID 생성"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def get_feedback_statistics(self) -> Dict:
        """피드백 통계 정보 반환"""
        if not self.feedback_data:
            return {
                "total_reviews": 0,
                "average_rating": 0,
                "helpful_percentage": 0,
                "language_distribution": {},
                "recent_suggestions": []
            }
        
        df = pd.DataFrame(self.feedback_data)
        
        # 기본 통계
        total_reviews = len(df)
        avg_rating = df['rating'].mean()
        helpful_percentage = (df['helpful'].sum() / total_reviews) * 100
        
        # 언어별 분포
        language_dist = df['language'].value_counts().to_dict()
        
        # 최근 제안사항 (빈 문자열이 아닌 것만)
        recent_suggestions = df[df['suggestions'] != '']['suggestions'].tail(5).tolist()
        
        return {
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 2),
            "helpful_percentage": round(helpful_percentage, 2),
            "language_distribution": language_dist,
            "recent_suggestions": recent_suggestions
        }
    
    def get_improvement_insights(self) -> List[str]:
        """개선 인사이트 제공"""
        stats = self.get_feedback_statistics()
        insights = []
        
        if stats["total_reviews"] == 0:
            return ["아직 피드백 데이터가 없습니다."]
        
        # 평점 기반 인사이트
        if stats["average_rating"] < 3.0:
            insights.append("⚠️ 평균 평점이 낮습니다. 리뷰 품질 개선이 필요합니다.")
        elif stats["average_rating"] >= 4.0:
            insights.append("✅ 높은 사용자 만족도를 보이고 있습니다.")
        
        # 도움됨 비율 기반 인사이트
        if stats["helpful_percentage"] < 60:
            insights.append("📈 사용자가 도움되지 않는다고 느끼는 비율이 높습니다.")
        elif stats["helpful_percentage"] >= 80:
            insights.append("🎯 대부분의 사용자가 리뷰를 유용하다고 평가합니다.")
        
        # 언어별 분포 인사이트
        top_language = max(stats["language_distribution"], key=stats["language_distribution"].get)
        insights.append(f"🔥 가장 많이 사용되는 언어: {top_language}")
        
        return insights


class SessionManager:
    """사용자 세션 관리 클래스"""
    
    def __init__(self):
        self.session_data = {}
    
    def start_session(self, session_id: str) -> Dict:
        """새 세션 시작"""
        self.session_data[session_id] = {
            "start_time": datetime.now(),
            "code_reviews": [],
            "feedback_submitted": False
        }
        return self.session_data[session_id]
    
    def add_review_to_session(self, session_id: str, review_data: Dict):
        """세션에 리뷰 데이터 추가"""
        if session_id in self.session_data:
            self.session_data[session_id]["code_reviews"].append(review_data)
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """세션 히스토리 반환"""
        if session_id in self.session_data:
            return self.session_data[session_id]["code_reviews"]
        return []
