from flask import Blueprint, jsonify, request
from init import db
from models.student import Student, student_schema, students_schema

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


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
@students_bp.route("/", methods=["POST"])
def create_student():
    try:
        # GET details from the REQUEST Body
        body_data = request.get_json()
        # Create a Student Object with the REQUEST Body data

        # Method 1: Error handling for unique email constraint
        # email = body_data.get("email")

        # stmt = db.select(Student).where(Student.email == email)
        # student = db.session.scalar(stmt)
        # data = student_schema.dump(student)

        # if data:
        #     return {"message": f"The Student with email:{email} already exists."}, 409
        
        new_student = Student(
            name = body_data.get("name"),
            email = body_data.get("email"),
            address = body_data.get("address")
        )
        # Add to the session
        db.session.add(new_student)
        # Commit the session
        db.session.commit()
        # Send ack
        data = student_schema.dump(new_student)
        return jsonify(data), 201
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        else:
            return  {"message": "Integrity Error occured."}, 409
    except:
        return {"message": "Unexpected error occured."}

# PUT/PATCH /id
# DELETE /id
