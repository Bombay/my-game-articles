# Task 01: 프로젝트 초기 설정 및 환경 구성

## 📋 체크리스트

- [x] Python 가상환경 생성 및 활성화
- [x] MCP SDK 및 필수 라이브러리 설치
- [x] 프로젝트 기본 폴더 구조 생성
- [x] 설정 파일 및 환경 변수 설정
- [x] Git 초기화 및 .gitignore 설정

## 📝 상세 내용

### 구현할 기능들

- Python 3.9+ 환경 설정
- MCP 서버 개발을 위한 필수 패키지 설치
- 프로젝트 기본 구조 생성
- 개발 환경 표준화

### 코드 예시

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install mcp httpx playwright python-dotenv
```

## 🛠️ 기술적 세부사항

### 사용할 기술 스택

- **Python**: 3.9+
- **MCP SDK**: Anthropic MCP Python SDK
- **HTTP Client**: httpx (async 지원)
- **브라우저 자동화**: playwright (로스트아크용)
- **환경 설정**: python-dotenv

### 파일 구조

```
my-game-articles/
├── src/
│   ├── __init__.py
│   ├── server.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── game_news.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── lordnine.py
│   │   ├── epic_seven.py
│   │   └── lost_ark.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── lordnine.py
│   │   ├── epic_seven.py
│   │   └── lost_ark.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

### 의존성

```txt
mcp>=0.1.0
httpx>=0.24.0
playwright>=1.40.0
python-dotenv>=1.0.0
pytest>=7.0.0
```

## ✅ 완료 조건

- [x] 가상환경이 정상적으로 생성되고 활성화됨
- [x] 모든 필수 패키지가 설치됨
- [x] 프로젝트 폴더 구조가 올바르게 생성됨
- [x] Git 저장소가 초기화됨
- [x] requirements.txt 파일이 생성됨

### 검증 방법

```bash
# 패키지 설치 확인
pip list | grep mcp
pip list | grep httpx

# 폴더 구조 확인
tree src/

# Git 상태 확인
git status
```
