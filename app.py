
import os, csv, io
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from werkzeug.security import check_password_hash
import psycopg

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
ADMIN_PASSWORD_HASH = os.environ["ADMIN_PASSWORD_HASH"]

def db():
    return psycopg.connect(DATABASE_URL)

def init_db():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    student_name TEXT NOT NULL,
                    major TEXT NOT NULL,
                    phone_last4 TEXT NOT NULL,
                    lineup_number TEXT NOT NULL,
                    lineup_location TEXT,
                    rehearsal_time TEXT,
                    notes TEXT
                )
            """)
        conn.commit()

def admin_required(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return inner

@app.before_request
def ensure_db():
    init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        student_id = request.form.get("student_id","").strip()
        phone_last4 = request.form.get("phone_last4","").strip()
        if not student_id or not phone_last4:
            error = "يرجى إدخال الرقم الجامعي وآخر 4 أرقام من رقم الهاتف."
        else:
            with db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT student_name, major, lineup_number,
                               COALESCE(lineup_location,''), COALESCE(rehearsal_time,''), COALESCE(notes,'')
                        FROM students
                        WHERE student_id=%s AND phone_last4=%s
                    """, (student_id, phone_last4))
                    row = cur.fetchone()
            if row:
                result = {
                    "student_name": row[0], "major": row[1], "lineup_number": row[2],
                    "lineup_location": row[3], "rehearsal_time": row[4], "notes": row[5]
                }
            else:
                error = "لم يتم العثور على بيانات مطابقة. يرجى التأكد من البيانات المدخلة."
    return render_template("index.html", result=result, error=error)

@app.route("/health")
def health():
    return {"status":"ok"}, 200

@app.route("/admin", methods=["GET","POST"])
def admin_login():
    if session.get("admin"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        password = request.form.get("password","")
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("كلمة المرور غير صحيحة.", "error")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM students")
            count = cur.fetchone()[0]
            cur.execute("SELECT student_id, student_name, major, lineup_number FROM students ORDER BY student_id LIMIT 100")
            rows = cur.fetchall()
    return render_template("admin_dashboard.html", count=count, rows=rows)

@app.route("/admin/upload", methods=["POST"])
@admin_required
def admin_upload():
    f = request.files.get("file")
    if not f or not f.filename:
        flash("يرجى اختيار ملف CSV.", "error")
        return redirect(url_for("admin_dashboard"))
    try:
        content = f.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content))
        required = {"student_id","student_name","major","phone_last4","lineup_number"}
        headers = set(reader.fieldnames or [])
        if not required.issubset(headers):
            flash("الملف لا يحتوي جميع الأعمدة المطلوبة.", "error")
            return redirect(url_for("admin_dashboard"))

        records = []
        for r in reader:
            sid = (r.get("student_id") or "").strip()
            if not sid:
                continue
            records.append((
                sid,
                (r.get("student_name") or "").strip(),
                (r.get("major") or "").strip(),
                (r.get("phone_last4") or "").strip(),
                (r.get("lineup_number") or "").strip(),
                (r.get("lineup_location") or "").strip(),
                (r.get("rehearsal_time") or "").strip(),
                (r.get("notes") or "").strip()
            ))

        with db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM students")
                cur.executemany("""
                    INSERT INTO students
                    (student_id,student_name,major,phone_last4,lineup_number,lineup_location,rehearsal_time,notes)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, records)
            conn.commit()
        flash(f"تم تحميل {len(records)} طالبًا بنجاح.", "success")
    except Exception as e:
        flash(f"تعذر قراءة الملف: {e}", "error")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/sample")
@admin_required
def sample():
    csv_text = """student_id,student_name,major,phone_last4,lineup_number,lineup_location,rehearsal_time,notes
202012345,طالب تجريبي,المحاسبة,6789,145,القاعة الرئيسية,10:00 صباحاً,الحضور قبل الموعد بـ 30 دقيقة
"""
    return Response(csv_text, mimetype="text/csv",
                    headers={"Content-Disposition":"attachment; filename=sample_students.csv"})

@app.route("/admin/logout")
@admin_required
def logout():
    session.clear()
    return redirect(url_for("admin_login"))
