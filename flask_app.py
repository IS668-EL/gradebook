from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin #add current_user back in later
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField
from werkzeug.security import check_password_hash

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config["DEBUG"] = True

bootstrap = Bootstrap(app)

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


    def __init__(self, studentid, firstname, lastname, major, email):
         self.studentid = studentid
         self.firstname = firstname
         self.lastname = lastname
         self.major = major
         self.email = email

class Assignment(db.Model):

    __tablename__ = "assignments"

    assignmentid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    fullscore = db.Column(db.Integer)

    def __init__(self, assignmentid, title, fullscore):
         self.assignmentid = assignmentid
         self.title = title
         self.fullscore = fullscore


class Grade(db.Model):

    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey('students.studentid'), nullable=True)
    student = db.relationship('Student', foreign_keys=studentid)
    assignmentid = db.Column(db.Integer, db.ForeignKey('assignments.assignmentid'), nullable=True)
    assignment = db.relationship('Assignment', foreign_keys=assignmentid)
    grade = db.Column(db.Integer)


class NewStudent(Form):

 studentid = TextField("Student ID")
 sfirstname = TextField("First Name")
 slasttname = TextField("Last Name")
 major = TextField("Major")
 email = TextField("email")


class UpdateGrade(FlaskForm):

    studentid = StringField('StudentId', validators=[DataRequired()])
    assignmentid = StringField('AssignmentId', validators=[DataRequired()])
    grade = StringField('Grade', validators=[DataRequired()])
    submit = SubmitField('Submit')

#@app.route("/", methods=["GET", "POST"])
@app.route('/')
@app.route('/students', methods=["GET", "POST"])
def index():
#def stable():
    #db = get_db()
    if request.method == "GET":
        #return render_template('main_page.html', students = students.query.all() )
        data = db.engine.execute("SELECT * FROM students")

        #student = Student(content=request.form["contents"])

        return render_template("main_page.html",data=data)



    if not current_user.is_authenticated:
        return redirect(url_for('index'))



#Add student
@app.route("/newstudent", methods=['GET', 'POST'])

def newstudent():
   if request.method == 'POST':
      if not request.form['firstname'] or not request.form['lastname'] or not request.form['major']:
         flash('Please enter all the fields', 'error')
      else:
         students = Student(request.form['studentid'], request.form['firstname'], request.form['lastname'], request.form['major'], request.form['email'])
         db.session.add(students)
         db.session.commit()
    #add 4 grades for the new student
         grades1 = Grade(studentid=request.form['studentid'],assignmentid=1,grade=0)
         db.session.add(grades1)
         grades2 = Grade(studentid=request.form['studentid'],assignmentid=2,grade=0)
         db.session.add(grades2)
         grades3 = Grade(studentid=request.form['studentid'],assignmentid=3,grade=0)
         db.session.add(grades3)
         grades4 = Grade(studentid=request.form['studentid'],assignmentid=4,grade=0)
         db.session.add(grades4)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('index'))
   return render_template('newstudent.html')

#Update Student
@app.route("/student/<int:studentid>/update_student", methods=['GET', 'POST'])

def update(studentid):

    newstudent = Student.query.get_or_404(studentid)
    form = NewStudent(obj=newstudent)

    if form.validate_on_submit():
        studentid = form.studentid
        firstname = form.firstname
        lastname = form.lastname
        major = form.major
        email = form.email
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('index'))


        form.email = email
        form.major =major
        form.lastname = lastname
        form.firstname = firstname
        form.studentid = studentid

    return render_template('student/update_student.html', action="Edit",
                            form=form, newstudent=newstudent, title="Edit Student")



    #newfirstname = request.form.get("newfirstname")
    #oldfirstname = request.form.get("oldfirstname")
    #student = Student.query.filter_by(firstname=oldfirstname).first()
    #student.firstname = newfirstname
    #db.session.commit()
    #return redirect(url_for('index'))


  #  newstudent = Student(request.form['newstudentid'], request.form['newfirstname'], request.form['newlastname'], request.form['newmajor'], request.form['newemail'])
   # oldstudent = Student(request.form['oldstudentid'], request.form['oldfirstname'], request.form['oldlastname'], request.form['oldmajor'], request.form['oldemail'])

    #student = Student.query.filter_by(student=oldstudent)
    #newstudent = Student(student)
    #if request.method == 'POST':
     #    db.session.commit(newstudent)
      #   return redirect(url_for('index'))
    #else:
     #   return render_template('update_student.html')

#Delete student
@app.route("/students/<int:studentid>/deletestudent/", methods=['GET', 'POST'])
def deletestudent(studentid):
    #first delete grades
    deletegrade = Grade.query.get_or_404(studentid)
    db.session.delete(deletegrade)
    db.session.commit()

    deletestudent = Student.query.get_or_404(studentid)
    db.session.delete(deletestudent)
    db.session.commit()
    flash('deleted!')
    return redirect(url_for('index'))

    return render_template('deletestudent.html',student = deletestudent)


#Gradebook
@app.route("/grades")

def grades():


        grades = db.engine.execute("SELECT grades.id, grades.studentid, grades.assignmentid, grades.grade, students.firstname, students.lastname, assignments.title, assignments.fullscore FROM grades, students, assignments WHERE grades.studentid = students.studentid AND grades.assignmentid = assignments.assignmentid;")



        return render_template("grades_page.html",grades=grades)

@app.route('/grades/updategrade/<int:id>', methods=['GET', 'POST'])

def update_grades(id):

    grades = Grade.query.get_or_404(id)
    form = UpdateGrade(obj=grades)
    if form.validate_on_submit():
        grades.studentid = form.studentid.data
        grades.assignmentid = form.assignmentid.data
        grades.grade = form.grade.data
        db.session.commit()
        flash('You have successfully updated the grade.')

        # redirect to the grades page
        return redirect(url_for('grades'))

    form.studentid.data = grades.studentid
    form.assignmentid.data = grades.assignmentid
    form.grade.data = grades.grade
    return render_template('updategrade_page.html', action="Edit",
                            form=form, grades=grades, title="Update Grade")
        #return render_template("grades_page.html",grades=grades)

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

