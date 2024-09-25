from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

    @staticmethod
    def add_student(name, grade):
        new_student = Student(name=name, grade=grade)
        db.session.add(new_student)
        db.session.commit()
        return new_student.id

    @staticmethod
    def get_all_students():
        return Student.query.all()

    @staticmethod
    def update_student(student_id, name, grade):
        student = Student.query.get(student_id)
        if not student:
            return None
        student.name = name
        student.grade = grade
        db.session.commit()
        return student.id

    @staticmethod
    def delete_student(student_id):
        student = Student.query.get(student_id)
        if not student:
            return None
        db.session.delete(student)
        db.session.commit()
        return student_id

    @staticmethod
    def search_student(student_id):
        return Student.query.filter_by(id=student_id).all()
