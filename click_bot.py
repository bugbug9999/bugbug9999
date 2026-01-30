#!/usr/bin/env python3
"""
웹사이트 클릭 봇 - 네이버 서버 시간 기준 정확한 클릭
"""

import time
import requests
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ============ 설정 ============
TARGET_URL = "https://www.google.com"  # 클릭할 웹페이지 URL (여기에 실제 URL 입력)
TARGET_HOUR = 14  # 목표 시간 (24시간 형식, 14 = 오후 2시)
TARGET_MINUTE = 0  # 목표 분
TARGET_SECOND = 0  # 목표 초

# 클릭할 버튼 설정 (아래 중 하나만 사용)
# CSS Selector 사용 시
BUTTON_SELECTOR = "button.submit"  # 여기에 버튼 selector 입력
SELECTOR_TYPE = "css"  # "css" 또는 "xpath"

# XPath 사용 시 (텍스트로 찾을 때 유용)
# BUTTON_SELECTOR = "//button[contains(text(), '구매하기')]"
# SELECTOR_TYPE = "xpath"

# 클릭 전 페이지 새로고침 여부
REFRESH_BEFORE_CLICK = True

# 새로고침 시작 시간 (목표 시간 몇 초 전부터)
REFRESH_START_SECONDS = 3
# =============================


def get_naver_server_time():
    """네이버 서버 시간을 가져옵니다."""
    try:
        response = requests.head("https://www.naver.com", timeout=5)
        date_header = response.headers.get('Date')
        if date_header:
            server_time = parsedate_to_datetime(date_header)
            # UTC를 KST(+9)로 변환
            kst_time = server_time + timedelta(hours=9)
            return kst_time
    except Exception as e:
        print(f"[오류] 네이버 서버 시간 가져오기 실패: {e}")
    return None


def get_time_offset():
    """로컬 시간과 네이버 서버 시간의 차이를 계산합니다."""
    offsets = []
    print("[정보] 네이버 서버 시간 동기화 중...")

    for i in range(5):
        local_before = datetime.now()
        server_time = get_naver_server_time()
        local_after = datetime.now()

        if server_time:
            # 네트워크 지연 보정 (왕복 시간의 절반)
            local_mid = local_before + (local_after - local_before) / 2
            offset = (server_time.replace(tzinfo=None) - local_mid).total_seconds()
            offsets.append(offset)
            print(f"  측정 {i+1}/5: 오프셋 = {offset:.3f}초")
        time.sleep(0.2)

    if offsets:
        # 중간값 사용 (이상치 제거)
        offsets.sort()
        median_offset = offsets[len(offsets) // 2]
        print(f"[정보] 시간 오프셋: {median_offset:.3f}초 (로컬 시간 + {median_offset:.3f}초 = 서버 시간)")
        return median_offset

    print("[경고] 시간 동기화 실패, 로컬 시간 사용")
    return 0


def get_adjusted_time(offset):
    """오프셋을 적용한 현재 시간을 반환합니다."""
    return datetime.now() + timedelta(seconds=offset)


def setup_browser():
    """브라우저를 설정하고 반환합니다."""
    print("[정보] 브라우저 설정 중...")

    options = Options()
    # options.add_argument("--headless")  # 브라우저 창 숨기기 (디버깅 시 주석 처리)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # User-Agent 설정
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # webdriver 감지 우회
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    return driver


def wait_for_target_time(offset, target_time):
    """목표 시간까지 대기합니다."""
    print(f"\n[대기] 목표 시간: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while True:
        current = get_adjusted_time(offset)
        remaining = (target_time - current).total_seconds()

        if remaining <= 0:
            break

        if remaining > 60:
            print(f"\r[대기] 남은 시간: {int(remaining // 60)}분 {int(remaining % 60)}초  ", end="", flush=True)
            time.sleep(1)
        elif remaining > 10:
            print(f"\r[대기] 남은 시간: {remaining:.1f}초  ", end="", flush=True)
            time.sleep(0.1)
        elif remaining > 1:
            print(f"\r[대기] 남은 시간: {remaining:.2f}초  ", end="", flush=True)
            time.sleep(0.01)
        else:
            print(f"\r[대기] 남은 시간: {remaining:.3f}초  ", end="", flush=True)
            time.sleep(0.001)

    print()


def click_button(driver, selector, selector_type):
    """버튼을 클릭합니다."""
    try:
        if selector_type == "xpath":
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR

        element = driver.find_element(by, selector)
        element.click()
        return True
    except Exception as e:
        print(f"[오류] 클릭 실패: {e}")
        return False


def run_bot():
    """봇을 실행합니다."""
    print("=" * 50)
    print("     웹사이트 클릭 봇 - 네이버 서버 시간 기준")
    print("=" * 50)
    print(f"\n[설정]")
    print(f"  - URL: {TARGET_URL}")
    print(f"  - 목표 시간: {TARGET_HOUR:02d}:{TARGET_MINUTE:02d}:{TARGET_SECOND:02d}")
    print(f"  - 버튼 선택자: {BUTTON_SELECTOR}")
    print(f"  - 선택자 타입: {SELECTOR_TYPE}")
    print(f"  - 새로고침: {'예' if REFRESH_BEFORE_CLICK else '아니오'}")

    # 시간 동기화
    offset = get_time_offset()
    current = get_adjusted_time(offset)

    # 오늘 목표 시간 계산
    target_time = current.replace(
        hour=TARGET_HOUR,
        minute=TARGET_MINUTE,
        second=TARGET_SECOND,
        microsecond=0
    )

    # 이미 지났으면 내일로
    if current >= target_time:
        target_time += timedelta(days=1)
        print(f"\n[정보] 오늘 목표 시간이 지났습니다. 내일 {target_time.strftime('%Y-%m-%d %H:%M:%S')}에 실행됩니다.")

    # 브라우저 설정
    driver = setup_browser()

    try:
        # 페이지 로드
        print(f"\n[정보] 페이지 로드 중: {TARGET_URL}")
        driver.get(TARGET_URL)

        print("\n" + "=" * 50)
        print("  로그인이 필요하면 지금 로그인하세요!")
        print("  준비되면 Enter를 누르세요...")
        print("=" * 50)
        input()

        # 새로고침 시작 시간
        refresh_time = target_time - timedelta(seconds=REFRESH_START_SECONDS)

        # 새로고침 시간까지 대기
        if REFRESH_BEFORE_CLICK:
            wait_for_target_time(offset, refresh_time)
            print(f"\n[정보] 페이지 새로고침!")
            driver.refresh()

        # 목표 시간까지 대기
        wait_for_target_time(offset, target_time)

        # 클릭 실행
        click_time = get_adjusted_time(offset)
        print(f"\n[클릭] 클릭 시도 시간: {click_time.strftime('%H:%M:%S.%f')}")

        success = click_button(driver, BUTTON_SELECTOR, SELECTOR_TYPE)

        if success:
            print("[성공] 버튼 클릭 완료!")
        else:
            print("[실패] 버튼 클릭 실패")

        # 결과 확인을 위해 대기
        print("\n[정보] 결과를 확인하세요. 종료하려면 Enter를 누르세요...")
        input()

    finally:
        driver.quit()
        print("[정보] 브라우저 종료")


if __name__ == "__main__":
    run_bot()
