import time
import os
import re
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- 讀取 GitHub Secrets (環境變數) ---
STUDENT_ID = os.environ.get('STUDENT_ID')
STUDENT_PW = os.environ.get('STUDENT_PW')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER')

def send_grade_email(grade_list, count):
    msg = MIMEText(f"嗨！(｡･ω･｡)ﾉ\n\niTouch 成績更新囉！目前已有 {count} 科出分。\n\n清單如下：\n" + "\n".join(grade_list))
    msg['Subject'] = f"🔔 iTouch 成績更新通知 ({count}科)"
    msg['From'] = f"成績機器人 <{EMAIL_SENDER}>"
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASS)
            server.send_message(msg)
        print("✅ 通知信件已發送。")
    except Exception as e:
        print(f"❌ 郵件發送失敗：{e}")

def run_grade_check():
    options = Options()
    # GitHub Actions 必須使用無頭模式 (headless)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
    wait = WebDriverWait(driver, 30)

    try:
        driver.get("https://itouch.cycu.edu.tw/")
        time.sleep(3)
        
        # 登入流程
        xpath_user = "/html/body/div/div[2]/div[1]/div/div[1]/div/div/div/form/div[1]/input"
        xpath_pass = "/html/body/div/div[2]/div[1]/div/div[1]/div/div/div/form/div[2]/input"
        xpath_btn  = "/html/body/div/div[2]/div[1]/div/div[1]/div/div/div/form/div[3]/div[1]/button"

        wait.until(EC.presence_of_element_located((By.XPATH, xpath_user))).send_keys(STUDENT_ID)
        driver.find_element(By.XPATH, xpath_pass).send_keys(STUDENT_PW)
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpath_btn))
        
        # 跳轉至成績頁
        wait.until(EC.url_contains("#/ann"))
        driver.get("https://itouch.cycu.edu.tw/home/?p=8672#/includeProc/id=20HS0003&f=3&p=520074")
        
        time.sleep(5)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "includeFrame")))
        content = driver.find_element(By.TAG_NAME, "body").text
        
        # 解析邏輯 (與之前相同)
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        grade_list, graded_count = [], 0
        for i in range(len(lines)):
            if lines[i] == "1142" and i + 8 < len(lines):
                subject = lines[i+4]
                if "Rank" in subject or "排名" in subject: continue
                val8, val9 = lines[i+8], (lines[i+9] if i+9 < len(lines) else "")
                if val8.isdigit() and val9.isdigit() and val9 != "1141":
                    score, graded_count = val8, graded_count + 1
                else: score = "尚未出分"
                grade_list.append(f"• {subject} -> {score}")

        # 比對紀錄
        record_file = "graded_count.txt"
        old_count = 0
        if os.path.exists(record_file):
            with open(record_file, "r") as f:
                old_count = int(f.read().strip())

        if graded_count > old_count:
            send_grade_email(grade_list, graded_count)
            with open(record_file, "w") as f:
                f.write(str(graded_count))
        else:
            print(f"目前已有 {graded_count} 科出分，與上次相同。")

    except Exception as e:
        print(f"❌ 錯誤：{e}")
    finally:
        driver.quit()

if __name__ == "__main__":

    run_grade_check()
