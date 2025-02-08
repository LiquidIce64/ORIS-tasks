import os
from flask import Flask, render_template

app = Flask("webserver")
app.secret_key = os.environ.get('API_KEY')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
