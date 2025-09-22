from flask import Blueprint, jsonify, request
from init import db
from models.teacher import Teacher, teacher_schema, teachers_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

# CREATE - POST /
# READ - GET / AND GET /id
# UPDATE - PUT/PATCH /id
# DELETE - DELETE /id

# READ - GET /
@teachers_bp.route("/")
def get_teachers():
    # Define the statement for GET All teacher: SELECT * FROM teachers;
    stmt = db.select(Teacher)
    # Execute it
    teachers_list = db.session.scalars(stmt)

    # Serialise it
    data = teachers_schema.dump(teachers_list)

    if data:
        # Return the jsonify(list)
        return jsonify(data)
    else:
        return {"message": "No records found. Add a teacher to get started."}, 404