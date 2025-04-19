from flask import Flask ,jsonify, render_template, request,make_response ,session
from  database import dbinitialization
from database.models import User, Student, Teacher, Quiz, Assignment, Course, Exam, Attendance, Classroom, Marks
from flask_restful import Api

from datetime import datetime
app = Flask(__name__)
app.config["MONGODB_SETTINGS"]={'host':"mongodb://localhost:27017/School"}
dbinitialization.initialize_db(app)
app = Flask(__name__)
app.secret_key="bsjvhusdhg5565645"
api=Api(app)

@app.route("/")
def loginform():
    return render_template("Login.html")

@app.route("/login",methods=["POST"])
def login():
    try:
        uname=request.form["uname"]
        pwd = request.form["pwd"]
        data =User.objects(userName=uname)
        if data:
            session["uname"]=uname
            session["email"]=data[0]['email']
            mydata = User.objects()
            utype = ""
            for i in range(len(mydata)):
                if uname == mydata[i]["userName"]:
                    utype = mydata[i]["userType"]
                    session["utype"] = utype
                    break
            if utype == "Student":
                return render_template("Student.html", name=uname)
            elif utype == "Admin":
                return render_template("Admin.html", name=uname)
            else:
                return render_template("Teacher.html", name=uname)

        else:
            return render_template("Login.html", error="login failed, First Sign In To System")
    except Exception as e:
        return render_template("Login.html",error="Login error"+str(e))

@app.route("/logout")
def logout():
    try:
        session.clear()
        return render_template("login.html")
    except Exception as e:
        return render_template("Login.html", error=str(e))

@app.route("/addStudentsForm")
def addStudentsForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname != None and utype == "Admin":
        return render_template("AddStudents.html")
    else:
        return render_template("Login.html", error = "First Login to system with Owner Credientials")

@app.route("/addstudents", methods = ['GET', 'POST'])
def addStudents():
        try:
            uname = session.get("uname")
            count = int(request.form.get('count'))

            for i in range(1, count + 1):
                roll_no = request.form.get(f'rollno{i}')
                name = request.form.get(f'name{i}')
                email = request.form.get(f'email{i}')
                password = request.form.get(f'pwd{i}')
                dob = request.form.get(f'dob{i}')
                phone = request.form.get(f'phone{i}')
                adm_date = request.form.get(f'admDate{i}')
                classroom_id = request.form.get(f'classroom_id{i}')

                t = Student(student_id= roll_no, name = name, email= email, password = password, dob = dob, phone_no = phone, admission_date= adm_date, classroom_id = classroom_id).save()
                t = User(userName=name, password=password, email=email, userType="Student").save()

            return render_template("Admin.html", name=uname)
        except Exception as e:
            return render_template("AddStudents.html", error = str(e))


@app.route("/addTeachersForm")
def addTeachersForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname != None and utype == "Admin":
        return render_template("AddTeachers.html")
    else:
        return render_template("Login.html", error = "First Login to system with Owner Credientials")

@app.route("/addTeachers", methods = ['GET', 'POST'])
def addTeachers():
        try:
            uname = session.get("uname")
            count = int(request.form.get('count'))
            print(count)
            for i in range(1, count + 1):
                teacher_id = request.form.get(f'teacherid{i}')
                name = request.form.get(f'teachername{i}')
                email = request.form.get(f'teacheremail{i}')
                password = request.form.get(f'teacherpwd{i}')
                phone = request.form.get(f'teacherphone{i}')
                joining_date = request.form.get(f'teacherjoiningDate{i}')
                salary = float(request.form.get(f'teachersalary{i}'))

                teacher = Teacher(
                    teacher_id=teacher_id,
                    name=name,
                    email=email,
                    password=password,
                    phone_no=phone,
                    joining_date=joining_date,
                    salary=salary
                ).save()
                t = User(userName=name, password=password, email=email, userType="Teacher").save()
                print(teacher)

            return render_template("Admin.html", name=uname)
        except Exception as e:
            return render_template("AddTeachers.html", error = str(e))


@app.route("/addCourcesForm")
def addCourcesForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname != None and utype == "Admin":
        return render_template("AddCourses.html")
    else:
        return render_template("Login.html", error = "First Login to system with Owner Credientials")

@app.route("/addCources", methods = ['GET', 'POST'])
def addCources():
        try:
            uname = session.get("uname")
            count = int(request.form.get('count_courses'))
            for i in range(1, count + 1):
                course_id = request.form.get(f'courseid{i}')
                name = request.form.get(f'coursename{i}')

                course = Course(
                    course_id=course_id,
                    name=name
                )
                course.save()

            return render_template("Admin.html", name=uname)
        except Exception as e:
            return render_template("AddCourses.html", error = str(e))


@app.route("/addExamssForm")
def addExamssForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname != None and utype == "Admin":
        return render_template("AddExams.html")
    else:
        return render_template("Login.html", error = "First Login to system with Owner Credientials")

@app.route("/addExams", methods = ['GET', 'POST'])
def addExams():
        try:
            uname = session.get("uname")
            count = int(request.form.get('count_exams'))

            for i in range(1, count + 1):
                exam_id = request.form.get(f'examid{i}')
                course_id = request.form.get(f'examcourseid{i}')
                teacher_id = request.form.get(f'examteacherid{i}')
                classroom_id = request.form.get(f'examclassroomid{i}')
                exam_name = request.form.get(f'examexamname{i}')

                course = Course.objects(course_id = course_id)
                teacher = Teacher.objects(teacher_id = teacher_id)
                classroom = Classroom.objects(classroom_id = classroom_id)

                if course and teacher and classroom:
                    exam = Exam(
                        exam_id=exam_id,
                        course_id=course_id,
                        teacher_id=teacher_id,
                        classroom_id=classroom_id,
                        exam_name=exam_name
                    )
                    exam.save()
            return render_template("Admin.html", name=uname)
        except Exception as e:
            return render_template("AddExams.html", error = str(e))


@app.route("/addClassroomsForm")
def addClassroomsForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname != None and utype == "Admin":
        return render_template("AddClassrooms.html")
    else:
        return render_template("Login.html", error = "First Login to system with Owner Credientials")

@app.route("/addClassrooms", methods = ['GET', 'POST'])
def addClassrooms():
        try:
            uname = session.get("uname")
            count_courses = int(request.form.get('count_courses'))
            course_ids = []
            for i in range(1, count_courses + 1):
                course_id = request.form.get(f'courseid{i}')

                courseData = Course.objects(course_id = course_id)
                if courseData :
                    course_ids.append(course_id)

            classroom_id = request.form.get('classroom_id')
            teacher_id = request.form.get('teacher_id')
            section = request.form.get('section')
            std_count = int(request.form.get('std_count'))

            teacherData = Teacher.objects(teacher_id = teacher_id)
            if teacherData:
                classroom = Classroom(
                    classroom_id=classroom_id,
                    teacher_id=teacher_id,
                    course_ids=course_ids,
                    section=section,
                    std_count=std_count
                )
                classroom.save()
            return render_template("Admin.html", name=uname)
        except Exception as e:
            return render_template("AddClassrooms.html", error = str(e))


@app.route("/students",methods=["GET"])
def students():
    try:
        uname = session.get("uname")
        data =Student.objects()
        return render_template("ViewStudents.html",data=data)

    except Exception as e:
        return render_template("Admin.html",error="Admin error"+str(e))

@app.route("/teachers",methods=["GET"])
def teachers():
    try:
        uname = session.get("uname")
        data =Teacher.objects()
        return render_template("ViewTeachers.html",data=data)

    except Exception as e:
        return render_template("Admin.html",error="Admin error"+str(e))

@app.route("/cources",methods=["GET"])
def cources():
    try:
        uname = session.get("uname")
        data = Course.objects()
        return render_template("ViewCources.html",data=data)

    except Exception as e:
        return render_template("Admin.html",error="Admin error"+str(e))

@app.route("/classrooms",methods=["GET"])
def classrooms():
    try:
        uname = session.get("uname")
        data =Classroom.objects()
        return render_template("ViewClassrooms.html",data=data)

    except Exception as e:
        return render_template("Admin.html",error="error: "+str(e))

@app.route("/exams",methods=["GET"])
def exams():
    try:
        uname = session.get("uname")
        data =Exam.objects()
        return render_template("ViewExams.html",data=data)

    except Exception as e:
        return render_template("Admin.html",error="restaurant error"+str(e))


@app.route("/updateStudentForm")
def updateStudentForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname != None and utype == "Admin":
        return render_template("UpdateStudent.html")
    else:
        return render_template("Login.html", error = "First Login to system with Owner Credientials")

@app.route("/updateStudent" , methods=['GET', 'POST'])
def updateStudent():
    try:
        uname = session.get("uname")
        id = request.form["id"]
        updatedName = request.form["name"]
        updatedEmail = request.form["email"]
        updatedPassword = request.form["password"]
        updatedDob = request.form["dob"]
        updatedPhoneNo = request.form["phone_no"]
        updatedAdmissionDate = request.form["admission_date"]
        updatedClassroomId = request.form["classroom_id"]


        if updatedName != '':
            Student.objects(student_id = id).update(name=updatedName)
        if updatedEmail != '':
            Student.objects(student_id = id).update(email=updatedEmail)
        if updatedPassword != '':
            Student.objects(student_id = id).update(password=updatedPassword)
        if updatedDob != '':
            Student.objects(student_id = id).update(dob=updatedDob)
        if updatedPhoneNo != '':
            Student.objects(student_id = id).update(phone_no=updatedPhoneNo)
        if updatedAdmissionDate != '':
            Student.objects(student_id = id).update(admission_date=updatedAdmissionDate)
        if updatedClassroomId != '':
            Student.objects(student_id = id).update(classroom_id=updatedClassroomId)

        return render_template("Admin.html", name = uname)
    except Exception as e:
        return render_template("UpdateStudent.html", error = str(e))


@app.route("/updateTeacherForm")
def updateTeacherForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname is not None and utype == "Admin":
        return render_template("UpdateTeacher.html")
    else:
        return render_template("Login.html", error="First login to the system with Owner Credentials")

@app.route("/updateTeacher", methods=['GET','POST'])
def updateTeacher():
    try:
        uname = session.get("uname")
        teacher_id = request.form["teacher_id"]
        updated_name = request.form["name"]
        updated_email = request.form["email"]
        updated_password = request.form["password"]
        updated_phone_no = request.form["phone_no"]
        updated_joining_date = request.form["joining_date"]
        updated_salary = request.form["salary"]

        if updated_name != '':
            Teacher.objects(teacher_id=teacher_id).update(name=updated_name)
        if updated_email != '':
            Teacher.objects(teacher_id=teacher_id).update(email=updated_email)
        if updated_password != '':
            Teacher.objects(teacher_id=teacher_id).update(password=updated_password)
        if updated_phone_no != '':
            Teacher.objects(teacher_id=teacher_id).update(phone_no=updated_phone_no)
        if updated_joining_date != '':
            Teacher.objects(teacher_id=teacher_id).update(joining_date=updated_joining_date)
        if updated_salary != '':
            Teacher.objects(teacher_id=teacher_id).update(salary=updated_salary)

        return render_template("Admin.html", name=uname)
    except Exception as e:
        return render_template("UpdateTeacher.html", error=str(e))

@app.route("/updateCourseForm")
def updateCourseForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname is not None and utype == "Admin":
        return render_template("UpdateCourse.html")
    else:
        return render_template("Login.html", error="First login to the system with Owner Credentials")

@app.route("/updateCourse", methods=['GET', 'POST'])
def updateCourse():
    try:
        uname = session.get("uname")
        course_id = request.form["course_id"]
        updated_name = request.form["name"]

        if updated_name != '':
            Course.objects(course_id=course_id).update(name=updated_name)

        return render_template("Admin.html", name=uname)
    except Exception as e:
        return render_template("UpdateCourse.html", error=str(e))


@app.route("/updateExamForm")
def updateExamForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname is not None and utype == "Admin":
        return render_template("UpdateExam.html")
    else:
        return render_template("Login.html", error="First login to the system with Owner Credentials")


@app.route("/updateExam", methods=['GET', 'POST'])
def updateExam():
    try:
        uname = session.get("uname")
        exam_id = request.form["exam_id"]
        updated_course_id = request.form["course_id"]
        updated_teacher_id = request.form["teacher_id"]
        updated_classroom_id = request.form["classroom_id"]
        updated_exam_name = request.form["exam_name"]

        teacher = Teacher.objects(teacher_id=updated_teacher_id)
        course = Course.objects(course_id = updated_course_id)
        classroom = Classroom.objects(classroom_id = updated_classroom_id)
        if updated_course_id != '' and course:
            Exam.objects(exam_id=exam_id).update(course_id=updated_course_id)
        if updated_teacher_id != ''and teacher:
            Exam.objects(exam_id=exam_id).update(teacher_id=updated_teacher_id)
        if updated_classroom_id != '' and classroom:
            Exam.objects(exam_id=exam_id).update(classroom_id=updated_classroom_id)
        if updated_exam_name != '':
            Exam.objects(exam_id=exam_id).update(exam_name=updated_exam_name)

        return render_template("Admin.html", name=uname)
    except Exception as e:
        return render_template("UpdateExam.html", error=str(e))

@app.route("/updateClassroomForm")
def updateClassroomForm():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname is not None and utype == "Admin":
        return render_template("UpdateClassroom.html")
    else:
        return render_template("Login.html", error="First login to the system with Owner Credentials")


@app.route("/updateClassroom", methods=['GET','POST'])
def updateClassroom():
    try:
        uname = session.get("uname")
        classroom_id = request.form["classroom_id"]
        updated_teacher_id = request.form["teacher_id"]
        updated_section = request.form["section"]
        updated_std_count = int(request.form["std_count"])

        teacher = Teacher.objects(teacher_id = updated_teacher_id)
        if updated_teacher_id != '' and teacher:
            Classroom.objects(classroom_id=classroom_id).update(teacher_id=updated_teacher_id)

        if updated_section != '':
            Classroom.objects(classroom_id=classroom_id).update(section=updated_section)
        if updated_std_count:
            Classroom.objects(classroom_id=classroom_id).update(std_count=updated_std_count)

        return render_template("Admin.html", name=uname)
    except Exception as e:
        return render_template("UpdateClassroom.html", error=str(e))


@app.route("/showCourses",methods=['GET'])
def ShowCourses():

    name = session.get("uname")
    emai = session.get("email")
    if name:
        dat=Student.objects(email=emai)
        st_name=dat[0]["name"]
        st_classroom_id=dat[0]["classroom_id"]
        data=Classroom.objects(classroom_id=st_classroom_id)
        dic={}
        for i in data[0]["course_ids"]:
            nam=Course.objects(course_id=i)
            dic[i]=nam[0]["name"]

        st_techer_id=data[0]["teacher_id"]
        dat=Teacher.objects(teacher_id=st_techer_id)
        tech_name=dat[0]["name"]
        return render_template("Courses.html",st_name=st_name,cls_id=st_classroom_id,tec_name=tech_name,data=dic)
    else:
        return render_template("login.html", error="Please login first")


@app.route("/getMarks/<string:course_id>",methods=["GET"])
def getMarks(course_id):
    name = session.get("uname")
    emai = session.get("email")
    if name:

        dat = Student.objects(email=emai)
        data = Marks.objects(course_id=course_id,student_id=dat[0]["student_id"] )
        st_name = dat[0]["name"]
        st_classroom_id = dat[0]["classroom_id"]
        data2 = Classroom.objects(classroom_id=st_classroom_id)
        st_techer_id = data2[0]["teacher_id"]
        dat = Teacher.objects(teacher_id=st_techer_id)
        tech_name = dat[0]["name"]

        return render_template("marks.html",st_name=st_name,cls_id=st_classroom_id,tec_name=tech_name,data=data[0])
    else:
        return render_template("login.html", error="Please login first")

@app.route("/showAttendence",methods=['GET'])
def ShowAttendence():

    name = session.get("uname")
    emai = session.get("email")
    if name:
        dat=Student.objects(email=emai)
        st_id=dat[0]["student_id"]
        dat=Attendance.objects(student_id=st_id)
        return render_template("AllAttendence.html",data=dat)
    else:
        return render_template("login.html", error="Please login first")


@app.route("/markAttendance", methods=['GET', 'POST'])
def markAttendance():
    if request.method == 'POST':

        name = session.get("uname")
        emai = session.get("email")

        if name:
            dat = Teacher.objects(email=emai)
            teacher_id = dat[0]["teacher_id"]
            dat1 = Classroom.objects(teacher_id=teacher_id)
            classroom_id = dat1[0]["classroom_id"]
            dat2 = Student.objects(classroom_id=classroom_id)

            date = datetime.today().strftime('%Y-%m-%d')

            for student in dat2:
                student_id = student.student_id
                student_name = student.name
                attendance_key = f'attendance_{student_id}'

                if request.form.get(attendance_key) == 'on':
                    status = 'Present'
                else:
                    status = 'Absent'

                attendance_record = Attendance(
                    student_id=student_id,
                    name=student_name,
                    date=date,
                    status=status
                )
                attendance_record.save()

            return render_template("Teacher.html", msg="Attendance marked successfully")

        else:
            return render_template("login.html", error="Please login first")
    else:

        name = session.get("uname")
        emai = session.get("email")

        if name:
            dat = Teacher.objects(email=emai)
            teacher_id = dat[0]["teacher_id"]
            dat1 = Classroom.objects(teacher_id=teacher_id)
            classroom_id = dat1[0]["classroom_id"]
            dat2 = Student.objects(classroom_id=classroom_id)

            return render_template("MarkAttendance.html", data=dat2)

        else:
            return render_template("login.html", error="Please login first")


@app.route("/courcesStudents",methods=["GET"])
def courcesStudents():
    try:
        uname = session.get("uname")
        utype = session.get("utype")
        emai = session.get("email")
        if uname != None and utype == "Teacher":
            dat = Teacher.objects(email=emai)
            teacher_id = dat[0]["teacher_id"]
            dat1 = Classroom.objects(teacher_id=teacher_id)
            classroom_id = dat1[0]["classroom_id"]
            course_ids = dat1[0]["course_ids"]
            ids = []
            names = []
            data = Course.objects()

            index = 0
            while index < len(course_ids):
                current_course_id = course_ids[index]
                matching_courses = [course for course in data if course.course_id == current_course_id]

                if matching_courses:
                    matched_course = matching_courses[0]
                    ids.append(matched_course.course_id)
                    names.append(matched_course.name)
                index += 1

            return render_template("TeachersCources.html",ids = ids, names = names)

    except Exception as e:
        return render_template("Admin.html",error="Admin error"+str(e))


@app.route("/marksEntryfORM")
def marksEntryfORM():
    uname = session.get("uname")
    utype = session.get("utype")
    if uname != None and utype == "Teacher":
        return render_template("MarksEntry.html")
    else:
        return render_template("Login.html", error = "First Login to system with Owner Credientials")

@app.route("/marksEntry", methods=['GET', 'POST'])
def marksEntry():
    try:
        uname = session.get("uname")
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        no_of_quizzes = int(request.form.get('no_of_quizzes'))

        quizzes = []
        for i in range(1, no_of_quizzes + 1):
            quiz_id = request.form.get(f'quiz_id{i}')
            quiz_topic = request.form.get(f'quiz_topic{i}')
            quiz_marks = float(request.form.get(f'quiz_marks{i}'))
            quizzes.append(Quiz(quiz_id=quiz_id, quiz_topic=quiz_topic, marks=quiz_marks))

        no_of_assignments = int(request.form.get('no_of_assignments'))
        assignments = []
        for i in range(1, no_of_assignments + 1):
            assignment_id = request.form.get(f'assignment_id{i}')
            assignment_topic = request.form.get(f'assignment_topic{i}')
            assignment_marks = float(request.form.get(f'assignment_marks{i}'))
            assignments.append(
                Assignment(assignment_id=assignment_id, assignment_topic=assignment_topic, marks=assignment_marks))

        total_marks = sum([quiz.marks for quiz in quizzes]) + sum([assignment.marks for assignment in assignments])

        marks_instance = Marks(student_id=student_id, course_id=course_id, quizzes=quizzes, assignments=assignments,
                               totalMarks=total_marks)
        marks_instance.save()

        return render_template("Teacher.html", msg = "Successfully added marks")

    except Exception as e:
        return render_template("MarksEntry.html", error=str(e))


@app.route("/markStudents", methods=['GET', 'POST'])
def markStudents():
        name = session.get("uname")
        emai = session.get("email")

        if name:
            dat = Teacher.objects(email=emai)
            teacher_id = dat[0]["teacher_id"]
            dat1 = Classroom.objects(teacher_id=teacher_id)
            classroom_id = dat1[0]["classroom_id"]
            dat2 = Student.objects(classroom_id=classroom_id)

            return render_template("StudentsMarks.html", data=dat2)

        else:
            return render_template("login.html", error="Please login first")


if __name__ == '__main__':
    app.run(debug=True, port=8001)
