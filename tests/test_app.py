import os
import pytest
from app import app
from flask import url_for
from werkzeug.datastructures import Headers
import time 
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'TEST'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_search(client):
    rv = client.get('/search')
    assert rv.status_code == 200

def test_erreur404(client):
    rv = client.get()
    print(rv.status_code)
    assert rv.status_code == 200

def test_recherche(client):
    rv = client.post('/search', data= {'search': '56200'})
    assert rv.status_code == 200

def test_recherche(client):
    rv = client.post('/search', data= {'search': 'bob'})
    assert rv.status == "200 OK"
    d =Headers()
    d.add('Content-Type', 'text/html; charset=utf-8')
    d.add('Content-Length', '3155')
    assert rv.headers == d
