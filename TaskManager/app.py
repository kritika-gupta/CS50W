import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "kritika123"

# connect to db
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# index (home page)
@app.route("/")
def index():

    # if logged in 
    if "username" in session:
        return render_template("index.html", username=session["username"])
    
    # not logged in 
    else:
        return render_template("index.html")

# login 
@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).fetchone()
        if user is None:
            flash("Username does not exist.", category="error")
            return redirect(url_for('login'))
        if sha256_crypt.verify(password, user.password):
            flash("You were successfully logged in!", category="success")
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Incorrect Password", category="error")
            return redirect(url_for('login'))
            
# logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # create account after user fills form and clicks register button
    if request.method == "POST":
        username = request.form.get("username")
        password = sha256_crypt.encrypt(request.form.get("password"))
        # TODO: validate form entries
        
        try:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username":username, "password":password})

        except exc.IntegrityError:
            #TODO: add specific error handling
            flash("Username already exists.", category='error')
            return redirect(url_for('register'))
        db.commit()
        flash("Account created, you can login now.", category="success")
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()