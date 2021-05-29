from flask import Flask, render_template, request, redirect, url_for
import os
from src.utils.solutionutils import get_solution_dir

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
    app.run(port=5000, host='0.0.0.0')
