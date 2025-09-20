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

    if data:
        # Return the jsonify(list)
        return jsonify(data)
    else:
        return {"message": "No records found. Add a student to get started."}

# GET /id
# POST /
# PUT/PATCH /id
# DELETE /id
