from .dbinitialization import db

class User(db.Document):
    userName=db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.StringField(required=True)
    userType = db.StringField(required=True)


class Student(db.Document):
    student_id = db.StringField(required=True)
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    dob = db.DateTimeField(required=True)
    phone_no = db.StringField(required=True)
    admission_date = db.DateTimeField(required=True)
    classroom_id = db.StringField(required=True)

class Teacher(db.Document):
    teacher_id = db.StringField(required=True)
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    phone_no = db.StringField(required=True)
    joining_date = db.DateTimeField(required=True)
    salary = db.FloatField(required=True)

class Quiz(db.EmbeddedDocument):
    quiz_id = db.StringField(required=True)
    quiz_topic = db.StringField(required=True)
    marks = db.FloatField(required=True)

class Assignment(db.EmbeddedDocument):
    assignment_id = db.StringField(required=True)
    assignment_topic = db.StringField(required=True)
    marks = db.FloatField(required=True)

class Course(db.Document):
    course_id = db.StringField(required=True)
    name = db.StringField(required=True)

class Marks(db.Document):
    student_id = db.StringField(required=True)
    course_id = db.StringField(required=True)
    quizzes = db.ListField(db.EmbeddedDocumentField(Quiz), required=True)
    assignments = db.ListField(db.EmbeddedDocumentField(Assignment), required=True)
    totalMarks = db.FloatField(required=True)

class Exam(db.Document):
    exam_id = db.StringField(required=True)
    course_id = db.StringField(required=True)
    teacher_id = db.StringField(required=True)
    classroom_id = db.StringField(required=True)
    exam_name = db.StringField(required=True)

class Attendance(db.Document):
    student_id = db.StringField(required=True)
    name = db.StringField(required=True)
    date = db.StringField(required=True)
    status = db.StringField(required=True)

class Classroom(db.Document):
    classroom_id = db.StringField(required=True)
    teacher_id = db.StringField(required=True)
    course_ids = db.ListField(db.StringField(), required=True)
    section = db.StringField(required=True)
    std_count = db.IntField(required=True)

