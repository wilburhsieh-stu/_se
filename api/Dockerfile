FROM python:3.9-slim

WORKDIR /app

# 複製依賴清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式程式碼
COPY . .

# 曝露 5000 端口
EXPOSE 5000

# 啟動 Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
