import pytest
from to_test.app import app
from to_test.pages.user import session, Session
from to_test.model_objects import Users, Tags, Notes
from to_test import model_objects
from to_test.model_objects import engine


@pytest.fixture(scope='function')
def wrapper(request):
    Session().close()
    model_objects.BaseModel.metadata.drop_all(engine)
    model_objects.BaseModel.metadata.create_all(engine)


@pytest.fixture
def userInfo():
    userInfoP = {
        "username": "new5",
        "email": "new5@gmail.com",
        "password": "12345678",
        "first_name": "new5",
        "last_name": "new5"
    }
    return userInfoP


@pytest.fixture
def userInfo2():
    userInfoP = {
        "username": "new6",
        "email": "new6@gmail.com",
        "password": "123456789",
        "first_name": "new6",
        "last_name": "new6"
    }
    return userInfoP


class TestUser:
    def test_user_create(self, wrapper, userInfo):
        response = app.test_client().post('/user/', json=userInfo)
        assert response.status_code == 200
        assert response.data == b"New user was successfully created!"

    def test_user_create_invalid(self, wrapper, userInfo):
        userInfo["email"] = "dsghsfgkjfgjksk52646835ghdhdk"
        response = app.test_client().post('/user/', json=userInfo)
        assert response.status_code == 400
        assert response.json == {"email": ["Not a valid email address."]}

    def test_user_create_username_used(self, wrapper, userInfo, userInfo2):
        userInfo2["username"] = "new5"
        app.test_client().post('/user/', json=userInfo)
        response = app.test_client().post('/user/', json=userInfo2)
        assert response.status_code == 400
        assert response.data == b'The username is used by other user'

    def test_user_create_email_used(self, wrapper, userInfo, userInfo2):
        userInfo2["email"] = "new5@gmail.com"
        app.test_client().post('/user/', json=userInfo)
        response = app.test_client().post('/user/', json=userInfo2)
        assert response.status_code == 400
        assert response.data == b'The email is used by other user'

    def test_user_update(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().put(f'/user/{new_user.id}', json={
                                                                        "username": "new8",
                                                                        "email": "new8@gmail.com",
                                                                        "password": "12345678910",
                                                                        "first_name": "new8",
                                                                        "last_name": "new8"
                                                                        },
                                         headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.data == b"The user was successfully updated"

    def test_user_update_invalid(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().put(f'/user/{new_user.id}', json={"email": "hdfsdhkjkjhegioiuorjss43k4wtoeuuehy"},
                                         headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.json == {"email": ["Not a valid email address."]}

    def test_user_update_user_not_found(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().put(f'/user/5', json={"email": "max2@gmail.com"},
                                         headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404
        assert response.data == b'An user with provided ID was not found.'

    def test_user_update_username_used(self, wrapper, userInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo2)
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().put(f'/user/{new_user.id}', json={
                                                                        "username": "new6",
                                                                        "email": "new8@gmail.com",
                                                                        "password": "12345678910",
                                                                        "first_name": "new8",
                                                                        "last_name": "new8"
                                                                        },
                                         headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.data == b'User with such username already exists.'

    def test_user_update_email_used(self, wrapper, userInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo2)
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().put(f'/user/{new_user.id}', json={
                                                                        "username": "new8",
                                                                        "email": "new6@gmail.com",
                                                                        "password": "12345678910",
                                                                        "first_name": "new8",
                                                                        "last_name": "new8"
                                                                        },
                                         headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.data == b'User with such email already exists.'

    def test_user_logout(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().post(f'/user/logout', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.json == {'message': 'Logged out'}

    def test_user_update_with_another_user(self, wrapper, userInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo)
        app.test_client().post('/user/', json=userInfo2)

        new_user1 = session.query(Users).filter(Users.username == userInfo["username"]).first()
        new_user2 = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user1.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().put(f'/user/{new_user2.id}', json={"email": "max2@gmail.com"},
                                         headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 403
        assert response.data == b"You are not this user"

    def test_user_delete(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().delete(f'/user/{new_user.id}', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.data == b"User was deleted."

    def test_user_delete_not_found(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().delete(f'/user/8', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404
        assert response.data == b'An user with provided ID was not found.'

    def test_user_delete_with_another_user(self, wrapper, userInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo)
        app.test_client().post('/user/', json=userInfo2)

        new_user1 = session.query(Users).filter(Users.username == userInfo["username"]).first()
        new_user2 = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user1.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().delete(f'/user/{new_user2.id}', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 403
        assert response.data == b"You are not this user"

    def test_user_login(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        assert resp.status_code == 200
        assert token is not None

    def test_user_login_invalid(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "1234"})

        assert resp.status_code == 400
        assert resp.json == {"message": "Incorrect password"}

    def test_user_login_not_found(self, wrapper, userInfo):
        resp = app.test_client().post('/user/login', json={"username": "dhsgfjgsj", "password": "1234"})

        assert resp.status_code == 404
        assert resp.json == {"message": "User not found"}

    def test_user_login_invalid_username(self, wrapper, userInfo):
        resp = app.test_client().post('/user/login', json={"username": ["dhsgfjgsj", "dhsgfjgsj"], "password": "1234"})

        assert resp.status_code == 400
        assert resp.json == {'username': ['Not a valid string.']}

    def test_user_get_id(self, wrapper, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().get(f'/user/{new_user.id}', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        ui = response.json["UserInfo"]
        ut = response.json["UserNotes"]
        assert ut == []
        assert ui["email"] == "new6@gmail.com"
        assert ui["first_name"] == "new6"
        assert ui["id"] == 1
        assert ui["last_name"] == "new6"
        assert ui["numOfEditingNotes"] == 0
        assert ui["numOfNotes"] == 0
        assert ui["username"] == "new6"

    def test_user_get_id_not_found(self, wrapper, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().get(f'/user/9', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404
        assert response.data == b'An user with provided ID was not found.'

    def test_user_get_me(self, wrapper, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().get('/user/me', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        ui = response.json["UserInfo"]
        ut = response.json["UserNotes"]
        assert ut == []
        assert ui["email"] == "new5@gmail.com"
        assert ui["first_name"] == "new5"
        assert ui["id"] == 1
        assert ui["last_name"] == "new5"
        assert ui["numOfEditingNotes"] == 0
        assert ui["numOfNotes"] == 0
        assert ui["username"] == "new5"

    def test_user_get_list(self, wrapper, userInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo)
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().get('/user/', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200

        ui1 = response.json["Users"][0]

        ui2 = response.json["Users"][1]

        assert ui1["email"] == "new5@gmail.com"
        assert ui1["first_name"] == "new5"
        assert ui1["id"] == 1
        assert ui1["last_name"] == "new5"
        assert ui1["numOfEditingNotes"] == 0
        assert ui1["numOfNotes"] == 0
        assert ui1["username"] == "new5"

        assert ui2["email"] == "new6@gmail.com"
        assert ui2["first_name"] == "new6"
        assert ui2["id"] == 2
        assert ui2["last_name"] == "new6"
        assert ui2["numOfEditingNotes"] == 0
        assert ui2["numOfNotes"] == 0
        assert ui2["username"] == "new6"


@pytest.fixture
def tagInfo():
    tagInfoP = {
        "name": "new"
    }
    return tagInfoP


@pytest.fixture
def tagInfo2():
    tagInfoP = {
        "name": "new2"
    }
    return tagInfoP


class TestTag:
    def test_tag_create_unauthorized(self, wrapper, tagInfo):
        response = app.test_client().post('/tag/', json=tagInfo)
        assert response.status_code == 401
        assert response.json == {"msg": "Missing Authorization Header"}

    def test_tag_create(self, wrapper, tagInfo, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.data == b"New tag was successfully created!"

    def test_tag_create_name_used(self, wrapper, tagInfo, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})
        response = app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 400
        assert response.data == b'Tag with such name already exists.'

    def test_tag_create_invalid_name(self, wrapper, tagInfo, userInfo):
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "12345678"})
        token = resp.json['token']

        tagInfo["name"] = ["dfsd", "sdfsd"]

        response = app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 400
        assert response.json == {"name":["Not a valid string."]}

    def test_tag_get_id(self, wrapper, tagInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        new_tag = session.query(Tags).filter(Tags.name == tagInfo["name"]).first()

        response = app.test_client().get(f'/tag/{new_tag.id}', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json == {'id': 1, 'name': 'new'}

    def test_tag_get_id_not_found(self, wrapper, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().get(f'/tag/8', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404
        assert response.data == b'An tag with provided ID was not found.'

    def test_tag_update(self, wrapper, tagInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        new_tag = session.query(Tags).filter(Tags.name == tagInfo["name"]).first()

        response = app.test_client().put(f'/tag/{new_tag.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={"name": "something"})

        assert response.status_code == 200
        assert response.data == b'The tag was successfully updated'

    def test_tag_update_invalid(self, wrapper, tagInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        new_tag = session.query(Tags).filter(Tags.name == tagInfo["name"]).first()

        response = app.test_client().put(f'/tag/{new_tag.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={"name": ["something", "jgdfh"]})

        assert response.status_code == 400
        assert response.json == {'name': ['Not a valid string.']}

    def test_tag_update_name_used(self, wrapper, tagInfo, tagInfo2, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})
        app.test_client().post('/tag/', json=tagInfo2, headers={"Authorization": f"Bearer {token}"})

        new_tag = session.query(Tags).filter(Tags.name == tagInfo["name"]).first()

        response = app.test_client().put(f'/tag/{new_tag.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={"name": "new2"})

        assert response.status_code == 400
        assert response.data == b'Tag with such name already exists.'

    def test_tag_update_not_found(self, wrapper, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().put(f'/tag/8', headers={"Authorization": f"Bearer {token}"},
                                         json={"name": "new2"})

        assert response.status_code == 404
        assert response.data == b'An tag with provided ID was not found.'

    def test_tag_delete(self, wrapper, tagInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        new_tag = session.query(Tags).filter(Tags.name == tagInfo["name"]).first()

        response = app.test_client().delete(f'/tag/{new_tag.id}', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.data == b'Tag was deleted.'

    def test_tag_delete_not_found(self, wrapper, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().delete(f'/tag/25', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404
        assert response.data == b'An tag with provided ID was not found.'


@pytest.fixture
def noteInfo():
    noteInfoP = {
        "title": "MyNote",
        "isPublic": "True",
        "text": "My new title",
        "tags": [
            {
                "name": "new"
            }
        ]
    }
    return noteInfoP


class TestNote:
    def test_note_create(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        response = app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.data == b'Note was added successfully'

    def test_note_create_title_used(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})
        response = app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.data == b'This title has already exist.'

    def test_note_create_tag_not_found(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.json == {"message": "Tag could not be found."}

    def test_note_create_tag_doubled(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        noteInfo["tags"] = [
            {
                "name": "new"
            },
            {
                "name": "new"
            }
        ]

        response = app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.json == {"message": "Can't use the same tag again"}

    def test_note_create_invalid(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        noteInfo["title"] = [
            {
                "name": "new"
            }
        ]

        response = app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 400
        assert response.json == {'title': ['Not a valid string.']}

    def test_note_update(self, wrapper, noteInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/tag/', json=tagInfo2, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().put(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                                "title": "MyNote2",
                                                "isPublic": "False",
                                                "text": "My new titless",
                                                "tags": [
                                                    {
                                                        "name": "new2"
                                                    }
                                                ]
                                            })

        assert response.status_code == 200
        assert response.data == b'Note was updated successfully'

    def test_note_update_tag_used(self, wrapper, noteInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().put(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                                "title": "MyNote2",
                                                "isPublic": "False",
                                                "text": "My new titless",
                                                "tags": [
                                                    {
                                                        "name": "new"
                                                    }
                                                ]
                                            })

        assert response.status_code == 400
        assert response.json == {"message": "Can\'t use the same tag again"}

    def test_note_update_tag_doubled(self, wrapper, noteInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/tag/', json=tagInfo2, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().put(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                                "title": "MyNote2",
                                                "isPublic": "False",
                                                "text": "My new titless",
                                                "tags": [
                                                    {
                                                        "name": "new2"
                                                    },
                                                    {
                                                        "name": "new2"
                                                    }
                                                ]
                                            })

        assert response.status_code == 400
        assert response.json == {"message": "Can\'t use the same tag again"}

    def test_note_update_tag_not_found(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().put(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                                "title": "MyNote2",
                                                "isPublic": "False",
                                                "text": "My new titless",
                                                "tags": [
                                                    {
                                                        "name": "new2"
                                                    }
                                                ]
                                            })

        assert response.status_code == 404
        assert response.json == {"message":"Tag could not be found."}

    def test_note_update_not_found(self, wrapper, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().put(f'/note/12', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                                "title": "MyNote2",
                                                "isPublic": "False",
                                                "text": "My new titless",
                                                "tags": [
                                                    {
                                                        "name": "new2"
                                                    }
                                                ]
                                            })

        assert response.status_code == 404
        assert response.data == b'An Note with provided ID was not found.'

    def test_note_update_not_allowed(self, wrapper, noteInfo, userInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        noteInfo["isPublic"] = False

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        new_user1 = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user1.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().put(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                                "title": "MyNote2",
                                                "isPublic": "False",
                                                "text": "My new titless",
                                                "tags": [
                                                    {
                                                        "name": "new2"
                                                    }
                                                ]
                                            })

        assert response.status_code == 403
        assert response.data == b'You`re not allowed.'

    def test_note_update_title_used(self, wrapper, noteInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/tag/', json=tagInfo2, headers={"Authorization": f"Bearer {token}"})

        noteInfo["title"] = 'MyNote3'
        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().put(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                                "title": "MyNote3",
                                                "isPublic": "False",
                                                "text": "My new titless",
                                                "tags": [
                                                    {
                                                        "name": "new2"
                                                    }
                                                ]
                                            })

        assert response.status_code == 400
        assert response.data == b'Note with such title already exists.'

    def test_note_update_invalid(self, wrapper, noteInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/tag/', json=tagInfo2, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().put(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"},
                                         json={
                                             "title": "MyNote2",
                                             "isPublic": "False",
                                             "text": "My new titless",
                                             "tags": [
                                                 [{
                                                     "name": "new2"
                                                 }]
                                             ]
                                         })

        assert response.status_code == 400
        assert response.json == {"tags": {"0": {"_schema": ["Invalid input type."]}}}

    def test_note_delete(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().delete(f'/note/{new_note.id}', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.data == b'Note was deleted.'

    def test_note_delete_not_found(self, wrapper, noteInfo, userInfo2, tagInfo):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().delete('/note/55', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404
        assert response.data == b'A note with provided ID was not found.'

    def test_note_delete_not_allowed(self, wrapper, noteInfo, userInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        noteInfo["isPublic"] = False

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        new_user1 = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user1.username, "password": "12345678"})
        token = resp.json['token']

        response = app.test_client().delete(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 403
        assert response.data == b'Methods is not allowed, note isn`t your.'

    def test_note_get_id(self, wrapper, noteInfo, tagInfo, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().get(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json == {'note': {'dateOfEditing': None,
                                          'editors': [],
                                          'id': 1,
                                          'isPublic': True,
                                          'owner_id': 1,
                                          'tags': [{'name': 'new'}],
                                          'text': 'My new title',
                                          'title': 'MyNote'}}

    def test_note_get_id_not_found(self, wrapper, userInfo2):
        app.test_client().post('/user/', json=userInfo2)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        response = app.test_client().get(f'/note/8', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404
        assert response.data == b'An Note with provided ID was not found.'

    def test_note_get_id_not_allowed(self, wrapper, noteInfo, tagInfo, userInfo2, userInfo):
        app.test_client().post('/user/', json=userInfo2)
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        noteInfo["isPublic"] = False

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_user1 = session.query(Users).filter(Users.username == userInfo["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user1.username, "password": "12345678"})
        token = resp.json['token']

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().get(f'/note/{new_note.id}', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403
        assert response.data == b'Note is private.'

    def test_note_give_right(self, wrapper, noteInfo, userInfo, userInfo2, tagInfo, tagInfo2):
        app.test_client().post('/user/', json=userInfo2)
        app.test_client().post('/user/', json=userInfo)

        new_user = session.query(Users).filter(Users.username == userInfo2["username"]).first()

        resp = app.test_client().post('/user/login', json={"username": new_user.username, "password": "123456789"})
        token = resp.json['token']

        app.test_client().post('/tag/', json=tagInfo, headers={"Authorization": f"Bearer {token}"})

        noteInfo["isPublic"] = False

        app.test_client().post('/note/', json=noteInfo, headers={"Authorization": f"Bearer {token}"})

        new_user1 = session.query(Users).filter(Users.username == userInfo["username"]).first()

        new_note = session.query(Notes).filter(Notes.title == noteInfo["title"]).first()

        response = app.test_client().post('/note/allowed', headers={"Authorization": f"Bearer {token}"}, json={
                                                                                                 "user_id": new_user1.id,
                                                                                                 "note_id": new_note.id
                                                                                                 })

        assert response.status_code == 200
        assert response.data == b'New editor was added.'
