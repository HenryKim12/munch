from app import models
from app.extensions import db
from sqlalchemy import func

postData = {
    "username": "test",
    "email": "test@gmail.com",
    "password": "test"
}

def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == models.User.query.count()

def test_get_user_by_id(client):
    user_count = models.User.query.count()
    if user_count == 0:
        postResponse = client.post("/users", json=postData)
        assert postResponse.status_code == 200
    db_user = models.User.query.filter_by(email=postData["email"]).first()
    response = client.get(f"/users/{db_user.to_dict()["id"]}")
    assert response.status_code == 200
    user = response.get_json()
    assert user["username"] == db_user["username"]
    assert user["email"] == db_user["email"]
    assert user["password"] == db_user["password"]
    assert user["restaurants"] == db_user["restaurants"]

def test_get_user_by_missing_id(client):
    response = client.get("/users/0")
    assert response.status_code == 404
    assert response.get_json() == "User does not exist."

def test_delete_user(client):
    existing_user = models.User.query.filter_by(email=postData["email"]).first()
    user_id = None
    if not existing_user:
        postResponse = client.post("/users", json=postData)
        assert postResponse.status_code == 200
        user_id = db.session.get(models.User, db.session.query(func.max(models.User.id)))
    else:
        user_id = existing_user["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    checkUserDeleted = db.session.query(db.exists().where(models.User.email == postData["email"])).scalar()
    assert checkUserDeleted == False

def test_delete_missing_user(client):
    response = client.delete("users/0")
    assert response.status_code == 404
    assert response.get_json() == "User does not exist."

def test_create_new_user(client):
    existing_user = db.session.query(db.exists().where(models.User.username == postData["username"])).scalar()
    if existing_user:
        del_response = client.delete(f"/users/{existing_user.to_dict()["id"]}")
        assert del_response.status_code == 200
    response = client.post("/users", json=postData)
    assert response.status_code == 200
    new_user_id = db.session.query(func.max(models.User.id)).scalar()
    new_user = db.session.get(models.User, new_user_id)
    assert new_user["username"] == postData["username"]

def test_create_existing_username(client):
    existing_user = db.session.query(db.exists().where(models.User.username == postData["username"])).scalar()
    if not existing_user:
        post_response = client.post("/users", json=postData)
        assert post_response.status_code == 200
    response = client.post("/users", json=postData)
    assert response.status_code == 409
    assert response.get_json() == "Account with given username/email already exists. Try signing in."

def test_create_existing_email(client):
    existing_user = db.session.query(db.exists().where(models.User.email == postData["email"])).scalar()
    if not existing_user:
        post_response = client.post("/users", json=postData)
        assert post_response.status_code == 200
    response = client.post("/users", json=postData)
    assert response.status_code == 409
    assert response.get_json() == "Account with given username/email already exists. Try signing in."

def test_update_user(client):
    updatedData = {
        "username": "test1",
        "email": "test1@gmail.com",
        "password": "test1"
    }
    existingUsername = models.User.query.filter_by(username=updatedData["username"]).first()
    if existingUsername:
        del_response = client.delete(f"/users/{existingUsername["id"]}")
        assert del_response.status_code == 200
    existingEmail = models.User.query.filter_by(email=updatedData["email"]).first()
    if existingEmail:
        del_response = client.delete(f"/users/{existingEmail["id"]}")
        assert del_response.status_code == 200

    if models.User.query.count() == 0:
        post_response = client.post("/users", json=postData)
        assert post_response.status_code == 200

    db_user_id = db.session.query(func.max(models.User.id)).scalar()
    response = client.put(f"/users/{db_user_id}", json=updatedData)
    assert response.status_code == 200
    db_user = db.session.get(models.User, db_user_id)
    assert db_user["username"] == updatedData["username"]
    assert db_user["email"] == updatedData["email"]