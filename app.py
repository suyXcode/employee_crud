import email
from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

# head + read employees
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


# create employee
@app.route('/add', methods=['POST'])
def add_employee():
    emp = Employee(
        name = request.form['name'],
        email = request.form['email'],
        salary = request.form['salary']
    )
    db.session.add(emp)
    
    db.session.commit()
    return redirect(url_for('index'))


# delete employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('index'))

# update employee
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    emp = Employee.query.get(id)
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.email = request.form['email']
        emp.salary = request.form['salary']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', employee=emp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)