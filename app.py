import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, g
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret123')

DATABASE = os.path.join(os.path.dirname(__file__), 'flask_portal.db')

# ---------------- DATABASE HELPERS ----------------
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT,
            email    TEXT UNIQUE,
            password TEXT,
            phone    TEXT,
            department TEXT,
            semester TEXT
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            user_id INTEGER,
            subject TEXT,
            marks   INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    db.commit()
    db.close()

# Create tables automatically on startup
with app.app_context():
    init_db()

# ---------------- SIGNUP ----------------
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name       = request.form['name']
        email      = request.form['email']
        phone      = request.form['phone']
        department = request.form['department']
        semester   = request.form['semester']
        password   = request.form['password']

        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE email=?", (email,)
        ).fetchone()

        if existing:
            return render_template('signup.html', error="Email already registered. Please login.")

        db.execute(
            "INSERT INTO users (name,email,phone,department,semester,password) VALUES (?,?,?,?,?,?)",
            (name, email, phone, department, semester, password)
        )
        db.commit()
        return redirect('/login')

    return render_template('signup.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        db   = get_db()
        user = db.execute(
            "SELECT id FROM users WHERE email=? AND password=?", (email, password)
        ).fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")

    return render_template('login.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    db   = get_db()
    user = db.execute(
        "SELECT name, email, phone, department, semester FROM users WHERE id=?",
        (session['user_id'],)
    ).fetchone()

    return render_template('dashboard.html', user=user)

# ---------------- PROFILE ----------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name       = request.form['name']
        phone      = request.form['phone']
        department = request.form['department']
        semester   = request.form['semester']
        password   = request.form['password']

        db = get_db()
        db.execute(
            "UPDATE users SET name=?,phone=?,department=?,semester=?,password=? WHERE id=?",
            (name, phone, department, semester, password, session['user_id'])
        )
        db.commit()
        return redirect('/dashboard')

    return render_template('profile.html')

# ---------------- GRADES ----------------
@app.route('/grades')
def grades():
    if 'user_id' not in session:
        return redirect('/login')

    db         = get_db()
    grade_data = db.execute(
        "SELECT subject, marks FROM grades WHERE user_id=?",
        (session['user_id'],)
    ).fetchall()

    return render_template('grades.html', grades=grade_data)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=False)