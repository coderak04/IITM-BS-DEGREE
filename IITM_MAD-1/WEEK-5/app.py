from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'database.sqlite3')
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Student(db.Model):
    __tablename__='student'
    student_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    roll_number=db.Column(db.String,unique=True,nullable=False)
    first_name=db.Column(db.String,nullable=False)
    last_name=db.Column(db.String)
    courses = db.relationship("Course", secondary='enrollments',backref="Student")

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String,  nullable=False)
    course_description = db.Column(db.String)


class Enroll(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"),nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"),nullable=False)

@app.route("/")
def index():
    slist=Student.query.all()
    return render_template("index.html",student_list=slist)

@app.route("/student/create",methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        result=request.form
        selected=result.getlist('courses')
        roll=result['roll']
        s3=Student.query.filter_by(roll_number=roll).all()
        if(len(s3)!=0):
            return render_template("student_exists.html")
        s1=Student(roll_number=roll,first_name=result['f_name'],last_name=result['l_name'])
        db.session.add(s1)
        db.session.commit()
        if(len(selected)!=0):
            for courses in selected:
                courses_id=int(courses[-1])
                c1=Course.query.get(courses_id)
                s1.courses.append(c1)
        db.session.commit()
        return redirect("/")
    return render_template("add_student.html")

@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
        s1 = Student.query.get(student_id)
        db.session.delete(s1)
        db.session.commit()
        return redirect('/')
        
@app.route("/student/<int:student_id>")
def student_detail(student_id):
    student_idd = Student.query.get(student_id)
    c1 = student_idd.courses
    return render_template("student_details.html",student_id = student_idd,courses = c1)
    
@app.route("/student/<int:student_id>/update" , methods =['GET','POST'])
def update_details(student_id):
    if request.method == 'POST':
        s1 = Student.query.get(student_id)
        s1.first_name = request.form['f_name']
        if request.form['l_name']!='':
            s1.last_name = request.form['l_name']
        db.session.add(s1)
        s1.courses = []
        db.session.commit()
        selected = request.form.getlist('courses')
        if len(selected)!=0:
            for courses in selected:
                x = int(courses[-1])
                c1 = Course.query.get(x)
                s1.courses.append(c1)
                db.session.commit()
        return redirect('/')
    return render_template("update.html",student_id = student_id)

if __name__ == '__main__':
    app.run(debug= True)