from apps import schemas 
from apps.config import settings
from jose import jwt
import pytest



def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'hello'

def test_login_user(client, test_user):
    res = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize(
        "email, password, status_code",[
            ("wrongemail@gmail.com", "password123", 403),
            ("sanjeev@gmail.com", "wrongpassword", 403),
            ("wrongemail@gmail.com", "wrongpassword", 403),
            (None, "password123", 422),
            ("sanjeev@gmail.com", None, 422),
        ]
)

def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login/", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid email or password"