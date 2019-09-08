import os

from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import time

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
uploadfolder = '/uploads'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.form.get("stock"):
            return render_template("sorry.html")
        if not request.form.get("shares") and request.form.get("shares") > 0:
            return render_template("sorry.html")
        filero = request.files['file']
        
    else:
        return render_template("index.html")

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        if not request.form.get("stock"):
            return render_template("sorry.html")

        if not request.form.get("shares") and request.form.get("shares") > 0:
            return render_template("sorry.html")
    else:
        return render_template("update.html")
        
@app.route("/history", methods=["GET", "POST"])
def history():
    if request.method == "POST":
        if not request.form.get("stock"):
            return render_template("history.html")

        if not request.form.get("shares") and request.form.get("shares") > 0:
            return render_template("sorry.html")
    else:
        return render_template("history.html")