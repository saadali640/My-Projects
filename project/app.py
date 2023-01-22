import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from flask_session import Session
from cs50 import SQL
from functools import wraps


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():
    home = True
    user_id = session["user_id"]
    posts = db.execute("select id, postimg, posttxt, date, likes, user_username, user_id from posts where user_id != ? order by id desc", user_id)
    return render_template("index.html", posts = posts, home = home)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
     user_id = session["user_id"]
     user = db.execute("select username from users where id = ?", user_id)
     username = user[0]["username"]
     bio0 = db.execute("select bio from users where id = ?", user_id)
     bio = bio0[0]["bio"]
     urlp0 = db.execute("select profilepic from users where id = ?", user_id)
     urlp = urlp0[0]["profilepic"]
     urlb0 = db.execute("select background from users where id = ?", user_id)
     urlb = urlb0[0]["background"]
     postdata = db.execute("select id, postimg, posttxt, date, likes from posts where user_id = ? order by id desc", user_id)


     if bio == None:
        bio = "No Bio"
     edit = False
     notedit = True
     newpost = False
     post = True

     if request.method == "GET":
       return render_template("profile.html",
       user = username, edit = edit, notedit = notedit, bio = bio, urlp = urlp, urlb = urlb,
       newpost = newpost, post = post, postdata = postdata)

     if request.method == "POST":
        if request.form.get("submit") == ("Edit Profile"):
          edit = True
          notedit = False
        else:
            newpost = True
            post = False
        return render_template("profile.html",
        user = username, edit = edit, notedit = notedit, bio = bio, urlp = urlp, urlb = urlb,
        newpost = newpost, post = post, postdata = postdata)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    user_id = session["user_id"]
    if request.method == "POST":
        bio = request.form.get("bio")
        pic = request.form.get("urlp")
        background = request.form.get("urlb")
        db.execute("UPDATE users SET bio = ? WHERE id = ?", bio, user_id)
        db.execute("UPDATE users SET profilepic = ? WHERE id = ?", pic, user_id)
        db.execute("UPDATE users SET background = ? WHERE id = ?", background, user_id)

        flash("Profile Updated")
        return redirect("/profile")


@app.route("/newpost", methods=["GET", "POST"])
@login_required
def newpost():
    user_id = session["user_id"]
    if request.method == "POST":
        postimg = request.form.get("postimg")
        posttxt = request.form.get("posttxt")
        name = db.execute("select username from users where id = ?", user_id)
        username = name[0]["username"]
        db.execute("insert into posts (user_id, postimg, posttxt, user_username) values (?,?,?,?)", user_id, postimg, posttxt, username)

        flash("Posted")
        return redirect("/profile")




@app.route("/oup/<int:id>", methods=["GET", "POST"])
@login_required
def oup(id):
     current_user = session["user_id"]
     user_id = id
     user = db.execute("select username from users where id = ?", user_id)
     username = user[0]["username"]
     bio0 = db.execute("select bio from users where id = ?", user_id)
     bio = bio0[0]["bio"]
     urlp0 = db.execute("select profilepic from users where id = ?", user_id)
     urlp = urlp0[0]["profilepic"]
     urlb0 = db.execute("select background from users where id = ?", user_id)
     urlb = urlb0[0]["background"]
     postdata = db.execute("select id, postimg, posttxt, date, likes, user_username, user_id from posts where user_id = ? order by id desc", user_id)


     if bio == None:
        bio = "No Bio"

     if request.method == "GET":
        if user_id == current_user:
            return redirect("/profile")
        else:
            return render_template("oup.html", bio = bio, urlp = urlp, urlb = urlb, postdata = postdata, user = username)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_input = request.form.get("search")
        results = db.execute("select username, id, profilepic from users where username like ? ", search_input)
        home = False
        return render_template("index.html", home = home, results = results)


@app.route("/comment/<int:id>", methods=["GET", "POST"])
def comment(id):
    user_id = session["user_id"]
    name = db.execute("select username from users where id = ?", user_id)
    username = name[0]["username"]
    postID = id
    comment = request.form.get("comment")
    if request.method == "POST":
        db.execute("insert into comments (user_id, post_id, comment, user_username) values (?,?,?,?)", user_id, postID, comment, username)
        row = db.execute("select * from posts where id = ?", id)
        comments = db.execute("select * from comments where post_id = ? group by id", postID)
        return redirect(url_for('view', id=postID))


@app.route("/view/<int:id>", methods=["GET", "POST"])
def view(id):
    if request.method == "GET":
        user_id = session["user_id"]
        liked = True
        postId = id
        row = db.execute("select * from posts where id = ?", id)
        comments = db.execute("select * from comments where post_id = ? group by id", postId)
        user0 = db.execute("select user_id from posts where id = ?", postId)
        user = user0[0]["user_id"]
        userpic0 = db.execute("select profilepic from users where id = ?", user)
        userpic = userpic0[0]["profilepic"]
        L = db.execute("select user_id from liked where post_id = ? and user_id = ?", postId, user_id)
        try:
          LL = L[0]["user_id"]
        except:
          liked = False
        return render_template("view.html", db = row, comments = comments, liked = liked, userpic = userpic)



@app.route("/add/<int:id>", methods=["GET", "POST"])
def add(id):
    if request.method == "GET":
        postID = id
        user_id = session["user_id"]
        db.execute("insert into liked (post_id, user_id) values (?,?)", postID, user_id)
        likes = db.execute("select likes from posts where id = ?", postID)
        likesNum = likes[0]["likes"] + 1

        db.execute("update posts set likes = ? where id = ?", likesNum, postID)
        return redirect(url_for('view', id=postID))

@app.route("/remove/<int:id>", methods=["GET", "POST"])
def remove(id):
    if request.method == "GET":
        postID = id
        user_id = session["user_id"]
        db.execute("delete from liked where post_id = ? and user_id = ?", postID, user_id)
        likes = db.execute("select likes from posts where id = ?", postID)
        likesNum = likes[0]["likes"] - 1

        db.execute("update posts set likes = ? where id = ?", likesNum, postID)
        return redirect(url_for('view', id=postID))



@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            flash("Must Provide Username")
            return render_template("login.html")


        elif not request.form.get("password"):
            flash("Must Provide Password")
            return render_template("login.html")


        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))



        if len(rows) != 1 or not rows[0]["username"]:
            flash("Username Does Not Exist")
            return render_template("login.html")

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid Password")
            return render_template("login.html")


        session["user_id"] = rows[0]["id"]


        return redirect("/")


    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""


    session.clear()


    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method =="GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            flash("Please Type In Your Username")
            return render_template("register.html")
        if not password:
            flash("Please Inter Password")
            return render_template("register.html")
        if not confirmation:
            flash("Please Confirm Password")
            return render_template("register.html")
        if password != confirmation:
            flash("Password Does Not Match")
            return render_template("register.html")

        hash = generate_password_hash(password)

        date = datetime.datetime.now()

        try:
            new_user = db.execute("INSERT INTO users (username, hash, date) VALUES (?, ?, ?)", username, hash, date)

        except:

            flash("Usename Already Exists")
            return render_template("register.html")

        session["user_id"] = new_user
        return render_template("index.html")
