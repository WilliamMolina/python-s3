import os
from flask import Flask, flash, request, jsonify, abort
from werkzeug.utils import secure_filename
import boto3

UPLOAD_FOLDER = '/projects/content-classifier'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', '.mp4', '.avi'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''<form method=POST enctype=multipart/form-data action="upload">
    <input type=file name=myfile>
    <input type=submit>
    </form>'''

@app.route('/upload', methods=['POST'])
def upload():
    ## S3 connection
    session = boto3.Session(
        aws_access_key_id="ACCESS_KEY_ID",
        aws_secret_access_key="SECRET_ACCESS_KEY",
    )
    s3 = session.resource('s3')
    s3.Bucket('YOUR_BUCKET_NAME').put_object(Key=secure_filename(request.files['myfile'].filename), Body=request.files['myfile'])
    return '<h1>File saved to S3</h1>'
        
if __name__ == '__main__':
   app.run(debug = True, port='5002', host='0.0.0.0')