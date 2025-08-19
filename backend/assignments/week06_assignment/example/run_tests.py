#!/usr/bin/env python3
"""
테스트 실행 스크립트
- 환경 설정 및 테스트 실행
- 커버리지 리포트 생성
"""
import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """테스트 환경 변수 설정"""
    os.environ["TESTING"] = "1"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["LOG_LEVEL"] = "INFO"
    print("✅ 테스트 환경 변수 설정 완료")

def check_dependencies():
    """필요한 의존성 확인"""
    try:
        import pytest
        import httpx
        import sqlalchemy
        import fastapi
        print("✅ 필수 의존성 확인 완료")
        return True
    except ImportError as e:
        print(f"❌ 의존성 누락: {e}")
        print("다음 명령으로 의존성을 설치하세요:")
        print("pip install -r requirements-test.txt")
        return False

def run_tests(args=None):
    """pytest 실행"""
    if args is None:
        args = []
    
    # 기본 pytest 명령어 구성
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",  # 상세 출력
        "--tb=short",  # 짧은 트레이스백
        "--cov=.",  # 커버리지 측정
        "--cov-report=html:htmlcov",  # HTML 리포트
        "--cov-report=term-missing",  # 터미널 리포트
        "--cov-fail-under=80",  # 80% 커버리지 요구
    ]
    
    # 추가 인자가 있으면 포함
    if args:
        cmd.extend(args)
    
    print(f"🚀 테스트 실행: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("📚 도서 관리 시스템 API 테스트 실행")
    print("=" * 50)
    
    # 1. 환경 설정
    setup_environment()
    
    # 2. 의존성 확인
    if not check_dependencies():
        sys.exit(1)
    
    # 3. 테스트 실행
    sys_args = sys.argv[1:]  # 스크립트에 전달된 추가 인자
    
    if run_tests(sys_args):
        print("\n✅ 모든 테스트가 성공적으로 완료되었습니다!")
        print("📊 커버리지 리포트: htmlcov/index.html")
    else:
        print("\n❌ 일부 테스트가 실패했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()