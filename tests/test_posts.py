from typing import List
from apps import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate, res.json())
    post_list = list(post_map)
        
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorizes_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/65656556")
    
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

 
@pytest.mark.parametrize("title, content, published", [
    ("1st title", "1st content", True),
    ("2nd title", "2nd content", False),
    ("3rd title", "3rd content", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_unauthorizes_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "hm", "content": "hm"})
    
    assert res.status_code == 401

def test_unauthorizes_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/99999999")
    
    assert res.status_code == 404

def test_delete_others_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json={"title": "Updated title", "content": "Updated content", "id": test_posts[0].id})
    updated_post = schemas.Post(**res.json()["data"])
    
    assert res.status_code == 200

def test_update_post_of_others(authorized_client, test_user, test_user2, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json={"title": "Updated title", "content": "Updated content", "id": test_posts[0].id})
    assert res.status_code == 403

def test_unauthorizes_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401

def test_user_update_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.put("/posts/99999999", json={"title": "Updated title", "content": "Updated content", "id": test_posts[0].id})
    
    assert res.status_code == 404