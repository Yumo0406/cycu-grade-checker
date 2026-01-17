# cycu-grade-checker
# 🎓 中原大學 iTouch 成績自動追蹤機器人 (CYCU Grade Checker)

這是一個專為中原大學 iTouch 系統設計的成績追蹤工具。它會自動巡邏成績頁面，並在老師送出新成績時發送 Email 通知。 (｡･ω･｡)ﾉ

## ✨ 功能特色
* **自動巡邏**：每小時自動登入 iTouch 檢查最新成績。
* **精準通知**：只有當「已出分科目數」增加時才會發信，不重複吵人。
* **隱私保護**：帳號密碼與 Email 密鑰皆儲存於 GitHub Secrets，安全不外洩。
* **簡單易用**：完全在雲端運行，不需開啟電腦。

## 🛠️ 技術架構
* **語言**：Python 3.9
* **自動化工具**：Selenium + Chrome WebDriver
* **執行環境**：GitHub Actions
* **通知系統**：Gmail SMTP (smtplib)

## 📝 專案結構
* `grade.py`: 核心爬蟲腳本，負責登入、解析成績及比對邏輯。
* `.github/workflows/main.yml`: 自動化排程設定。
* `graded_count.txt`: 紀錄上次已出分的科目數量，用於比對更新。

## 🤖 維護者
* **Feng, Ying-chen**

---
希望每學期都能順利 Pass！加油加油！ (๑•̀ㅂ•́)و✧
