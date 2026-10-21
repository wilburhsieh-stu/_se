# Docker 學習紀錄與微服務架構實作

本專案記錄了 Docker 的基礎使用方式，並實作了一個包含 Nginx、Python API 與 PostgreSQL 的簡易微服務系統。

## 第一部分：Docker 學習紀錄

### 1. Docker 核心概念
* **Image (映像檔)**：一個唯讀的模板，包含了執行環境、程式碼與依賴套件（類似系統安裝光碟）。
* **Container (容器)**：從 Image 建立出來的執行實體，各自獨立運作（類似裝好系統的虛擬機，但更輕量）。
* **Dockerfile**：用來定義如何打包自訂 Image 的腳本檔案。
* **Docker Compose**：透過 `docker-compose.yml` 檔案，一次定義並啟動多個互相關聯的 Container（微服務架構必備）。

### 2. 常用 Docker 指令
* `docker pull <image>`：從 Docker Hub 下載映像檔。
* `docker ps`：查看正在執行的容器。
* `docker build -t <name> .`：根據當前目錄的 Dockerfile 建立映像檔。
* `docker run -d -p 80:80 <image>`：在背景執行容器，並將本機的 80 port 映射到容器的 80 port。
* `docker rm -f <container_id>`：強制刪除容器。

### 3. Docker Compose 指令
* `docker-compose up -d`：背景啟動所有定義在 YAML 中的服務。
* `docker-compose down`：停止並刪除所有由 Compose 啟動的服務與網路。
* `docker-compose logs -f`：持續查看所有服務的輸出日誌。

---

## 第二部分：微服務系統架構

本系統展示了一個典型的三層式微服務架構：
1. **web (Nginx)**：作為 Web Server 提供靜態 HTML 介面，同時作為 Reverse Proxy，將 `/api` 開頭的請求轉發給後端。
2. **api (Python/Flask)**：後端應用程式，負責處理商業邏輯並連接資料庫。
3. **db (PostgreSQL)**：關聯式資料庫，用於儲存系統資料。

### 專案目錄結構建議
請在你的電腦上建立一個資料夾，並依照以下結構放置檔案：
```text
docker-demo/
├── README.md
├── docker-compose.yml
├── html/
│   └── index.html         (前端網頁)
├── nginx/
│   └── default.conf       (Nginx 設定檔)
└── api/
    ├── Dockerfile         (Python 環境建置)
    ├── requirements.txt   (Python 套件依賴)
    └── app.py             (Python API 程式碼)
```

### 啟動教學
1. 確保已安裝 Docker 與 Docker Compose。
2. 在終端機進入 `docker-demo` 資料夾。
3. 執行指令：`docker-compose up -d --build`
4. 打開瀏覽器，前往 `http://localhost` 即可看到展示介面，並能測試前後端與資料庫的連線狀態！
