import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/cash", methods = ["GET", "POST"])
@login_required
def cash():
    """Add Cash"""
    if request.method=="GET":
        return render_template("cash.html")

    else:
        add_cash = int(request.form.get("add_cash"))
        if not add_cash or add_cash < 1:
            flash("Must Provide Cash Amount")
            return render_template("cash.html")

        user_id = session["user_id"]
        user_wallet = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_wallet[0]["cash"]

        update_wallet = user_cash + add_cash

        db.execute("UPDATE users SET Cash = ? WHERE id = ?", update_wallet, user_id)

        flash("Cash Added")
        return render_template("cash.html")




@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    try:
     user_id = session["user_id"]
     symbols = db.execute("SELECT symbol, sum(shares) as shares FROM purchases WHERE user_id = ? GROUP BY symbol having shares > 0", user_id)

     name = []
     total = 0
     for symbol in symbols:
       stock = lookup(symbol["symbol"])
       name.append({
         "symbol": stock["symbol"],
         "nam": stock["name"],
         "price": usd(stock["price"]),
         "shares": symbol["shares"],
         "bill": usd((stock["price"]) * symbol["shares"])
       })
       total += stock["price"] * symbol["shares"]


     user_wallet = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
     user_cash = user_wallet[0]["cash"]

     total += user_cash

     return render_template("index.html", database = name, cash = usd(user_cash), total = usd(total))

    except:
     return render_template("index.html", cash = usd(0), total = usd(0))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
           flash("Please Type Stock Name")
           return apology("Please Type Stock Name")

        stock = lookup(symbol.upper())

        if stock == None:
            flash("Sorry Stock Does Not Exist")
            return apology("Sorry Stock Does Not Exist")

        if not shares:
            flash("Please Inter Amount Of Shares")
            return apology("Please Inter Amount Of Shares")

        if not shares.isdigit() or int(shares) < 1:
            flash("Input Must Be A Positive Number")
            return apology("Input Must Be A Positive Number")


        user_id = session["user_id"]
        user_wallet = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_wallet[0]["cash"]

        bill = int(shares) * stock["price"]

        if user_cash < bill:
            flash("Insuffecient Funds")
            return apology("Insuffecient Funds")

        update_wallet = user_cash - bill

        db.execute("UPDATE users SET Cash = ? WHERE id = ?", update_wallet, user_id)
        date = datetime.datetime.now()

        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, bill, date) VALUES (?, ?, ?, ?, ?, ?)", user_id, stock["symbol"], int(shares), stock["price"], bill, date)

        flash("Bought!")
        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    purchases = db.execute("SELECT symbol, sum(shares) AS shares, price, sum(bill) AS bill, date FROM purchases WHERE user_id = ? GROUP BY id", user_id)

    return render_template("history.html", database = purchases)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must Provide Username", 403)
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must Provide Password", 403)
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct

        if len(rows) != 1 or not rows[0]["username"]:
            flash("Username Does Not Exist", 403)
            return render_template("login.html")

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid Password", 403)
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        stock = lookup(symbol.upper())

        if stock == None:
            flash("Sorry Stock Does Not Exist")
            return apology("Sorry Stock Does Not Exist")

        if not symbol:
           flash("Please Type Symbol")
           return apology("Please Type Symbol")

        return render_template("quoted.html", name = stock["name"], price = usd(stock["price"]), symbol = stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method =="GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            flash("Please Type In Your Username")
            return apology("Please Type In Your Username")
        if not password:
            flash("Please Inter Password")
            return apology("Please Inter Password")
        if not confirmation:
            flash("Please Confirm Password")
            return apology("Please Confirm Password")
        if password != confirmation:
            flash("Password Does Not Match")
            return apology("Password Does Not Match")

        hash = generate_password_hash(password)

        date = datetime.datetime.now()

        try:
            new_user = db.execute("INSERT INTO users (username, hash, date) VALUES (?, ?, ?)", username, hash, date)

        except:

            flash("Usename Already Exists")
            return apology("Usename Already Exists")

        session["user_id"] = new_user
        return render_template("index.html")





@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        userid = session["user_id"]
        symbols=db.execute("select symbol from purchases where user_id=? group by symbol having sum(shares)>0", userid)
        return render_template("sell.html", symbols = [row["symbol"] for row in symbols])

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
           flash("Please Type Stock Name")
           return apology("Please Type Stock Name")

        stock = lookup(symbol.upper())

        if stock == None:
            flash("Sorry Stock Does Not Exist")
            return apology("Sorry Stock Does Not Exist")

        if not shares:
            flash("Please Inter Amount Of Shares")
            return apology("Please Inter Amount Of Shares")

        if int(shares) < 1:
            flash("Input Must Be A Positive Integer")
            return apology("Input Must Be A Positive Integer")

        user_id = session["user_id"]
        user_shares = db.execute("SELECT sum(shares) as shares FROM purchases WHERE user_id = ? AND symbol = ?", user_id, symbol.upper())
        user_sh = user_shares[0]["shares"]
        try:
            sy = db.execute("SELECT symbol FROM purchases WHERE user_id = ? AND symbol = ?", user_id, symbol.upper())
            sym = sy[0]["symbol"]

        except:
            flash("You Do Not Own Any Stocks From This Company")
            return apology("You Do Not Own Any Stocks From This Company")

        user_wallet = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_wallet[0]["cash"]

        if user_sh < 1:
            flash("You Do Not Own Any Stocks From This Company")
            return apology("You Do Not Own Any Stocks From This Company")

        if user_sh < int(shares):
            flash("You Do Not Own That Much Shares")
            return apology("You Do Not Own That Much Shares")

        bill = int(shares) * stock["price"]
        update_wallet = user_cash + bill


        db.execute("UPDATE users SET Cash = ? WHERE id = ?", update_wallet, user_id)
        date = datetime.datetime.now()

        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, bill, date) VALUES (?, ?, ?, ?, ?, ?)", user_id, stock["symbol"], (-1)*int(shares), stock["price"], bill, date)

        flash("Transaction Completed!")
        return redirect("/")


