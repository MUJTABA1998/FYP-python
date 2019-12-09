from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, LoginManager
import os, random, datetime
app = Flask(__name__)
LoginManager(app)


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, 'database.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False, unique=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    program = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=True)


class Teacher(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False, unique=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    program = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=True)


class Admin(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False, unique=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)


db.create_all()
db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('member-login.html')


@app.route('/admin')
def admin():
    return render_template('admin-login.html')


@app.route('/admin-login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        name = request.form['name']
        students = Student.query.all()
        teachers = Teacher.query.all()
        admins = Admin.query.all()
        password = request.form['password']
        valid = Admin.query.filter_by(name=name, password=password).first()
        if (name == "admin" and password == "admin") or valid:
            return render_template('dashboard-admin.html', name=name, teachers=teachers, students=students,
                                   admins=admins)
        else:
            msg_type = "alert alert-danger"
            msg = "Invalid information"
            return render_template('admin-login.html', type=msg_type, msg=msg)
    return render_template('index.html')


@app.route('/add-member', methods=['POST', 'GET'])
def add_member():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = random.randint(10000111, 23456789)
        program = request.form['programm']
        typ = request.form['type']
        date = datetime.datetime.now()
        if typ == "teacher":
            valid = Teacher.query.filter_by(email=email).first()
            if valid:
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-danger"
                msg = "Email already exit"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       teachers=teachers, admins=admins)
            else:
                teacher = Teacher()
                teacher.email = email
                teacher.name = name
                teacher.program = program
                teacher.password = password
                teacher.date = date
                db.session.add(teacher)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-success"
                msg = "Member added"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       teachers=teachers, admins=admins)
        elif typ == "student":
            valid = Student.query.filter_by(email=email).first()
            if valid:
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-danger"
                msg = "Email already exit"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       teachers=teachers, admins=admins)
            else:
                student = Student()
                student.email = email
                student.password = password
                student.date = date
                student.name = name
                student.program = program
                db.session.add(student)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-success"
                msg = "Member added"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       admins=admins, teachers=teachers)
        else:
            return render_template('dashboard-admin.html')
    return render_template('admin-login.html')


@app.route('/remove-member', methods=['POST', 'GET'])
def remove_member():
    if request.method == 'POST':
        email = request.form['email']
        typ = request.form['type']
        name = request.form['name']
        if typ == "teacher":
            valid = Teacher.query.filter_by(email=email, name=name).first()
            if valid:
                db.session.delete(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-success"
                msg = "Member removed"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       teachers=teachers, admins=admins)
            else:
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-info"
                msg = "Invalid information"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       teachers=teachers, admins=admins)
        elif typ == "student":
            valid = Student.query.filter_by(email=email, name=name).first()
            if valid:
                db.session.delete(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-success"
                msg = "Member removed"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       teachers=teachers, admins=admins)
            else:
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-info"
                msg = "Invlid information"
                return render_template('dashboard-admin.html', type=msg_type, msg=msg, students=students,
                                       teachers=teachers, admins=admins)
        return render_template('dashboard-admin.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return render_template('admin-login.html')


@app.route('/logout-member', methods=['POST', 'GET'])
def logout_member():
    logout_user()
    return render_template('member-login.html')


@app.route('/update-member', methods=['POST', 'GET'])
def to_update():
    if request.method == 'POST':
        email = request.form['email']
        member = request.form['type']
        new_email = request.form['new-email']
        new_name = request.form['new-name']
        new_password = request.form['new-password']
        if member == "teacher":
            valid = Teacher.query.filter_by(email=email).first()
            if valid:
                valid.email = new_email
                valid.name = new_name
                valid.password = new_password
                db.session.add(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-success"
                msg = "Member updated successfully"
                return render_template('dashboard-admin.html', students=students, teachers=teachers, type=msg_type,
                                       msg=msg, admins=admins)
            if not valid:
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-info"
                msg = "Email not exited"
                return render_template('dashboard-admin.html', students=students, teachers=teachers, type=msg_type,
                                       msg=msg, admins=admins)
        if member == "student":
            valid = Student.query.filter_by(email=email).first()
            if valid:
                valid.email = new_email
                valid.name = new_name
                valid.password = new_password
                db.session.add(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-success"
                msg = "Member updated successfully"
                return render_template('dashboard-admin.html', students=students, teachers=teachers, type=msg_type,
                                msg=msg, admins=admins)
            if not valid:
                students = Student.query.all()
                teachers = Teacher.query.all()
                admins = Admin.query.all()
                msg_type = "alert alert-info"
                msg = "Email not exited"
                return render_template('dashboard-admin.html', students=students, teachers=teachers, type=msg_type,
                        msg=msg, admins=admins)
    admins = Admin.query.all()
    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template('dashboard-admin.html', students=students, teachers=teachers, admins=admins)


@app.route('/add-admin', methods=['POST', 'GET'])
def add_admin():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        valid = Admin.query.filter_by(email=email).first()
        if valid:
            students = Student.query.all()
            teachers = Teacher.query.all()
            admins = Admin.query.all()
            msg_type = "alert alert-danger"
            msg = "Admin already exit"
            return render_template('dashboard-admin.html', students=students, admins=admins, teachers=teachers,
                                   type=msg_type, msg=msg)
        if not valid:
            admin1 = Admin(
                email=email,
                password=password,
                name=name
            )
            db.session.add(admin1)
            db.session.commit()
            students = Student.query.all()
            admins = Admin.query.all()
            teachers = Teacher.query.all()
            msg_type = "alert alert-success"
            msg = "Admin successfully added"
            return render_template('dashboard-admin.html', students=students, admins=admins, teachers=teachers,
                                   type=msg_type, msg=msg)
    students = Student.query.all()
    admins = Admin.query.all()
    teachers = Teacher.query.all()
    return render_template('dashboard-admin.html', students=students, admins=admins, teachers=teachers)


@app.route('/update-admin', methods=['POST', 'GET'])
def update_admin():
    if request.method == 'POST':
        email = request.form['email']
        new_email = request.form['new-email']
        new_name = request.form['new-name']
        new_password = request.form['new-password']
        valid = Admin.query.filter_by(email=email).first()
        if valid:
            valid.email = new_email
            valid.name = new_name
            valid.password = new_password
            db.session.add(valid)
            db.session.commit()
            students = Student.query.all()
            teachers = Teacher.query.all()
            admins = Admin.query.all()
            msg_type = "alert alert-success"
            msg = "Admin updated successfully"
            return render_template('dashboard-admin.html', students=students, teachers=teachers, type=msg_type,
                                   msg=msg, admins=admins)
        if not valid:
            students = Student.query.all()
            teachers = Teacher.query.all()
            admins = Admin.query.all()
            msg_type = "alert alert-info"
            msg = "Email not exited"
            return render_template('dashboard-admin.html', students=students, teachers=teachers, type=msg_type,
                                   msg=msg, admins=admins)
    students = Student.query.all()
    teachers = Teacher.query.all()
    admins = Admin.query.all()
    return render_template('dashboard-admin.html', students=students, teachers=teachers, admins=admins)


@app.route('/member-login', methods=['POST', 'GET'])
def member_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        member = request.form['type']
        if member == "teacher":
            valid = Teacher.query.filter_by(email=email,password=password).first()
            if valid:
                name = valid.name
                password = valid.password
                join_date = valid.date
                program = valid.program
                email = valid.email
                date = datetime.datetime.now()
                return render_template('member-info.html', name=name, password=password, join_date=join_date,
                                       program=program, date=date, email=email, member=member)
            if not valid:
                msg_type = "alert alert-danger"
                msg = "Member not exited"
                return render_template('member-login.html', type=msg_type, msg=msg)
        if member == "student":
            valid = Student.query.filter_by(email=email,password=password).first()
            if valid:
                name = valid.name
                password = valid.password
                join_date = valid.date
                program = valid.program
                email = valid.email
                date = datetime.datetime.now()
                return render_template('member-info.html',email=email, name=name, password=password, join_date=join_date,
                                       program=program, date=date, member=member)
            if not valid:
                msg_type = "alert alert-danger"
                msg = "Member not exited"
                return render_template('member-login.html', type=msg_type, msg=msg)
    return render_template('member-login.html')


@app.route('/change-member-email', methods=['POST', 'GET'])
def update_email():
    if request.method == 'POST':
        email = request.form['email']
        member = request.form['type']
        new_email = request.form['new-email']
        if member == "teacher":
            valid = Teacher.query.filter_by(email=email).first()
            if valid:
                valid.email = new_email
                db.session.add(valid)
                db.session.commit()
                msg_type = "alert alert-success"
                msg = "Email successfully changed"
                return render_template('member-login.html', type=msg_type, msg=msg)
        if member == "student":
            valid = Student.query.filter_by(email=email).first()
            if valid:
                valid.email = new_email
                db.session.add(valid)
                db.session.commit()
                msg_type = "alert alert-success"
                msg = "Email successfully changed"
                return render_template('member-login.html', type=msg_type, msg=msg)
    return render_template('member-info.html')


@app.route('/change-member-password', methods=['POST', 'GET'])
def update_password():
    if request.method == 'POST':
        email = request.form['email']
        member = request.form['type']
        password = request.form['password']
        new_password = request.form['new-password']
        if member == "teacher":
            valid = Teacher.query.filter_by(email=email, password=password).first()
            if valid:
                valid.password = new_password
                db.session.add(valid)
                db.session.commit()
                msg_type = "alert alert-success"
                msg = "Password successfully changed"
                return render_template('member-login.html', type=msg_type, msg=msg)
        if member == "student":
            valid = Student.query.filter_by(email=email, password=password).first()
            if valid:
                valid.password = new_password
                db.session.add(valid)
                db.session.commit()
                msg_type = "alert alert-success"
                msg = "Password successfully changed"
                return render_template('member-login.html', type=msg_type, msg=msg)
    return render_template('member-info.html')


if __name__ == '__main__':
    app.run(debug=True)