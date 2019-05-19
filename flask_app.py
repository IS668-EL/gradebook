from flask import Flask, redirect, render_template, request, url_for
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin #add current_user back in later
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
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


#@app.route("/", methods=["GET", "POST"])
@app.route("/")
#def index():
def stable():
    #db = get_db()
    #if request.method == "GET":

        data = db.engine.execute("SELECT * FROM students")

        #student = Student(content=request.form["contents"])

        return render_template("main_page.html",data=data)
        #student = (
         #     'SELECT studentid, firstname, lastname, major, email'
          #       ' FROM Student'
           #      ' ORDER BY created DESC').fetchall()
        #return render_template('main_page.html', student=Student.query.all())

    #if not current_user.is_authenticated:
     #   return redirect(url_for('index'))

    #student = Student(content=request.form["contents"], commenter=current_user)
    #db.session.add(grade)
    #db.session.commit()
    #return redirect(url_for('index'))


#Gradebook
@app.route("/grades")
#def index():
def grades():
    #db = get_db()
    #if request.method == "GET":

        grade = db.engine.execute("SELECT * FROM grades")

        #student = Student(content=request.form["contents"])

        return render_template("main_page.html",grade=grade)

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

