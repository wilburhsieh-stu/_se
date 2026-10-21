import argparse
import requests
import sys

def main():
    # 設定命令列參數解析
    parser = argparse.ArgumentParser(description="一個類似 curl 的 Python HTTP 客戶端工具")
    parser.add_argument("url", help="目標 URL")
    parser.add_argument("-X", "--request", default="GET", help="指定 HTTP 請求方法，例如 GET, POST, PUT, DELETE (預設: GET)")
    parser.add_argument("-d", "--data", help="要傳送的 HTTP 數據 (Data)")
    parser.add_argument("-H", "--header", action="append", help="自訂 HTTP 標頭 (可多次使用，例如: -H 'Content-Type: application/json')")
    parser.add_argument("-i", "--include", action="store_true", help="在輸出結果中包含 HTTP 回應標頭")

    args = parser.parse_args()

    # 處理自訂標頭
    headers = {}
    if args.header:
        for h in args.header:
            if ":" in h:
                key, value = h.split(":", 1)
                headers[key.strip()] = value.strip()
            else:
                print(f"警告: 無效的標頭格式 '{h}'，請使用 'Key: Value' 格式。")

    try:
        # 發送 HTTP 請求
        response = requests.request(
            method=args.request.upper(),
            url=args.url,
            data=args.data,
            headers=headers
        )

        # 輸出回應標頭 (如果加上了 -i 參數)
        if args.include:
            print(f"HTTP {response.status_code} {response.reason}")
            for key, value in response.headers.items():
                print(f"{key}: {value}")
            print() # 印出空行以分隔標頭與內容

        # 輸出回應主體內容
        print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"請求發生錯誤: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
