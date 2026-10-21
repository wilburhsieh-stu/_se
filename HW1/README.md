# MyCurl 🚀

`MyCurl` 是一個使用 Python 實作的輕量級命令列 HTTP 客戶端工具。它模仿了強大且廣受歡迎的原生 `curl` 工具的核心功能與語法，讓開發者在沒有安裝 `curl` 的環境下，也能透過 Python 快速發送 HTTP 請求、測試 API、自訂標頭與攜帶負載數據。

---

## ✨ 核心特色

- **純粹輕量**：單一腳本檔案即可運行，極簡設計。
- **高相容性**：語法高度仿照原生 `curl`，無縫接軌您的肌肉記憶。
- **支援多種 HTTP 方法**：`GET`, `POST`, `PUT`, `DELETE`, `PATCH` 等。
- **彈性數據傳輸**：支援傳送純文字、表單數據 (Form Data) 或 JSON 格式內容。
- **自訂性高**：可自由添加多個 HTTP 請求標頭 (Headers)。
- **詳細除錯資訊**：支援檢視完整的 HTTP 回應狀態碼與標頭 (`-i` 參數)。

---

## 📂 專案結構

```text
mycurl/
├── mycurl.py       # 核心主程式原始碼
├── README.md       # 專案說明文件 (本檔案)
└── requirements.txt# 專案依賴套件清單 (非必備，僅含 requests)
```

---

## 📦 安裝與環境設定

本專案依賴 Python 3.6+ 以及 `requests` 函式庫。強烈建議在虛擬環境中執行。

### 1. 取得專案碼
您可以直接下載 `mycurl.py` 檔案，或是將專案 Clone 到本地：
```bash
git clone https://github.com/yourusername/mycurl.git
cd mycurl
```

### 2. 建立並啟動虛擬環境 (推薦)
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. 安裝依賴套件
```bash
pip install requests
```

---

## 🛠️ 完整指令與參數說明

基本語法：
```bash
python mycurl.py [選項] <URL>
```

### 參數列表

| 縮寫 | 完整參數 | 預設值 | 說明 |
| :--- | :--- | :--- | :--- |
| (無) | `url` | **必填** | 目標網站或 API 的 URL (例如：`https://api.github.com`) |
| `-X` | `--request` | `GET` | 指定 HTTP 請求方法 (`GET`, `POST`, `PUT`, `DELETE`, `OPTIONS` 等) |
| `-d` | `--data` | (無) | 要傳送的 HTTP 請求主體數據 (Data) |
| `-H` | `--header` | (無) | 自訂 HTTP 標頭。支援多次使用 (格式為 `"Key: Value"`) |
| `-i` | `--include` | `False`| 在標準輸出中包含 HTTP 回應標頭 (Response Headers) 與狀態碼 |
| `-h` | `--help` | (無) | 顯示完整的幫助選單與參數說明並退出程式 |

---

## 💡 實戰範例與預期輸出

### 範例 1：最基礎的 GET 請求
獲取網頁的 HTML 或 API 的預設回應。

**指令：**
```bash
python mycurl.py https://httpbin.org/get
```

### 範例 2：檢視完整的 HTTP 標頭 (-i)
如果您想檢查伺服器回傳的 `Content-Type`、`Server` 或狀態碼，請加上 `-i`。

**指令：**
```bash
python mycurl.py -i https://httpbin.org/get
```

### 範例 3：發送 POST 請求與表單數據 (-X, -d)
模擬網頁表單送出數據。

**指令：**
```bash
python mycurl.py -X POST -d "username=admin&password=123" https://httpbin.org/post
```

### 範例 4：與 RESTful API 互動 (JSON + 自訂標頭)
現今最常見的 API 呼叫方式，自訂 `Content-Type` 並攜帶 JSON 字串。

**指令：**
```bash
python mycurl.py -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SECRET_TOKEN" \
  -d '{"title": "foo", "body": "bar", "userId": 1}' \
  https://jsonplaceholder.typicode.com/posts
```

---

## ⚠️ 常見問題與錯誤排除

1. **`ModuleNotFoundError: No module named 'requests'`**
   - **原因**：尚未安裝 requests 套件。
   - **解法**：執行 `pip install requests`。

2. **警告: 無效的標頭格式**
   - **原因**：使用了 `-H` 但格式不對（缺少冒號）。
   - **解法**：確保標頭格式為字串且包含冒號，例如 `-H "Accept: application/json"`。請注意引號的使用。

---

## 📄 授權條款 (License)

本專案採用 **MIT 授權條款** 發佈。
