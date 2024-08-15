from flask import Flask, request, redirect, url_for
import os



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.' 
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload CSV File</title>
    <h1>Upload CSV File</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.csv')
        file.save(file_path)
        return redirect(url_for('index'))
    return redirect(request.url)

def run_app():
    app.run(host='0.0.0.0', port=8062)
