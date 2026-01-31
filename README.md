# W.W.H/1.3.1
따따하/1.3.1 작성을 A.I.를 활용하여 ‘책 제목’만 입력해도 양식에 맞게 작성하는 웹사이트 프로젝트


# 독서감상문 자동 생성 웹사이트 (Gemini + Selenium)

이 프로젝트는 사용자가 입력한 책 정보를 바탕으로 웹 크롤링을 통해 책 내용을 수집하고, Google Gemini AI가 독서감상문을 자동으로 작성해주는 웹사이트입니다.

## 주요 기능

1. **자동 책 정보 수집**: Selenium을 이용한 웹 크롤링으로 책의 줄거리와 내용 자동 수집
1. **AI 독서감상문 생성**: Google Gemini API를 활용하여 수집된 정보를 바탕으로 독서감상문 자동 작성
1. **사용자 친화적 인터페이스**: 간편한 입력 폼과 실시간 생성 과정 표시

## 프로젝트 구조

```
.
├── index.html          # 프론트엔드 (사용자 인터페이스)
├── app.py             # 백엔드 서버 (Flask + Gemini + Selenium)
├── requirements.txt   # Python 패키지 목록
└── README.md         # 이 파일
```

## 설치 방법

### 1. Python 패키지 설치

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install flask flask-cors selenium google-generativeai webdriver-manager
```

### 2. Chrome 브라우저 및 ChromeDriver 설치

**자동 설치 (권장)**

- `webdriver-manager` 패키지가 자동으로 ChromeDriver를 관리합니다.

**수동 설치**

- Chrome 브라우저가 설치되어 있어야 합니다.
- ChromeDriver 다운로드: https://chromedriver.chromium.org/

### 3. Google Gemini API 키 설정

Google AI Studio에서 API 키를 발급받으세요: https://makersuite.google.com/app/apikey

**방법 1: 환경 변수 설정 (권장)**

Windows:

```bash
set GEMINI_API_KEY=your-api-key-here
```

Mac/Linux:

```bash
export GEMINI_API_KEY=your-api-key-here
```

**방법 2: 코드에 직접 입력**

`app.py` 파일에서 다음 부분을 수정:

```python
GEMINI_API_KEY = "your-api-key-here"  # 직접 API 키 입력
genai.configure(api_key=GEMINI_API_KEY)
```

## 실행 방법

### 1. 백엔드 서버 실행

```bash
python app.py
```

서버가 `http://localhost:5000`에서 실행됩니다.

### 2. 프론트엔드 실행

`index.html` 파일을 웹 브라우저로 열거나, 간단한 HTTP 서버를 실행:

```bash
# Python을 이용한 간단한 서버 (다른 터미널에서 실행)
python -m http.server 8000
```

그 다음 브라우저에서 `http://localhost:8000/index.html`로 접속합니다.

## 사용 방법

1. 웹 페이지에서 다음 정보를 입력합니다:
- 도서명
- 저자
- 출판사
- 출판 연도
1. “독서감상문 생성하기” 버튼을 클릭합니다.
1. 시스템이 다음 과정을 자동으로 수행합니다:
- Google과 Naver에서 책 정보 검색 및 크롤링
- 수집된 정보를 바탕으로 Gemini AI가 독서감상문 작성
- 결과를 화면에 표시

## 프롬프트 커스터마이징

`app.py` 파일의 다음 부분에서 프롬프트를 수정할 수 있습니다:

```python
# ============================================
# 여기에 프롬프트를 넣어주세요.
# ============================================
prompt = f"""당신은 전문 독서감상문 작성자입니다.
...
"""
# ============================================
```

### 프롬프트 작성 시 사용 가능한 변수

- `{book_title}` - 도서명
- `{author}` - 저자
- `{publisher}` - 출판사
- `{year}` - 출판 연도
- `{book_content}` - 크롤링으로 수집된 책 내용

### 프롬프트 작성 예시

```python
prompt = f"""당신은 고등학생을 위한 독서감상문 작성 전문가입니다.

【책 정보】
- 도서명: {book_title}
- 저자: {author}
- 출판사: {publisher}
- 출판 연도: {year}년

【수집된 책 내용】
{book_content}

【작성 지침】
1. 고등학생 수준의 어휘와 표현 사용
2. 비판적 사고와 분석적 관점 포함
3. 현대 사회와의 연관성 논의
4. 총 1000-1500자 분량

【형식】
서론: 책 선택 동기와 시대적 배경
본론 1: 작품 분석 (주제, 갈등, 인물)
본론 2: 인상적인 장면과 문학적 기법
본론 3: 현대적 의미와 시사점
결론: 개인적 성찰과 독서의 가치

학술적이면서도 개인적인 경험이 담긴 독서감상문을 작성해주세요.
"""
```

## 크롤링 방식 수정

`app.py`의 `scrape_book_info()` 함수에서 크롤링 방식을 수정할 수 있습니다:

```python
def scrape_book_info(book_title, author, publisher, year):
    # 여기서 크롤링 로직을 수정할 수 있습니다
    # 예: 다른 웹사이트 추가, CSS 선택자 변경 등
    pass
```

### 크롤링 대상 사이트 추가 예시

```python
# 교보문고 검색
kyobo_url = f"https://search.kyobobook.co.kr/search?keyword={book_title}"
driver.get(kyobo_url)
# ... 정보 추출 코드

# 알라딘 검색
aladin_url = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord={book_title}"
driver.get(aladin_url)
# ... 정보 추출 코드
```

## 주의사항

- **API 키 필수**: Google Gemini API 키가 없으면 작동하지 않습니다.
- **Chrome 필수**: Selenium 크롤링을 위해 Chrome 브라우저가 설치되어 있어야 합니다.
- **API 요금**: Gemini API 사용량에 따라 요금이 부과될 수 있습니다 (무료 할당량 확인 필요).
- **크롤링 제한**: 일부 웹사이트는 크롤링을 제한할 수 있습니다.
- **속도**: 크롤링과 AI 생성 과정으로 인해 20-40초 정도 소요될 수 있습니다.

## 문제 해결

### “서버와 연결할 수 없습니다” 오류

- `app.py`가 실행 중인지 확인하세요
- 포트 5000이 사용 가능한지 확인하세요

### API 키 오류

- 환경 변수가 올바르게 설정되었는지 확인하세요
- Gemini API 키가 유효한지 확인하세요 (https://makersuite.google.com/)

### ChromeDriver 오류

- Chrome 브라우저가 최신 버전인지 확인하세요
- `webdriver-manager`가 올바르게 설치되었는지 확인하세요

### 크롤링 실패

- 인터넷 연결 상태를 확인하세요
- 검색 결과가 없는 경우 다른 검색어로 시도하세요
- 일부 사이트가 차단되었을 수 있습니다

### CORS 오류

- `flask-cors` 패키지가 설치되어 있는지 확인하세요

## 성능 최적화 팁

1. **캐싱 구현**: 같은 책에 대한 크롤링 결과를 캐싱하여 재사용
1. **병렬 처리**: 여러 사이트를 동시에 크롤링
1. **타임아웃 설정**: 느린 사이트를 건너뛰기
1. **사용자 피드백**: 크롤링 진행 상황을 실시간으로 표시

## 라이선스 및 사용 제한

- 이 프로젝트는 교육 목적으로 제작되었습니다.
- 웹 크롤링 시 각 웹사이트의 이용 약관을 준수하세요.
- 과도한 크롤링은 IP 차단의 원인이 될 수 있습니다.