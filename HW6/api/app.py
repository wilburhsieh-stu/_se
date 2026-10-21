from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    # 透過環境變數取得連線資訊 (由 docker-compose.yml 提供)
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'microdb'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASS', 'secretpassword')
    )
    return conn

@app.route('/api/status')
def status():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "API 與 PostgreSQL 資料庫連線成功！",
            "database_version": db_version
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"資料庫連線失敗: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
