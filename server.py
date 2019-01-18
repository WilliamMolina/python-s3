import os
from flask import Flask, flash, request, jsonify, abort
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/projects/content-classifier'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', '.mp4', '.avi'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(400,'No file part.')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            abort(400, 'No file selected.')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response = {'status': 'OK','message': 'File has been uploaded.'}
            return jsonify(response)
    else:
        response = {'status': 'OK','message': 'It works!.'}
        return jsonify(response)
        
if __name__ == '__main__':
   app.run(debug = True, port='5002', host='0.0.0.0')