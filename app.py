import os
from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret')

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'flask_lab4')

mysql = MySQL(app)

# ---------------- SIGNUP ----------------
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        semester = request.form['semester']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing = cur.fetchone()

        if existing:
            cur.close()
            return render_template('signup.html', error="Email already registered. Please login.")

        cur.execute(
            "INSERT INTO users (name, email, phone, department, semester, password) VALUES (%s,%s,%s,%s,%s,%s)",
            (name, email, phone, department, semester, password)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/login')

    return render_template('signup.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT name, email, phone, department, semester FROM users WHERE id=%s",
        (session['user_id'],)
    )
    user = cur.fetchone()
    cur.close()
    return render_template('dashboard.html', user=user)


# ---------------- PROFILE ----------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        department = request.form['department']
        semester = request.form['semester']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE users SET name=%s, phone=%s, department=%s, semester=%s, password=%s WHERE id=%s",
            (name, phone, department, semester, password, session['user_id'])
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/dashboard')

    return render_template('profile.html')


# ---------------- GRADES ----------------
@app.route('/grades')
def grades():
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute("SELECT subject, marks FROM grades WHERE user_id=%s", (session['user_id'],))
    grade_data = cur.fetchall()
    cur.close()
    return render_template('grades.html', grades=grade_data)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=False)