from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'kritika123'


# index (home page)
@app.route("/")
def index():

    # if logged in 
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    
    # not logged in 
    else:
        return render_template("index.html")

# login 
@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == "POST":
        session['username'] = request.form.get('username')
        return redirect(url_for('index'))
    
# logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()