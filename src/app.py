from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
from src.utils.solutionutils import get_solution_dir

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def test():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def loginPost():
    login = request.form.get('login')
    password = request.form.get('password')
    user = User.query.filter_by(login=login).first()
    if user and check_password_hash(user.password, password):
        return redirect(url_for('test'))
    # flash('message')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


# @app.route('/signup', methods=['POST'])
# def signup():
#     return


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(f'{get_solution_dir()}/data/{uploaded_file.filename}')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'sdafddsfdsfsdfdsafdasddad'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    db.create_all(app=app)
    app.run(port=5000, host='0.0.0.0')
