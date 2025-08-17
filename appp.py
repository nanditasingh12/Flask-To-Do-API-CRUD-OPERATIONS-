import os
from datetime import datetime
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# -----------------------------------------------------------------------------
# App & DB config
# -----------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "todo.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -----------------------------------------------------------------------------
# Database model
# -----------------------------------------------------------------------------
class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    completed = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.String(25), nullable=True)  # ISO date string like "2025-08-15"
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date,
            "created_at": self.created_at.isoformat() + "Z",
            "updated_at": self.updated_at.isoformat() + "Z",
        }

with app.app_context():
    db.create_all()

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def validate_task_payload(data, partial=False):
    if not data:
        abort(400, description="JSON body required.")
    if not partial and "title" not in data:
        abort(400, description="Field 'title' is required.")
    if "title" in data and (not isinstance(data["title"], str) or not data["title"].strip()):
        abort(400, description="Field 'title' must be a non-empty string.")
    if "completed" in data and not isinstance(data["completed"], bool):
        abort(400, description="Field 'completed' must be boolean (true/false).")

# -----------------------------------------------------------------------------
# Routes (CRUD)
# -----------------------------------------------------------------------------

# Create task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)
    validate_task_payload(data)

    task = Task(
        title=data["title"].strip(),
        description=data.get("description", "").strip(),
        completed=bool(data.get("completed", False)),
        due_date=data.get("due_date"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# Get tasks (with optional filters & pagination)
@app.route("/tasks", methods=["GET"])
def list_tasks():
    # Filters: ?completed=true|false  ?q=search  ?page=1&limit=10
    q = Task.query
    completed = request.args.get("completed")
    if completed is not None:
        if completed.lower() not in {"true", "false"}:
            abort(400, description="completed must be true or false")
        q = q.filter(Task.completed == (completed.lower() == "true"))

    search = request.args.get("q")
    if search:
        like = f"%{search}%"
        q = q.filter(db.or_(Task.title.ilike(like), Task.description.ilike(like)))

    # Pagination
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        abort(400, description="page and limit must be integers")

    items = q.order_by(Task.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)
    return jsonify({
        "page": page,
        "limit": limit,
        "total": items.total,
        "tasks": [t.to_dict() for t in items.items],
    }), 200

# Get single task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

# Update task (full update with PUT, partial with PATCH)
@app.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True)
    validate_task_payload(data, partial=(request.method == "PATCH"))

    if "title" in data:
        task.title = data["title"].strip()
    if "description" in data:
        task.description = data.get("description", "").strip()
    if "completed" in data:
        task.completed = bool(data["completed"])
    if "due_date" in data:
        task.due_date = data["due_date"]

    db.session.commit()
    return jsonify(task.to_dict()), 200

# Delete task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)