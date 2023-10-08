from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ensures users are logged in first
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session.get('user_id'))
        if session.get("user_id") is None: 
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")



@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == 'POST':

        name = request.form.get('username')
        password = request.form.get('password')

        if not name:
            return 'Please input a username'

        if not password:
            return 'Please input password'

        if name != 'go' and password != 'ans':
            return render_template('login.html')
            
        # Remember which user has logged in
        session["user_id"] = name
            
        return redirect('/')


    # GET
    else:
        return render_template("login.html")



if __name__ == '__main__':
    app.run(debug=True)