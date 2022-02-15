from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# our index route will handle rendering our form
@app.route('/')
def default():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_user():
    print("create reuest from is:")
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    data ={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "birthday": request.form["birthday"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    print(f"data for create is:{data}")
    res = User.create(data)
    print(f"res is {res}")
    session["user_id"] = res
    return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    print("login request from is:")
    print(request.form)
    user = User.get_user_email(request.form)
    if not user:
        flash("Invalid Email or Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email or Password","login")
        return redirect('/')
    session['user_id'] = user.id    
    return redirect('/success')


@app.route('/success')
def success():
    if 'user_id' not in session:
        redirect('/reset')
    data = session['user_id']
    user = User.get_user(data)
    all_users = User.get_all()
    print('success result is:')
    print(user)
    print(all_users)
    return render_template('success.html', user = User.get_user(session['user_id']))

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

@app.route("/clean/<int:id>")
def clean(id):
    data = {'id':id}
    User.delete(data)
    return redirect('/')
