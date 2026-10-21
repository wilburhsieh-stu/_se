from flask import Flask, request, render_template_string, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # 用於顯示 flash 提示訊息

# ================= 核心邏輯 (與先前類似，但改用實體資料庫檔案) =================
class SchoolSystem:
    def __init__(self, db_name="nqu_system.db"):
        self.db_name = db_name
        self.setup_database()

    def get_conn(self):
        # 讓 SQLite 支援資料列以字典形式操作
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row 
        return conn

    def setup_database(self):
        with self.get_conn() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS Students (student_id TEXT PRIMARY KEY, name TEXT, department TEXT);
                CREATE TABLE IF NOT EXISTS Courses (course_id TEXT PRIMARY KEY, name TEXT, credits INTEGER, capacity INTEGER, enrolled INTEGER DEFAULT 0);
                CREATE TABLE IF NOT EXISTS Enrollments (
                    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT, course_id TEXT,
                    UNIQUE(student_id, course_id)
                );
            ''')

    def add_student(self, student_id, name, department):
        try:
            with self.get_conn() as conn:
                conn.execute("INSERT INTO Students (student_id, name, department) VALUES (?, ?, ?)", (student_id, name, department))
            return True, f"學生 {name} 新增成功！"
        except sqlite3.IntegrityError:
            return False, "學號已存在！"

    def add_course(self, course_id, name, credits, capacity):
        try:
            with self.get_conn() as conn:
                conn.execute("INSERT INTO Courses (course_id, name, credits, capacity) VALUES (?, ?, ?, ?)", (course_id, name, credits, capacity))
            return True, f"課程 {name} 新增成功！"
        except sqlite3.IntegrityError:
            return False, "課程代碼已存在！"

    def enroll_course(self, student_id, course_id):
        with self.get_conn() as conn:
            course = conn.execute("SELECT capacity, enrolled FROM Courses WHERE course_id = ?", (course_id,)).fetchone()
            if not course: return False, "找不到該課程。"
            if course['enrolled'] >= course['capacity']: return False, "課程已額滿！"
            
            try:
                conn.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
                conn.execute("UPDATE Courses SET enrolled = enrolled + 1 WHERE course_id = ?", (course_id,))
                return True, "選課成功！"
            except sqlite3.IntegrityError:
                return False, "你已經選過這門課了！"

    def get_all(self, table):
        with self.get_conn() as conn:
            return conn.execute(f"SELECT * FROM {table}").fetchall()

system = SchoolSystem()

# ================= HTML 網頁介面 (直接寫入字串方便單檔執行) =================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>金大校務系統原型</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
        .container { display: flex; gap: 20px; }
        .box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); flex: 1; }
        h2 { color: #333; }
        input, button { padding: 8px; margin: 5px 0; width: 90%; }
        button { background: #0056b3; color: white; border: none; cursor: pointer; }
        button:hover { background: #004494; }
        .alert { background: #ffe4e1; padding: 10px; color: #a94442; border: 1px solid #ebccd1; margin-bottom: 15px;}
        .success { background: #dff0d8; color: #3c763d; border-color: #d6e9c6; }
    </style>
</head>
<body>
    <h1>🎓 大學校務系統 Web 版</h1>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert {% if category == 'success' %}success{% endif %}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <div class="container">
        <!-- 學生管理 -->
        <div class="box">
            <h2>👤 新增學生</h2>
            <form action="/add_student" method="post">
                <input type="text" name="student_id" placeholder="學號 (例: 11201)" required><br>
                <input type="text" name="name" placeholder="姓名" required><br>
                <input type="text" name="department" placeholder="科系" required><br>
                <button type="submit">註冊學生</button>
            </form>
            <hr>
            <h3>學生列表</h3>
            <ul>
                {% for s in students %}<li>{{ s.student_id }} - {{ s.name }} ({{ s.department }})</li>{% endfor %}
            </ul>
        </div>

        <!-- 課程管理 -->
        <div class="box">
            <h2>📚 新增課程</h2>
            <form action="/add_course" method="post">
                <input type="text" name="course_id" placeholder="課程代碼 (例: CS101)" required><br>
                <input type="text" name="name" placeholder="課程名稱" required><br>
                <input type="number" name="credits" placeholder="學分數" required><br>
                <input type="number" name="capacity" placeholder="人數上限" required><br>
                <button type="submit">開設課程</button>
            </form>
            <hr>
            <h3>課程列表 (已選/上限)</h3>
            <ul>
                {% for c in courses %}<li>{{ c.course_id }} - {{ c.name }} ({{ c.enrolled }}/{{ c.capacity }})</li>{% endfor %}
            </ul>
        </div>

        <!-- 選課操作 -->
        <div class="box">
            <h2>✅ 學生選課</h2>
            <form action="/enroll" method="post">
                <input type="text" name="student_id" placeholder="輸入你的學號" required><br>
                <input type="text" name="course_id" placeholder="輸入你想選的課程代碼" required><br>
                <button type="submit">送出選課</button>
            </form>
            <hr>
            <h3>最新選課紀錄</h3>
            <ul>
                {% for e in enrollments %}<li>學生 {{ e.student_id }} 選了 課程 {{ e.course_id }}</li>{% endfor %}
            </ul>
        </div>
    </div>
</body>
</html>
'''

# ================= Flask 路由與 API =================
@app.route('/')
def index():
    students = system.get_all("Students")
    courses = system.get_all("Courses")
    enrollments = system.get_all("Enrollments")
    return render_template_string(HTML_TEMPLATE, students=students, courses=courses, enrollments=enrollments)

@app.route('/add_student', methods=['POST'])
def handle_add_student():
    success, msg = system.add_student(request.form['student_id'], request.form['name'], request.form['department'])
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('index'))

@app.route('/add_course', methods=['POST'])
def handle_add_course():
    success, msg = system.add_course(request.form['course_id'], request.form['name'], int(request.form['credits']), int(request.form['capacity']))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('index'))

@app.route('/enroll', methods=['POST'])
def handle_enroll():
    success, msg = system.enroll_course(request.form['student_id'], request.form['course_id'])
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("啟動伺服器... 請打開瀏覽器輸入 http://127.0.0.1:5000")
    app.run(debug=True)
