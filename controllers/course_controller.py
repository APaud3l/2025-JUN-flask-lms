from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

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
@courses_bp.route("/", methods=["POST"])
def create_course():
    try:
        # Get the data from the Request Body
        body_data = request.get_json()
        # Create a course instance
        new_course = Course(
            name = body_data.get("name"),
            duration = body_data.get("duration"),
            teacher_id = body_data.get("teacher_id")
        )
        # Add to the session
        db.session.add(new_course)
        # Commit it
        db.session.commit()
        # Return the response
        return jsonify(course_schema.dump(new_course)), 201
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION: # foreign key violation
            # return {"message": err.orig.diag.message_detail}, 409
            return {"message": "Invalid teacher selected."}, 409
        else:
            return  {"message": "Integrity Error occured."}, 409
    except:
        return {"message": "Unexpected error occured."}, 400
        

# DELETE - DELETE /course_id
# UPDAET - PUT/PATCH /course_id