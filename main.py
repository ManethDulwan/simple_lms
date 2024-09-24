from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
def get_db_connection():
    # Replace these with your actual database connection details
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lms'
    )

@app.route("/add", methods=['POST'])
def add_student():
    name = request.form.get('name')
    grade = request.form.get('grade')

    # Validate input data
    if not name or not grade:
        return jsonify({"error": "Invalid input"}), 400

    # Insert data into the database
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", (name, grade))
        connection.commit()  # Commit the changes
        return jsonify({"message": "Student added successfully", "name": name, "grade": grade}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
@app.route("/get", methods=['GET'])
def get_all_students():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()  # Fetch all results
        student_list = [{'id':student[0],'name': student[1], 'grade': student[2]} for student in students]
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(student_list), 200

@app.route("/update", methods=['POST'])
def update_student():
    data = request.get_json()
    student_id = data.get('id')
    name = data.get('name')
    grade = data.get('grade')

    # Validate input data
    if not student_id or not name or not grade:
        return jsonify({"error": "Invalid input"}), 400

    # Insert data into the database
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE students SET name = %s, grade = %s WHERE id = %s",
            (name, grade, student_id)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        connection.commit()  # Commit the changes
        return jsonify({"message": "Student updated successfully", "id": student_id, "name": name, "grade": grade}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
@app.route("/delete", methods=['POST'])
def delete_student():
    data = request.get_json()
    student_id = data.get('id')

    # Validate input data
    if not student_id:
        return jsonify({"error": "Invalid input"}), 400

    # Delete data from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
        connection.commit()  # Commit the changes
        return jsonify({"message": "Student deleted successfully", "id": student_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/search", methods=['POST'])
def serach_users():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'message': 'Database connection failed'}), 500

    cursor = connection.cursor()
    data = request.get_json()
    student_id = data.get('search')
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s",(student_id,))
        students = cursor.fetchall()  # Fetch all results
        student_list = [{'id':student[0],'name': student[1], 'grade': student[2]} for student in students]
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(student_list), 200

if __name__ == "__main__":
    app.run(debug=True)
