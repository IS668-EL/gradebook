from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin #add current_user back in later
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#from flask_wtf import Form
#from wtforms import TextField
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="mygrade",
    password="springis668",
    hostname="mygrade.mysql.pythonanywhere-services.com",
    databasename="mygrade$teamproject2",
    #databasename="mygrade$dummyempty",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "SOMETHING RANDOM"
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Student(db.Model):

    __tablename__ = "students"

    studentid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    major = db.Column(db.String(50))
    email = db.Column(db.String(100))


    def __init__(self, firstname, lastname, major, email):
         #self.studentid = studentid
         self.firstname = firstname
         self.lastname = lastname
         self.major = major
         self.email = email

class Assignment(db.Model):

    __tablename__ = "assignments"

    assignmentid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    fullscore = db.Column(db.Integer)

class Grade(db.Model):

    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey('students.studentid'), nullable=True)
    student = db.relationship('Student', foreign_keys=studentid)
    assignmentid = db.Column(db.Integer, db.ForeignKey('assignments.assignmentid'), nullable=True)
    assignment = db.relationship('Assignment', foreign_keys=assignmentid)
    grade = db.Column(db.Integer)



#class NewStudent(Form):

# studentid = TextField("Student ID")
# sfirstname = TextField("First Name")
# slasttname = TextField("Last Name")
# major = TextField("Major")
# email = TextField("email")

@app.route("/", methods=["GET", "POST"])
#@app.route("/")
def index():
#def stable():
    #db = get_db()
    if request.method == "GET":
        #return render_template('main_page.html', students = students.query.all() )
        data = db.engine.execute("SELECT * FROM students")

        #student = Student(content=request.form["contents"])

        return render_template("main_page.html",data=data)
        #student = (
         #     'SELECT studentid, firstname, lastname, major, email'
          #       ' FROM Student'
           #      ' ORDER BY created DESC').fetchall()
        #return render_template('main_page.html', student=Student.query.all())

        #db.engine.execute("INSERT INTO students(studentid, firstname, lastname, major, email) VALUES (%s,%s,%s,%s,%s)", (studentid, firstname, lastname, major, email))
    #db.session.add(newstudent)
    #db.session.commit()


    if not current_user.is_authenticated:
        return redirect(url_for('index'))



#Add student
@app.route("/newstudent", methods=['GET', 'POST'])
#def newstudent():
    #form = NewStudent(newstudent.form)
    #return render_template('newstudent.html', form = form)
    #Student(form)

def newstudent():
   if request.method == 'POST':
      if not request.form['firstname'] or not request.form['lastname'] or not request.form['major']:
         flash('Please enter all the fields', 'error')
      else:
         students = Student(request.form['firstname'], request.form['lastname'], request.form['major'], request.form['email'])
         db.session.add(students)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('index'))
   return render_template('newstudent.html')

#Gradebook
@app.route("/grades")

def grades():
    #db = get_db()
    #if request.method == "GET":

        grades = db.engine.execute("SELECT grades.id, grades.studentid, grades.assignmentid, grades.grade, students.firstname, students.lastname FROM grades, students WHERE grades.studentid = students.studentid;")

        #student = Student(content=request.form["contents"])

        return render_template("grades_page.html",grades=grades)

    # if not current_user.is_authenticated:
      #  return redirect(url_

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))


@app.route("/logout/")
@login_required
def logout():
     logout_user()
     return redirect(url_for('index'))

