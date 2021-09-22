import glob

import yaml
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os

from src.utils.configutils import load_config
from src.utils.solutionutils import get_solution_dir
from src.experiment.experiment import Experiment
import pickle
from shutil import copyfile
from src.utils.castutils import smart_cast

STATIC_FOLDER = f'{get_solution_dir()}/src/static'
TEMPLATE_FOLDER = f'{get_solution_dir()}/src/templates'
app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
db = SQLAlchemy()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(150))

    def __init__(self, login, password):
        self.login = login
        self.password = password


class UserExperiment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(30), db.ForeignKey('user.login'))
    active_experiment = db.Column(db.String(100))

    def __init__(self, login):
        self.login = login
        self.active_experiment = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def test():
    return render_template('index.html')


@app.route('/experiments')
@login_required
def experiments():
    return render_template('experiments.html')


@app.route('/experiment')
@login_required
def experiment():
    user_experiment = UserExperiment.query.filter_by(login=current_user.login).first()
    experiment_name = user_experiment.active_experiment.split('/')[-1]
    experiment_path = user_experiment.active_experiment
    config = load_config(experiment_path)

    data = {}
    data['experiment_name'] = experiment_name
    df_name = None

    # Check if .csv file exists
    if len(glob.glob(f'{experiment_path}/*.csv')) == 1:
        df_name = glob.glob(f'{experiment_path}/*.csv')[0].split('/')[-1]
        data['df_name'] = df_name

    # If .csv file exists, create / load experiment
    if df_name is not None:

        # If there are .pkl file = load
        pkl_path = glob.glob(f'{experiment_path}/*.pkl')
        if len(pkl_path) == 1:
            print("Loading experiment from pickle")
            exp = pickle.load(open(pkl_path[0], "rb"))
        # Else create new Experiment
        else:
            print("Creating new experiment")
            exp = Experiment(f'{experiment_path}/{df_name}', config)
        data['df_html'] = exp.df.df.to_html()
        data['exp'] = exp

        # Catch commands
        command = request.args.get("command")
        if command == 'preprocessing':
            exp.preprocess_data()
        elif command == 'config':
            return render_template('edit_config.html', config=exp.config)
        elif command == 'update_yaml':
            print(config)
            exp.config = config
            exp.df.params = config['dataframe']
        elif command == 'train':
            exp.train()
        elif command == 'optimize':
            exp.train()
            exp.model.optimize()
            name = exp.model.__class__.__name__.lower()
            config[name] = exp.model.params
            with open(f'{experiment_path}/config.yaml', "w") as file:
                yaml.dump(config, file)
        elif command == 'evaluate':
            exp.evaluate()


        # Display predictions
        if exp.df_with_predictions is not None:
            data['eval_html'] = exp.df_with_predictions.to_html()

        # Display scaled data
        if exp.df.df_scaled is not None:
            data['df_scaled_html'] = exp.df.df_scaled.to_html()

        # Save experiment to pickle
        print("Saving experiment to pickle")
        pickle.dump(exp, open(f'{experiment_path}/exp.pkl', "wb"))

    return render_template('experiment.html', data=data)


@app.route('/experiment', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        path = UserExperiment.query.filter_by(login=current_user.login).first().active_experiment
        uploaded_file.save(f'{path}/{uploaded_file.filename}')
    return redirect(url_for('experiment'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')
    user = User.query.filter_by(login=login).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('test'))
    elif not user:
        flash("Wrong username")
        return redirect(url_for('login'))
    else:
        flash("Wrong password")
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    login = request.form.get('login')
    password = request.form.get('password')

    if len(password) < 5:
        flash("Password should be at least 5 characters long")
        return redirect(url_for('signup'))
    if User.query.filter_by(login=login).first():
        flash(f'User {login} already exists')
        return redirect(url_for('signup'))

    # Hash password
    password = generate_password_hash(password)

    # Create user and add to database
    user = User(login, password)
    db.session.add(user)

    # Assign user with None experiment
    user_experiment = UserExperiment(login)
    db.session.add(user_experiment)

    # Commit
    db.session.commit()

    # Create user directory
    create_user_directory(login)

    return redirect(url_for('login'))


def create_user_directory(username):
    os.makedirs(f'{get_solution_dir()}/data/users/{username}')


def get_user_experiments():
    return sorted(os.listdir(f'{get_solution_dir()}/data/users/{current_user.login}'))


@app.route('/create_experiment')
def create_experiment():
    # Generate experiment name
    new_dir_name = f'Experiment{str(len(get_user_experiments()) + 1).zfill(2)}'

    # Generate experiment path & create it
    experiment_dir_path = f'{get_solution_dir()}/data/users/{current_user.login}/{new_dir_name}'
    os.makedirs(experiment_dir_path)

    # Copy basic config.yaml to experiment folder
    copyfile(src=f'{get_solution_dir()}/src/static/config.yaml', dst=f'{experiment_dir_path}/config.yaml')

    return redirect(url_for('experiments'))


@app.route('/set_active_experiment')
def set_active_experiment():
    experiment = request.args.get('name')
    active_experiment_path = f'{get_solution_dir()}/data/users/{current_user.login}/{experiment}'

    user_experiment = UserExperiment.query.filter_by(login=current_user.login).first()
    user_experiment.active_experiment = active_experiment_path
    db.session.commit()

    return redirect(url_for('experiment'))


@app.route('/config', methods=['POST'])
def config_post():
    user_experiment = UserExperiment.query.filter_by(login=current_user.login).first()
    experiment_path = user_experiment.active_experiment
    current_yaml = load_config(experiment_path)

    for item in current_yaml:
        for param in current_yaml[item]:
            print(f'{item}_{param}', request.form.get(f'{item}_{param}'))
            current_yaml[item][param] = smart_cast(request.form.get(f'{item}_{param}'))

    with open(f'{experiment_path}/config.yaml', "w") as file:
        yaml.dump(current_yaml, file)

    return redirect(url_for('experiment', command='update_yaml'))


if __name__ == '__main__':
    app.config['SECRET_KEY'] = "OutU':Mdix!YyTYo|Hi:7+b9<IP[CR"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Functions
    app.jinja_env.globals.update(get_user_experiments=get_user_experiments)
    app.jinja_env.globals.update(get_solution_dir=get_solution_dir)
    app.jinja_env.globals.update(round=round)

    db.init_app(app)
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    db.create_all(app=app)
    app.run(port=5000, host='0.0.0.0')

# TODO parametry optimize dla mlp
# TODO auto ml
