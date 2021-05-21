from pip._internal.vcs import git

from app import aplication
from app import *
from flask_mobility import Mobility


def test_getUsers():
    with aplication.test_client() as test_client:
        response = test_client.get('/users')
        print(response)
        assert response.status_code == 200


def test_getNotes():
    with aplication.test_client() as test_client:
        response = test_client.get('/note')
        print(response)
        assert response.status_code == 200


def test_getTags():
    with aplication.test_client() as test_client:
        response = test_client.get('/tags')
        print(response)
        assert response.status_code == 200


def test_getHistories():
    with aplication.test_client() as test_client:
        response = test_client.get('/histories')
        print(response)
        assert response.status_code == 200

