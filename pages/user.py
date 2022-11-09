from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from model_objects import Session, Users, Notes, TagNote
from validation_schemas import UserCreate, UserUpdate, UserInfo, NoteCreate

user = Blueprint('user', __name__, url_prefix='/user')
bcrypt = Bcrypt()
session = Session()

@user.route('/', methods=['POST'])
def add_user():
    try:
        user = UserCreate().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    existsUserName = session.query(Users).filter_by(username=user['username']).first()
    if existsUserName:
        return Response(status=400, response='The username is used by other user')
    existsEmail = session.query(Users).filter_by(email=user['email']).first()
    if existsEmail:
        return Response(status=400, response='The email is used by other user')
    hashed_password = bcrypt.generate_password_hash(user['password']) 
    new_user = Users(first_name=user['first_name'], last_name=user['last_name'], username=user['username'], email=user['email'], password=hashed_password)
    session.add(new_user)
    session.commit()

    return Response(response="New user was successfully created!")

@user.route('/<int:user_id>', methods=['PUT'])
def update_tag(user_id):
    try:
        user_update = UserUpdate().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    db_user = session.query(Users).filter_by(id=user_id).first()
    if not db_user:
        return Response(status=404, response='An user with provided ID was not found.')

    if 'first_name' in user_update.keys():
        db_user.first_name = user_update['first_name']
    if 'last_name' in user_update.keys():
        db_user.last_name = user_update['last_name']
    if 'username' in user_update.keys():
        existsUsername = session.query(Users.id).filter_by(username=user_update['username']).first()
        if existsUsername:
            return Response(status=400, response='User with such username already exists.')
        db_user.username = user_update['username']
    if 'email' in user_update.keys():
        existsEmail = session.query(Users.id).filter_by(email=user_update['email']).first()
        if existsEmail:
            return Response(status=400, response='User with such email already exists.')
        db_user.email = user_update['email']
    if 'password' in user_update.keys():
        hashed_password = bcrypt.generate_password_hash(user_update['password'])
        db_user.password = hashed_password
    session.commit()


#Умова перевірки чи вказують одинакові дані
    return Response(response="The user was successfully updated")

@user.route('/<int:user_id>', methods=['DELETE'])
def delete_tag(user_id):
    db_user = session.query(Users).filter_by(id=user_id).first()
    if not db_user:
        return Response(status=404, response='An user with provided ID was not found.')

    session.delete(db_user)
    session.commit()
    return Response(response='User was deleted.')


@user.route("/", methods=['GET'])
def get_list_authors():
    users = session.query(Users).all()
    users_schema = UserInfo(many=True)
    result = users_schema.dump(users)
    return {"Users": result}



@user.route("/<int:user_id>", methods=['GET'])
def get_authors(user_id):
    db_user = session.query(Users).filter_by(id=user_id).first()
    if not db_user:
        return Response(status=404, response='An user with provided ID was not found.')
    notes = session.query(Notes).filter_by(owner_id=user_id).all()
    user_info = UserInfo().dump(db_user)
    notes_info = NoteCreate().dump(notes, many=True)

    return {"UserInfo": user_info, "UserNotes":notes_info}



    