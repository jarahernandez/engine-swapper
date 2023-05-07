from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    data = {
        'id': session['user_id']
    }
    return render_template('success.html', logged_user=user.User.get_user_by_id(data))

@app.route('/signup', methods=['POST'])
def register_user():
    if not user.User.validate_signup(request.form):
        return redirect('/')
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    }
    session['user_id'] = user.User.add_user(data)
    return redirect('/success')

@app.route('/login', methods=['POST'])
def log_user_in():
    is_user_found = user.User.validate_login(request.form)
    if not is_user_found:
        return redirect('/')
    session['user_id'] = is_user_found.id
    return redirect('/success')