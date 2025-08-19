

1. conftest.py
    (1) : 실제 데이터베이스에 영향을 최소한으로 하기 위해, sqlite를 쓰긴 하지만,
            기존의 서버에서 mysql 테스트용 데이터베이스를 하나 만들었음.
    
    (2) : @pytest.fixture
            def test_db(): 테스트 전에 테이블 데이터 모두 비우고,
                            이세션을 테스트 함수에서 쓰도록 하고, 끝나면 닫기.

    (3) : @pytest.fixture(autouse=True)
            def override_db(test_db): 위에서 정의한 test_db에 기존 get_db정의


실행방법
pytest tests/test_main.py::함수명--별도실행