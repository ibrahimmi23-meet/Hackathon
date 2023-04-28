from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {

  "apiKey": "AIzaSyAA2icBX8XHj5nkIZXvZl0N2xkPur_KVE4",

  "authDomain": "hackathon-5646c.firebaseapp.com",

  "projectId": "hackathon-5646c",

  "storageBucket": "hackathon-5646c.appspot.com",

  "messagingSenderId": "501674961643",

  "appId": "1:501674961643:web:baaea2f16b5bbc5019ecae", "databaseURL": "https://hackathon-5646c-default-rtdb.europe-west1.firebasedatabase.app"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    user = {"email": email, "password": password, "username" : request.form['Username']}
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      db.child('Users').child(login_session['user']['localId']).set(user)
      return render_template("home.html")
    except:
      error = "Authentication failed"
      print (error)
  return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(email, password)
      return render_template("home.html")
    except:
      error = "Authentication failed"
      print (error)
  return render_template("signin.html")


@app.route('/home', methods=['GET', 'POST'])
def home():
  return render_template('home.html')

@app.route("/signout")
def signout():
  login_session['user'] = None
  auth.current_user = None
  return redirect(url_for('signin'))


if __name__ == '__main__':
  app.run(debug=True)
