from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from noteProgect.model_objects import Session, Tags, Users
from noteProgect.validation_schemas import TagInfo
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

tag = Blueprint('tag', __name__, url_prefix="/tag")
bcrypt = Bcrypt()
session = Session()


@tag.route('/', methods=['POST'])
@jwt_required()
def add_tag():
    try:
        tag = TagInfo().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = session.query(Users).filter_by(id=get_jwt_identity()).first()
    if not user:
        return Response(status=404, response='Login please.')
    exists = session.query(Tags.id).filter_by(name=tag['name']).first()
    if exists:
        return Response(status=400, response='Tag with such name already exists.')
    new_tag = Tags(name=tag['name'])
    session.add(new_tag)
    session.commit()

    return Response(response='New tag was successfully created!')


@tag.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tagGet = session.query(Tags).filter_by(id=tag_id).first()
    if not tagGet:
        return Response(status=404, response='An tag with provided ID was not found.')
    return TagInfo().dump(tagGet), 200


@tag.route('/<int:tag_id>', methods=['PUT'])
@jwt_required()
def update_tag(tag_id):
    try:
        data = TagInfo().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = session.query(Users).filter_by(id=get_jwt_identity()).first()
    if not user:
        return Response(status=404, response='Login please')
    db_tag = session.query(Tags).filter_by(id=tag_id).first()
    if not db_tag:
        return Response(status=404, response='An tag with provided ID was not found.')

    exists = session.query(Tags.id).filter_by(name=data['name']).first()
    if exists:
        return Response(status=400, response='Tag with such number already exists.')
    db_tag.name = data['name']
    session.commit()

    return Response(response="The tag was successfully updated")


@tag.route('/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    user = session.query(Users).filter_by(id=get_jwt_identity()).first()
    if not user:
        return Response(status=404, response='Login please')
    db_tag = session.query(Tags).filter_by(id=tag_id).first()
    if not db_tag:
        return Response(status=404, response='An tag with provided ID was not found.')

    session.delete(db_tag)
    session.commit()
    return Response(response='Tag was deleted.')
