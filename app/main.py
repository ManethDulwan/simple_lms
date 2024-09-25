from flask import Flask, request, jsonify
from flask_cors import CORS
from Models.models import db, Student

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/add", methods=['POST'])
def add_student():
    name = request.form.get('name')
    grade = request.form.get('grade')

    if not name or not grade:
        return jsonify({"error": "Invalid input"}), 400

    try:
        student_id = Student.add_student(name, grade)
        return jsonify({"message": "Student added successfully", "id": student_id, "name": name, "grade": grade}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/get", methods=['GET'])
def get_all_students():
    try:
        students = Student.get_all_students()
        student_list = [{'id': student.id, 'name': student.name, 'grade': student.grade} for student in students]
        return jsonify(student_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/update", methods=['POST'])
def update_student():
    data = request.get_json()
    student_id = data.get('id')
    name = data.get('name')
    grade = data.get('grade')

    if not student_id or not name or not grade:
        return jsonify({"error": "Invalid input"}), 400

    try:
        updated_id = Student.update_student(student_id, name, grade)
        if not updated_id:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": "Student updated successfully", "id": student_id, "name": name, "grade": grade}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/delete", methods=['POST'])
def delete_student():
    data = request.get_json()
    student_id = data.get('id')

    if not student_id:
        return jsonify({"error": "Invalid input"}), 400

    try:
        deleted_id = Student.delete_student(student_id)
        if not deleted_id:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"message": "Student deleted successfully", "id": deleted_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/search", methods=['POST'])
def search_student():
    data = request.get_json()
    student_id = data.get('search')

    try:
        students = Student.search_student(student_id)
        student_list = [{'id': student.id, 'name': student.name, 'grade': student.grade} for student in students]
        return jsonify(student_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
