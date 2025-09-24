from flask import Blueprint, jsonify, request
from init import db
from models.course import Course, course_schema, courses_schema

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

# READ - GET /
@courses_bp.route("/")
def get_courses():
    # Define the statement
    stmt = db.select(Course)
    # Execute it
    courses_list = db.session.scalars(stmt)

    # serialise it
    data = courses_schema.dump(courses_list)
    # If it exists:
    if data:
        # return it
        return jsonify(data)
    # Else:
    else:
        # Acknowledge
        return {"message": "No courses created yet."}, 404


# READ a course - GET /course_id
# CREATE - POST /
# DELETE - DELETE /course_id
# UPDAET - PUT/PATCH /course_id