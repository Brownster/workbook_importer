from flask import Flask, request, send_from_directory, render_template, make_response
from werkzeug.utils import secure_filename
import os
import importer
from urllib.parse import quote as url_quote

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
            return render_template('index.html', error='No file part in the request'), 400
        file = request.files['file']
        # if the user does not select a file, the browser also submits an empty part without a filename
        if file.filename == '':
            return render_template('index.html', error='No selected file'), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # process the file
            output_filename = filename.rsplit('.', 1)[0] + '.csv'
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            try:
                importer.yaml_to_csv(filepath, output_filepath)
                os.remove(filepath)  # Clean up the original file
                
                success_message = f'''
                <div class="success-message">
                    <h2>Conversion Complete!</h2>
                    <p>Your file has been successfully converted to CSV format.</p>
                    <a href="/uploads/{output_filename}" class="download-button">Download {output_filename}</a>
                    <p class="info-text">You can also upload another file for conversion.</p>
                </div>
                '''
                return render_template('index.html', success_html=success_message)
            except Exception as e:
                return render_template('index.html', error=f"Error processing file: {str(e)}"), 500
                
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/template')
def download_template():
    """Provide a sample YAML template file for users to download"""
    template_yaml = """# Sample Prometheus Exporter Configuration Template
# This template shows the required structure for Workbook Importer

# OS Exporter Examples (linux, windows, verint, vmware, aacc)
exporter_linux:
  server1.example.com:
    location: "New York"
    country: "USA"
    environment: "production"
    ip_address: "192.168.1.10"
    listen_port: "9100"
    username: "prometheus"
    password: "encrypted_password_here"

exporter_windows:
  winserv01.example.com:
    location: "London"
    country: "UK"
    environment: "development"
    ip_address: "192.168.2.20"
    listen_port: "9182"

# App Exporter Examples (cms, avayasbc, aes, etc.)
exporter_cms:
  app1.example.com:
    location: "Singapore"
    country: "Singapore"
    environment: "staging"
    ip_address: "192.168.3.30"
    listen_port: "9113"

# Blackbox Exporter Example
exporter_blackbox:
  monitor.example.com:
    10.0.0.1:
      module: "icmp"
      location: "Tokyo"
      country: "Japan"
      environment: "production"
    10.0.0.2:
      module: "tcp_connect"
      location: "Tokyo" 
      country: "Japan"
      environment: "production"
    10.0.0.3:
      module: "ssh_banner"
      location: "Tokyo"
      country: "Japan" 
      environment: "production"
    10.0.0.4:
      module: "http_2xx"
      location: "Tokyo"
      country: "Japan"
      environment: "production"

# SSL Certificate Exporter Example
exporter_ssl:
  secure.example.com:
    ip_address: "192.168.4.40"
    location: "Berlin"
    country: "Germany"
    environment: "production"
"""
    response = make_response(template_yaml)
    response.headers["Content-Disposition"] = "attachment; filename=template.yaml"
    response.headers["Content-Type"] = "application/x-yaml"
    return response

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5001)
