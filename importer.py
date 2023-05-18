from flask import Flask, request, send_file, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os
import csv
import yaml
from tempfile import NamedTemporaryFile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # replace with your own secret key
app.config['UPLOAD_FOLDER'] = '/path/to/upload/folder'  # replace with your desired upload folder path

class ConversionForm(FlaskForm):
    submit = SubmitField('Convert')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = ConversionForm()
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            yaml_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(yaml_file)
            
            csv_data = convert_yaml_to_csv(yaml_file)
            keys = csv_data[0].keys()

            csv_file = NamedTemporaryFile(delete=False, suffix='.csv')
            with open(csv_file.name, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(csv_data)
            return send_file(csv_file.name, as_attachment=True, attachment_filename='converted.csv', mimetype='text/csv')

    return render_template('upload.html', form=form)
    
    
           
    return '''
    <!doctype html>
    <title>Upload YAML File</title>
    <h1>Upload YAML file for conversion to CSV</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <p>{}</p>
        <input type="submit" value="Convert">
    </form>
    '''.format(form.submit())

def create_row(hostname, details, exporter_name_os, exporter_name_app):
    row = {
        'Configuration Item Name': '',
        'Location': details.get('location', ''),
        'Country': details.get('country', ''),
        'Domain': details.get('domain', ''),
        'Status': details.get('status', ''),
        'Secret Server URL': details.get('secret_server_url', ''),
        'Hostnames': details.get('hostnames', ''),
        'FQDN': details.get('fqdn', ''),
        'IP Address': details.get('ip_address', ''),
        'Application Ports': '',
        'Exporter_name_os': exporter_name_os,
        'Done': '',
        'OS-Listen-Port': details.get('listen_port', ''),
        'Exporter_name_app': exporter_name_app,
        'Done': '',
        'App-Listen-Port': details.get('app_listen_port', ''),
        'http_2xx': '',
        'icmp': 'TRUE' if details.get('module') == 'icmp' else '',
        'ssh-banner': 'TRUE' if details.get('module') == 'ssh_banner' else '',
        'tcp-connect': '',
        'SNMP': '',
        'Exporter_SSL': '',
        'Notes': '',
        'Description': '',
        'Story #': '',
        'Completed': '',
        'Review comments': '',
        'MaaS alarm': '',
        'Resolution': '',
        'comm_string': '',
        'ssh_username': details.get('username', ''),
        'ssh_password': details.get('password', ''),
        'jmx_ports': '',
        'snmp_version': '',
        'snmp_user': '',
        'snmp_password': ''
    }
    return row

def handle_exporter(exporter_data, exporter_name_os, exporter_name_app, csv_data):
    for hostname, details in exporter_data.items():
        csv_data.append(create_row(hostname, details, exporter_name_os, exporter_name_app))

def convert_yaml_to_csv(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    csv_data = []

    exporter_data = {
        'exporter_linux': data.get('exporter_linux', {}),
        'exporter_acm': data.get('exporter_acm', {}),
        'exporter_aic': data.get('exporter_aic', {}),
        'exporter_audiocodesbc': data.get('exporter_audiocodesbc', {}),
        'exporter_cms': data.get('exporter_cms', {}),
        'exporter_aaep': data.get('exporter_aaep', {}),
        'exporter_voiceportal': data.get('exporter_voiceportal', {}),
        'exporter_oceanamonitor': data.get('exporter_oceanamonitor', {}),
        'exporter_aes': data.get('exporter_aes', {}),
        'exporter_aam': data.get('exporter_aam', {}),
        'exporter_breeze': data.get('exporter_breeze', {}),
        'exporter_ipo': data.get('exporter_ipo', {}),
        'exporter_iq': data.get('exporter_iq', {}),
        'exporter_blackbox': data.get('exporter_blackbox', {}),
        'exporter_filestat': data.get('exporter_filestat', {}),
        'exporter_gateway': data.get('exporter_gateway', {}),
        'exporter_mpp': data.get('exporter_mpp', {}),
        'exporter_ams': data.get('exporter_ams', {}),
        'exporter_pc5': data.get('exporter_pc5', {}),
        'exporter_avayasbc': data.get('exporter_avayasbc', {}),
        'exporter_sm': data.get('exporter_sm', {}),
        'exporter_weblm': data.get('exporter_weblm', {}),
        'exporter_wfodb': data.get('exporter_wfodb', {}),
        'exporter_jmx': data.get('exporter_jmx', {}),
        'exporter_tcti': data.get('exporter_tcti', {}),
        'exporter_callback': data.get('exporter_callback', {}),
        'exporter_drac': data.get('exporter_drac', {}),
        'exporter_network': data.get('exporter_network', {}),
        'exporter_nuancelm': data.get('exporter_nuancelm', {}),
        'exporter_pfsense': data.get('exporter_pfsense', {}),
        'exporter_ssl': data.get('exporter_ssl', {}),
        'exporter_baas': data.get('exporter_baas', {}),
        'exporter_windows': data.get('exporter_windows', {}),
        'exporter_vmware': data.get('exporter_vmware', {}),
        'exporter_REDIS': data.get('exporter_REDIS', {}),
        'exporter_verint': data.get('exporter_verint', {})
    }

    for exporter, exporter_data in exporter_data.items():
        if exporter == 'exporter_blackbox':
            handle_exporter(exporter_data, 'exporter_blackbox', '', csv_data)
        elif exporter in ['exporter_windows', 'exporter_verint', 'exporter_vmware']:
            handle_exporter(exporter_data, exporter, '', csv_data)
        else:
            handle_exporter(exporter_data, '', exporter, csv_data)

    return csv_data

# Example usage
yaml_file = 'your_yaml_file.yaml'
csv_data = convert_yaml_to_csv(yaml_file)
keys = csv_data[0].keys()

# Writing data to CSV file
with open('exporters.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(csv_data)

print("CSV file generated successfully.")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
