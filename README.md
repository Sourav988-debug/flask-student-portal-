# Flask Student Portal

A full-stack web application for student authentication and academic record management, built with Python Flask and SQLite.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Live Demo

https://flask-student-portal.onrender.com

## Features

- User registration and login with session management
- Duplicate email prevention on signup
- Profile management — update name, phone, department, semester
- Password reset functionality
- Read-only academic grades viewer
- Responsive UI using Bootstrap 5 and custom CSS
- Secure session handling

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Database | SQLite (zero config) |
| Frontend | HTML5, Bootstrap 5, CSS3 |
| Hosting | Render (free tier) |

## Project Structure
`
flask-student-portal/
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment config
├── .env.example         # Environment variable template
├── README.md
├── LICENSE
├── templates/
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   └── grades.html
└── static/
    └── style.css
`

## Local Setup

1. Clone the repository
`ash
   git clone https://github.com/Sourav988-debug/flask-student-portal-.git
   cd flask-student-portal-
`

2. Install dependencies
`ash
   pip install -r requirements.txt
`

3. Run the app
`ash
   python app.py
`

4. Open http://127.0.0.1:5000

## Deployment

Deployed on Render — auto-deploys on every git push to main.

## Author

Sourav — [GitHub](https://github.com/Sourav988-debug)

## License

MIT License — see LICENSE
