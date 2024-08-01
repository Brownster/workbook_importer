# Workbook Importer

The Workbook Importer is a Flask-based web application designed to facilitate the conversion of YAML files into CSV format. This tool is particularly useful for users who need to transform YAML configuration files into a more universally readable format, such as CSV.

## Features

- **File Upload Interface**: Simple web interface to upload YAML files.
- **File Conversion**: Automatic conversion of YAML to CSV.
- **File Download**: Direct download link for the converted CSV file.

![image](https://github.com/user-attachments/assets/854844e8-a318-4443-8bd5-e2f2f9fe5d5e)

## Supported Prometheus Exporters

Supported OS Exporters

    exporter_linux
    exporter_windows
    exporter_verint
    exporter_vmware

Supported App Exporters

    exporter_cms
    exporter_avayasbc
    exporter_aes
    exporter_verint
    exporter_gateway
    exporter_breeze
    exporter_sm
    exporter_acm
    exporter_jmx
    exporter_kafka
    exporter_callback
    exporter_drac
    exporter_genesyscloud
    exporter_tcti
    exporter_aaep
    exporter_pfsense
    exporter_aic
    exporter_zookeeper
    exporter_aam
    exporter_ipoffice
    exporter_iq
    exporter_oceanamonitor
    exporter_ams
    exporter_pc5
    exporter_wfodb
    exporter_nuancelm
    exporter_baas
    exporter_redis
    exporter_mpp
    exporter_network
    exporter_weblm
    exporter_audiocodesbc
    exporter_voice_portal

## Installation

To get started with the Workbook Importer, follow these steps:

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/Brownster/workbook_importer.git
cd workbook_importer

Install Dependencies

bash

pip install -r requirements.txt

Running the Application

bash

python app.py

This will start the Flask server on http://localhost:5001, where you can access the web interface to upload YAML files.
Usage

    Access the Web Interface:
        Open your web browser and navigate to http://localhost:5001.

    Upload a YAML File:
        Click the 'Choose File' button and select the YAML file you wish to convert.
        Click 'Upload and Convert to CSV' to start the conversion.

    Download the CSV File:
        After the file is processed, a download link will appear. Click the link to download the converted CSV file.

Contributing

Contributions to the Workbook Importer are welcome! If you have suggestions for improvements or encounter any issues, please open an issue or submit a pull request.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgements

    Flask framework for making this possible.
    YAML for Python for providing an excellent parsing tool.

Thank you for using or contributing to Workbook Importer!
