# 웹사이트 클릭 봇

네이버 서버 시간 기준으로 정확한 시간에 웹페이지 버튼을 클릭하는 봇입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 1. 설정 변경

`click_bot.py` 파일 상단의 설정을 수정하세요:

```python
# 클릭할 웹페이지 URL
TARGET_URL = "https://example.com"

# 목표 시간 (24시간 형식)
TARGET_HOUR = 14    # 오후 2시
TARGET_MINUTE = 0
TARGET_SECOND = 0

# 클릭할 버튼 (CSS Selector 또는 XPath)
BUTTON_SELECTOR = "button.submit"
SELECTOR_TYPE = "css"  # "css" 또는 "xpath"
```

### 2. 버튼 찾는 방법

크롬에서 F12 (개발자 도구) → 버튼 우클릭 → "검사" → 요소 우클릭 → "Copy" → "Copy selector" 또는 "Copy XPath"

**CSS Selector 예시:**
```python
BUTTON_SELECTOR = "button.buy-btn"
BUTTON_SELECTOR = "#purchase-button"
BUTTON_SELECTOR = "input[type='submit']"
```

**XPath 예시 (텍스트로 찾을 때):**
```python
BUTTON_SELECTOR = "//button[contains(text(), '구매하기')]"
BUTTON_SELECTOR = "//button[text()='예약']"
SELECTOR_TYPE = "xpath"
```

### 3. 실행

```bash
python click_bot.py
```

### 4. 실행 순서

1. 브라우저가 열리고 페이지가 로드됩니다
2. **로그인이 필요하면 직접 로그인하세요**
3. 준비되면 Enter를 누르세요
4. 봇이 목표 시간까지 대기합니다
5. 시간이 되면 자동으로 새로고침 + 클릭합니다

## 주의사항

- 크롬 브라우저가 설치되어 있어야 합니다
- ChromeDriver는 자동으로 설치됩니다
- 봇 실행 후 로그인은 직접 해야 합니다
