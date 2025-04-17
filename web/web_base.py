from flask import Flask, request, redirect, render_template, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

UPLOAD_FOLDER= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Select file!')
        return redirect(url_for('upload-form'))
    file = request.files['file']
    username = request.form['username']
    password = request.form['password']

    print(f'File:{file.filename}, Username:{username}, Password:{password}')

    if file.filename == '':
        flash('There\'s no file!')
        return redirect(url_for('upload_form'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        flash(f"File:{file.filename}, upload successfully")
        return redirect(url_for('upload_form'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)