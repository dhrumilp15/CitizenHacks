import os

from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, url_for
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import time

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['DEBUG'] = True
app.secret_key = "holiday maid indoor dial sword leisure limit spend connect cheese round slot hat"
UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    else:
        return render_template("index.html")
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        print("in post")
        # if not request.form.get("file") or not request.form.get("patient") or not request.form.get("doctor"):
        #     return render_template("sorry.html")

        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        print(request.files)
        filey = request.files['file']
        patient = request.form.get("patient")
        doctor = request.form.get("doctor")
        # if user does not select file, browser also
        # submit an empty part without filename
        if filey.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(filey.filename)
        print("filename: " + filename)
        filey.save(os.path.join(".", filename))
        fileurl = filename
        os.system("keybase fs mv {} /keybase/private/{},{}".format(fileurl, doctor, patient))
        os.system("keybase chat send {},{} 'Your updated files have been added to your shared folder and you should copy them into your private folder.'".format(doctor,patient))
        os.system("rm {}".format(filename))
        return redirect("/")        
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