import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# ---------------- CONFIG ----------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "employees.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{db_path}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

# -------- CREATE TABLES ON STARTUP ------
with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@app.route("/add", methods=["POST"])
def add_employee():
    emp = Employee(
        name=request.form["name"],
        email=request.form["email"],
        salary=request.form["salary"]
    )
    db.session.add(emp)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_employee(id):
    emp = Employee.query.get_or_404(id)

    if request.method == "POST":
        emp.name = request.form["name"]
        emp.email = request.form["email"]
        emp.salary = request.form["salary"]
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("update.html", employee=emp)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
