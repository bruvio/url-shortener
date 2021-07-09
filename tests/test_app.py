import sqlite3
import subprocess

from hashids import Hashids
from src.app import app, generate_hasdid, get_query

hashids = Hashids(min_length=16, salt=app.config["SECRET_KEY"])


def test_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.data == b"Hello, bruvio!"


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200


def test_create_hashid():
    subprocess.call(["python", "./src/db.py"])
    conn = sqlite3.connect("./src/database.db")
    conn.row_factory = sqlite3.Row
    url = "https://app.trainingpeaks.com/"
    hasdid = generate_hasdid(url, conn)
    assert len(hasdid) == 16


def test_get_real_url():
    subprocess.call(["python", "./src/db.py"])
    conn = sqlite3.connect("./src/database.db")
    conn.row_factory = sqlite3.Row
    url = "https://app.trainingpeaks.com/"
    hasdid = generate_hasdid(url, conn)
    original_id = hashids.decode(hasdid)
    query_ = get_query()
    conn = sqlite3.connect("./src/database.db")
    conn.row_factory = sqlite3.Row
    original_id = original_id[0]
    url_data = conn.execute(query_, (original_id,)).fetchone()
    original_url = url_data["original_url"]
    assert original_url == url
