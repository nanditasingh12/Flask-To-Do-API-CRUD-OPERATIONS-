**Features**

Create, read, update, and delete tasks
Mark tasks as completed / not completed
Search tasks by title or description
Filter tasks by completion status
SQLite database (todo.db) included


**Tech Stack**

Flask – Python web framework
Flask-SQLAlchemy – ORM for database
Flask-CORS – Handle cross-origin requests
SQLite – Lightweight database

**Project Structure**

.
├── app.py        # Main Flask application
├── todo.db       # SQLite database (auto-created if missing)
├── venv/         # Virtual environment (not included in repo)
└── README.md     # Project documentation

**Setup Instructions**

1️⃣ Clone the repository
git clone "https://github.com/nanditasingh12/Flask-To-Do-API-CRUD-OPERATIONS-.git"
cd flask-todo-api

2️⃣ Create and activate virtual environment

Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1


Linux / Mac:
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install flask flask_sqlalchemy flask_cors

4️⃣ Run the app
python app.py


App will run at 👉 http://127.0.0.1:5000 (You can use postman to test API's)

📌 API Endpoints
🔹 Health Check

GET /health

{"status": "ok"}

<img width="1364" height="268" alt="image" src="https://github.com/user-attachments/assets/307cf57a-49a4-4d37-98cb-a2bfc954be01" />


🔹 Create Task

POST /tasks

<img width="1381" height="476" alt="image" src="https://github.com/user-attachments/assets/9323fa13-4851-4a40-9e21-04615d581f67" />


🔹 Get Single Task

GET /tasks/<id>

<img width="1415" height="666" alt="image" src="https://github.com/user-attachments/assets/2dcf3312-f171-448d-90a8-a41eeb8d43fa" />

<img width="542" height="318" alt="image" src="https://github.com/user-attachments/assets/902cac0c-4afd-4f22-b2c3-f3b70b33aad7" />



DELETE /tasks/<id>

🧪 Testing with Curl

Create a task:

curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Test Task\"}"


Get all tasks:

curl http://127.0.0.1:5000/tasks

**Database:**

<img width="1919" height="1018" alt="image" src="https://github.com/user-attachments/assets/ae73f961-f6a1-4197-a111-9753a90cff61" />
