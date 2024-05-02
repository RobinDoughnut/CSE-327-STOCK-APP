from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# My App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    
with app.app_context():
    db.create_all()


# Index or home
@app.route("/", methods=["POST", "GET"])
def index():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('index.html',user=user)
    
    return redirect('/login')


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == 'POST':
        # handle request
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
        
            if user and user.check_password(password):
                session['email'] = user.email
                return redirect('/index')
            else:
                return render_template('login.html',error='Invalid user')

    return render_template('login.html')


    # Forget any user_id



# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
       # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')


    return render_template('register.html')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop('email', None)
    return redirect('/login')



if __name__ in "__main__":
    app.run(debug=True)
    

