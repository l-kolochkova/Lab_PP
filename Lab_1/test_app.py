import base64



import pytest
import tempfile
import os

from app import app


def test_get_users():
    with app.test_client() as test_client:
        response = test_client.get('/users')
        print(response)
        assert response.status_code == 200


def test_get_user():
    with app.test_client() as test_client:
        response = test_client.get('/users/<id>')
        print(response)
        assert response.status_code == 200


def test_update_user():
    with app.test_client() as test_client:
        response = test_client.put('/users/<id>')
        print(response)
        assert response.status_code == 200


def test_delete_user():
    with app.test_client() as test_client:
        response = test_client.delete('/users/<id>')
        print(response)
        assert response.status_code == 200


def test_add_user():
    with app.test_client() as test_client:
        response = test_client.post('/users')
        print(response)
        assert response.status_code == 200


def test_get_note():
    with app.test_client() as test_client:
        response = test_client.get('/note/<id>')
        print(response)
        assert response.status_code == 200


def test_get_notes():
    with app.test_client() as test_client:
        response = test_client.get('/note')
        print(response)
        assert response.status_code == 200


def test_update_note():
    with app.test_client() as test_client:
        response = test_client.put('/note/<id>')
        print(response)
        assert response.status_code == 200


def test_delete_note():
    with app.test_client() as test_client:
        response = test_client.delete('/note/<id>')
        print(response)
        assert response.status_code == 200


def test_add_note():
    with app.test_client() as test_client:
        response = test_client.post('/note')
        print(response)
        assert response.status_code == 200


def test_get_tag():
    with app.test_client() as test_client:
        response = test_client.get('/tags/<id>')
        print(response)
        assert response.status_code == 200


def test_get_tags():
    with app.test_client() as test_client:
        response = test_client.get('/tags')
        assert response.status_code == 200


def test_update_tag():
    with app.test_client() as test_client:
        response = test_client.put('/tags/<id>')
        print(response)
        assert response.status_code == 200


def test_delete_tag():
    with app.test_client() as test_client:
        response = test_client.delete('/tags/<id>')
        print(response)
        assert response.status_code == 200


def test_add_tag():
    with app.test_client() as test_client:
        response = test_client.post('/tags')
        print(response)
        assert response.status_code == 200


def test_get_histories():
    with app.test_client() as test_client:
        response = test_client.get('/history')
        assert response.status_code == 200


def test_get_history():
    with app.test_client() as test_client:
        response = test_client.get('/history/<id>')
        assert response.status_code == 200


def test_add_history():
    with app.test_client() as test_client:
        response = test_client.post('/history/')
        print(response)
        assert response.status_code == 200


def test_delete_history():
    with app.test_client() as test_client:
        response = test_client.delete('/history/<id>')
        print(response)
        assert response.status_code == 200


def test_login():
    with app.test_client() as test_client:
        log = base64.b64encode(b'Oleg:123').decode('utf-8')
        res = test_client.get('/login', headers={'Authorization': 'Basic ' + log})
        assert res.status_code == 200


def test_hello_world():
    with app.test_client() as test_client:
        response = test_client.get('/api/v1/hello-world-/<num_of_variant>')
        print(response)
        assert response.status_code == 200


def test_protected():
    with app.test_client() as test_client:
        response = test_client.get('/protected')
        print(response)
        assert response.status_code == 200


def test_unprotected():
    with app.test_client() as test_client:
        response = test_client.get('/logout')
        print(response)
        assert response.status_code == 200


def test_get_user1():
    with app.test_client() as test_client:
        rv = test_client.get("/users/<100>")
        assert rv.get_json() == {}