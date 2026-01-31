from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import google.generativeai as genai
import os
import time

app = Flask(**name**)
CORS(app)  # CORS 활성화

# Gemini API 설정

# 환경 변수에서 API 키를 가져오거나, 직접 입력하세요

GEMINI_API_KEY = os.environ.get(“GEMINI_API_KEY”)  # 또는 직접 API 키 입력
genai.configure(api_key=GEMINI_API_KEY)

def scrape_book_info(book_title, author, publisher, year):
“””
Selenium을 사용하여 책 정보를 크롤링하는 함수
“””
chrome_options = Options()
chrome_options.add_argument(’–headless’)  # 브라우저 창을 띄우지 않음
chrome_options.add_argument(’–no-sandbox’)
chrome_options.add_argument(’–disable-dev-shm-usage’)
chrome_options.add_argument(’–disable-gpu’)
chrome_options.add_argument(‘user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36’)

```
driver = None
book_content = ""

try:
    driver = webdriver.Chrome(options=chrome_options)
    
    # 검색 쿼리 생성
    search_query = f"{book_title} {author} 줄거리 내용"
    google_search_url = f"https://www.google.com/search?q={search_query}"
    
    driver.get(google_search_url)
    time.sleep(2)
    
    # 검색 결과에서 텍스트 추출
    try:
        # Google 검색 결과의 스니펫들을 수집
        snippets = driver.find_elements(By.CSS_SELECTOR, '.VwiC3b, .yXK7lf, .hgKElc, .s3v9rd')
        
        for snippet in snippets[:5]:  # 상위 5개 결과만 수집
            text = snippet.text.strip()
            if text and len(text) > 50:  # 의미있는 길이의 텍스트만 수집
                book_content += text + "\n\n"
        
        # 추가로 네이버 책 정보 검색
        naver_search_url = f"https://search.naver.com/search.naver?query={book_title}+{author}+책"
        driver.get(naver_search_url)
        time.sleep(2)
        
        # 네이버 검색 결과에서 책 설명 추출
        naver_snippets = driver.find_elements(By.CSS_SELECTOR, '.detail_info, .book_info, .txt_block')
        for snippet in naver_snippets[:3]:
            text = snippet.text.strip()
            if text and len(text) > 50:
                book_content += text + "\n\n"
                
    except Exception as e:
        print(f"검색 결과 추출 중 오류: {e}")
    
    if not book_content:
        book_content = f"'{book_title}' (저자: {author}, 출판사: {publisher}, {year}년)에 대한 상세 정보를 찾지 못했습니다."
        
except Exception as e:
    print(f"크롤링 오류: {e}")
    book_content = f"책 정보를 검색하는 중 오류가 발생했습니다: {str(e)}"
    
finally:
    if driver:
        driver.quit()

return book_content
```

@app.route(’/generate’, methods=[‘POST’])
def generate_essay():
try:
# 프론트엔드에서 받은 데이터
data = request.json
book_title = data.get(‘bookTitle’, ‘’)
author = data.get(‘author’, ‘’)
publisher = data.get(‘publisher’, ‘’)
year = data.get(‘year’, ‘’)

```
    print(f"책 정보 검색 시작: {book_title} - {author}")
    
    # 1단계: 웹 크롤링으로 책 정보 수집
    book_content = scrape_book_info(book_title, author, publisher, year)
    
    print(f"크롤링 완료. 수집된 내용 길이: {len(book_content)}")
    
    # ============================================
    # 여기에 프롬프트를 넣어주세요.
    # ============================================
    prompt = f"""당신은 전문 독서감상문 작성자입니다. 다음 정보를 바탕으로 독서감상문을 작성해주세요.
```

【책 정보】

- 도서명: {book_title}
- 저자: {author}
- 출판사: {publisher}
- 출판 연도: {year}년

【수집된 책 내용 정보】
{book_content}

【작성 요구사항】
위 정보를 바탕으로 다음 형식에 맞춰 독서감상문을 작성해주세요:

1. 서론 (2-3문단)
- 이 책을 선택하게 된 이유
- 책에 대한 첫인상
1. 본론 (3-4문단)
- 책의 주요 내용과 줄거리 요약
- 인상 깊었던 장면이나 구절
- 책의 핵심 메시지와 주제
1. 결론 (2-3문단)
- 이 책을 읽고 느낀 점
- 나에게 준 교훈과 깨달음
- 이 책을 다른 사람에게 추천하고 싶은 이유

자연스럽고 진솔한 문체로 작성하며, 구체적인 예시를 포함해주세요.
독서감상문은 총 800-1200자 정도로 작성해주세요.”””
# ============================================

```
    # 2단계: Gemini API로 독서감상문 생성
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    result = response.text
    
    print("독서감상문 생성 완료")
    
    return jsonify({
        'success': True,
        'result': result
    })
    
except Exception as e:
    print(f"에러 발생: {str(e)}")
    return jsonify({
        'success': False,
        'error': f'오류가 발생했습니다: {str(e)}'
    }), 500
```

@app.route(’/’, methods=[‘GET’])
def home():
return “독서감상문 생성 API 서버가 실행 중입니다. (Gemini + Selenium)”

if **name** == ‘**main**’:
app.run(debug=True, port=5000)