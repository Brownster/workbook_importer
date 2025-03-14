# Workbook Importer

The Workbook Importer is a Flask-based web application specifically designed to facilitate the conversion of Puppet YAML hieradata configurations into CSV format. This tool is invaluable for systems administrators and monitoring engineers who manage Prometheus instances. It simplifies the process of transforming complex YAML configuration files, used in Puppet for provisioning monitoring targets, into a universally readable CSV format, making it easier to audit, document, and review configurations.

![image](https://github.com/user-attachments/assets/854844e8-a318-4443-8bd5-e2f2f9fe5d5e)

## Features

- **Intuitive Web Interface**: User-friendly interface to upload YAML files
- **Template Download**: Sample YAML template to help you get started with the correct format
- **Detailed Field Descriptions**: Interactive documentation about CSV output fields
- **Error Handling**: Clear error messages and feedback during conversion
- **Automatic Conversion**: Fast and efficient transformation of YAML hieradata to CSV
- **Instant Download**: Direct download link for the converted CSV file
- **Comprehensive Help**: Built-in documentation about supported exporters and fields

## Supported Prometheus Exporters

### OS Exporters
- exporter_linux
- exporter_windows
- exporter_verint
- exporter_vmware
- exporter_aacc

### App Exporters
- exporter_cms
- exporter_blackbox
- exporter_avayasbc
- exporter_aes
- exporter_aessnmp
- exporter_verint
- exporter_gateway
- exporter_breeze
- exporter_sm
- exporter_acm
- exporter_jmx
- exporter_kafka
- exporter_callback
- exporter_drac
- exporter_genesyscloud
- exporter_tcti
- exporter_aaep
- exporter_pfsense
- exporter_aic
- exporter_zookeeper
- exporter_aam
- exporter_ipoffice
- exporter_iq
- exporter_oceanamonitor
- exporter_ams
- exporter_pc5
- exporter_wfodb
- exporter_nuancelm
- exporter_baas
- exporter_redis
- exporter_mpp
- exporter_network
- exporter_weblm
- exporter_audiocodesbc
- exporter_voiceportal

### Special Exporters
- exporter_ssl (SSL certificate monitoring)
- exporter_blackbox (for ICMP, TCP, HTTP, and SSH banner checks)

## CSV Output Fields

The conversion process creates a CSV file with the following fields:

| Field Name | Description |
|------------|-------------|
| Configuration Item Name | The hostname without domain |
| Location | Physical or logical location of the server |
| Country | Country where the server is located |
| Environment | Deployment environment (prod, dev, test, etc.) |
| Domain | Domain portion of the FQDN |
| Hostnames | Short hostname |
| FQDN | Fully Qualified Domain Name |
| IP Address | IP address of the server |
| Exporter_name_os | Name of the OS-level exporter |
| OS-Listen-Port | Port number for the OS exporter |
| Exporter_name_app | Name of the application exporter |
| App-Listen-Port | Port number for the application exporter |
| Exporter_name_app_2 | Name of second application exporter |
| App-Listen-Port-2 | Port for second application exporter |
| Exporter_name_app_3 | Name of third application exporter |
| App-Listen-Port-3 | Port for third application exporter |
| Exporter_SSL | Flag indicating if SSL exporter is used |
| http_2xx | Flag for HTTP 2xx blackbox checks |
| icmp | Flag for ICMP blackbox checks |
| ssh-banner | Flag for SSH banner blackbox checks |
| tcp-connect | Flag for TCP connection blackbox checks |
| ssh_username | SSH Username if applicable |
| ssh_password | Encrypted SSH Password if applicable |

## Installation

To get started with the Workbook Importer, follow these steps:

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/Brownster/workbook_importer.git
cd workbook_importer
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

This will start the Flask server on http://localhost:5001, where you can access the web interface to upload YAML files.

## Usage

1. **Access the Web Interface**:
   - Open your web browser and navigate to http://localhost:5001

2. **Download the Template** (Optional):
   - Click the "Download Template YAML" button to get a sample file showing the expected format
   - Use this template as a reference for creating your own YAML files

3. **Upload a YAML File**:
   - Click the "Choose File" button and select the YAML file you wish to convert
   - YAML files with extensions .yaml, .yml, or .eyaml are supported
   - Click "Upload and Convert to CSV" to start the conversion

4. **Download the CSV File**:
   - After the file is processed, a success message with a download link will appear
   - Click the link to download the converted CSV file
   - The CSV file will contain all the fields listed in the documentation

## Docker Support

A Dockerfile is included for containerized deployment. To build and run the application in Docker:

```bash
docker build -t workbook-importer .
docker run -p 5001:5001 workbook-importer
```

Then access the application at http://localhost:5001

## Contributing

Contributions to the Workbook Importer are welcome! If you have suggestions for improvements or encounter any issues, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Flask framework for making this possible
- YAML for Python for providing an excellent parsing tool

Thank you for using or contributing to Workbook Importer!
