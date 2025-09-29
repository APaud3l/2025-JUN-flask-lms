from flask import Blueprint, jsonify, request

from init import db
from models.enrolment import Enrolment
from schemas.schemas import enrolment_schema, enrolments_schema

enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/enrolments")

# Read all
@enrolments_bp.route("/")
def get_enrolments():
    # Get potential filters from query params
    course_id = request.args.get("course_id", type=int)
    student_id = request.args.get("student_id", type=int)
    
    # define the stmt
    stmt = db.select(Enrolment)
    
    # Testing
    # print(Enrolment.course.name)
    
    # Add filters based on the params provided
    if course_id:
        stmt = stmt.where(Enrolment.course_id == course_id)
    if student_id:
        stmt = stmt.where(Enrolment.student_id == student_id)
        # stmt = stmt.filter_by(student_id = student_id)
    # execute it
    enrolments_list = db.session.scalars(stmt)
    # serliase it
    data = enrolments_schema.dump(enrolments_list)
    
    # print(data)
    if data:
        return jsonify(data)
    # return it
    else:
        return {"message": "No enrolments found."}, 404
    
