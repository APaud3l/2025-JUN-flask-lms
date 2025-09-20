from flask import Blueprint, jsonify
from init import db
from models.student import Student, student_schema, students_schema


students_bp = Blueprint("students", __name__, url_prefix="/students")

# Routes to be defined
# GET /
@students_bp.route("/")
def get_students():
    # Define a statement: SELECT * FROM students;
    stmt = db.select(Student)
    # Execute it
    students_list = db.session.scalars(stmt)
    # Serialise it
    data = students_schema.dump(students_list)
    
    # Quick Python brain-teaser exercise
    print("The name of the students:", [student["name"] for student in data])

    if data:
        # Return the jsonify(list)
        return jsonify(data)
    else:
        return {"message": "No records found. Add a student to get started."}, 404

# GET /id
@students_bp.route("/<int:student_id>")
def get_a_student(student_id):
    # Define the statement: SELECT * FROM students WHERE id = student_id;
    stmt = db.select(Student).where(Student.student_id == student_id)
    # Execute it
    student = db.session.scalar(stmt)
    # Serialise it
    data = student_schema.dump(student)
    if data:
        # Return it
        return jsonify(data)
    else:
        return {"message": f"Student with id: {student_id} does not exist."}, 404

# POST /
# PUT/PATCH /id
# DELETE /id
