# Flask Student Portal

A full-stack web application for student authentication and academic record management, built with Python Flask and MySQL.

## Features

- User registration and login with session management
- Duplicate email prevention on signup
- Profile management — update name, phone, department, semester
- Password reset functionality
- Read-only academic grades viewer
- Responsive UI using Bootstrap 5 and custom CSS
- Secure session handling with Flask sessions

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | MySQL |
| Frontend | HTML5, Bootstrap 5, CSS3 |
| Auth | Flask Sessions |

## Project Structure
```
flask-student-portal/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── templates/          # HTML pages
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   └── grades.html
└── static/
    └── style.css       # Custom styles
```

## Setup (Local)

1. Clone the repository
```bash
   git clone https://github.com/YOUR_USERNAME/flask-student-portal.git
   cd flask-student-portal
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create a .env file from the template
```bash
   cp .env.example .env
```
   Edit .env with your MySQL credentials.

4. Set up the database
```sql
   CREATE DATABASE flask_lab4;
   USE flask_lab4;
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       email VARCHAR(100) UNIQUE,
       password VARCHAR(255),
       phone VARCHAR(15),
       department VARCHAR(50),
       semester VARCHAR(10)
   );
   CREATE TABLE grades (
       user_id INT,
       subject VARCHAR(50),
       marks INT,
       FOREIGN KEY (user_id) REFERENCES users(id)
   );
```

5. Run the app
```bash
   python app.py
```
   Open http://127.0.0.1:5000

## Live Demo

[View deployed app](https://YOUR_USERNAME.pythonanywhere.com)

## Author

Your Name — [GitHub](https://github.com/YOUR_USERNAME)

## License

MIT License — see [LICENSE](LICENSE)
