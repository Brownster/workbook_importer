from flask import Flask, request, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os
import importer

app = Flask(__name__)

# Configure upload settings
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['ALLOWED_EXTENSIONS'] = {'yaml', 'yml', 'eyaml'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part in the request', 400
        file = request.files['file']
        # if the user does not select a file, the browser also submits an empty part without a filename
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # process the file
            output_filename = filename.rsplit('.', 1)[0] + '.csv'
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            importer.yaml_to_csv(filepath, output_filepath)
            os.remove(filepath)
            return '''
            <a href="/uploads/{filename}">Download {filename}</a>
            '''.format(filename=output_filename), 201
    return render_template('index.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5001)
