from flask import Blueprint, jsonify

from init import db
from models.enrolment import Enrolment
from schemas.schemas import enrolment_schema, enrolments_schema

enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/enrolments")

# Read all
@enrolments_bp.route("/")
def get_enrolments():
    # define the stmt
    stmt = db.select(Enrolment)
    # execute it
    enrolments_list = db.session.scalars(stmt)
    # serliase it
    data = enrolments_schema.dump(enrolments_list)
    if data:
        return jsonify(data)
    # return it
    else:
        return {"message": "No enrolments found."}, 404