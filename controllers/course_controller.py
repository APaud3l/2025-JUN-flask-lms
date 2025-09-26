from flask import Blueprint, jsonify, request
from init import db

from models.course import Course
from schemas.schemas import course_schema, courses_schema

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
@courses_bp.route("/<int:course_id>")
def get_a_course(course_id):
    # Define the statement
    # SQL: SELECT * FROM courses WHERE course_id = course_id;
    stmt = db.select(Course).where(Course.course_id == course_id)
    # excute it
    course = db.session.scalar(stmt)
    # serialise it
    data = course_schema.dump(course)

    # if the course exists
    if data:
        # return it
        return jsonify(data)
    # else
    else:
        # ack
        return {"message": f"Course with id: {course_id} does not exist"}, 404

# CREATE - POST /
# DELETE - DELETE /course_id
# UPDAET - PUT/PATCH /course_id