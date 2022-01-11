import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for
from hashids import Hashids
from src.utils.queries import get_query, insert_query, update_click_query


def get_db_connection():
    conn = sqlite3.connect("./src/database.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_app():
    return Flask(__name__)


app = create_app()

app.config["SECRET_KEY"] = "l@ll3r0"

hashids = Hashids(min_length=16, salt=app.config["SECRET_KEY"])


def generate_hasdid(url, conn):

    if not url:
        flash("The URL is required!")
        return redirect(url_for("index"))
    query_ = insert_query()
    url_data = conn.execute(query_, (url,))
    conn.commit()
    conn.close()

    url_id = url_data.lastrowid
    return hashids.encode(url_id)


def get_original_url(original_id, conn):
    query_ = get_query()
    url_data = conn.execute(query_, (original_id,)).fetchone()
    original_url = url_data["original_url"]
    clicks = url_data["clicks"]
    query_ = update_click_query()
    conn.execute(query_, (clicks + 1, original_id))

    conn.commit()
    conn.close()
    return original_url


@app.route("/hello")  # test endpoint
def home():
    return "Hello, bruvio!"


@app.route("/", methods=("GET", "POST"))
def index():
    conn = get_db_connection()
    if request.method == "POST":
        url = request.form["url"]

        hashid = generate_hasdid(url, conn)
        short_url = request.host_url + hashid

        return render_template("index.html", short_url=short_url)

    return render_template("index.html")


@app.route("/<id>")
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        original_url = get_original_url(original_id, conn)
        return redirect(original_url)
    else:
        flash("Invalid URL")
        return redirect(url_for("index"))


@app.route("/stats")
def stats():
    conn = get_db_connection()
    db_urls = conn.execute(
        "SELECT id, created, original_url, clicks FROM urls"
    ).fetchall()
    conn.close()

    urls = []
    for url in db_urls:
        url = dict(url)
        url["short_url"] = request.host_url + hashids.encode(url["id"])
        urls.append(url)

    return render_template("stats.html", urls=urls)
