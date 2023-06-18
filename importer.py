import csv
import yaml
import sys

def create_row(hostname, details, exporter_name_os='', exporter_name_app='', exporter_name_app_ssl='', exporter_name_app_bb=''):
    hostname_parts = hostname.split('.')
    hostname_field = hostname_parts[0]
    domain_field = '.'.join(hostname_parts[1:])

    row = {
        'Configuration Item Name': hostname_field,
        'Location': details.get('location', ''),
        'Country': details.get('country', ''),
        'Domain': domain_field,
        'Hostnames': hostname_field,
        'FQDN': hostname,
        'IP Address': details.get('ip_address', ''),
        'Exporter_name_os': exporter_name_os,
        'OS-Listen-Port': details.get('listen_port', ''),
        'Exporter_name_app': exporter_name_app,
        'App-Listen-Port': details.get('listen_port', ''),
        'Exporter_name_app_2': exporter_name_app,
        'App-Listen-Port-2': details.get('listen_port', ''),
        'Exporter_name_app_3': exporter_name_app,
        'App-Listen-Port-3': details.get('listen_port', ''),
        'Exporter_SSL': 'FALSE',
        'icmp': 'FALSE',
        'ssh-banner': 'FALSE',
        'tcp-connect': 'FALSE',
        'ssh_username': details.get('username', ''),
        'ssh_password': details.get('password', '')
    }
    return row

def process_exporter_data_os(exporter_data, csv_data, exporter_name):
    for hostname, details in exporter_data.items():
        if hostname not in csv_data:
            csv_data[hostname] = create_row(hostname, details, exporter_name_os=exporter_name)
        else:
            csv_data[hostname]['Exporter_name_os'] = exporter_name
            csv_data[hostname]['OS-Listen-Port'] = details.get('listen_port', '')



def process_exporter_data_app(exporter_data, csv_data, exporter_name_os='', exporter_name_app=''):
    if exporter_data is None:
        print(f"Warning: exporter_data is None for {exporter_name_app}")
        return
    for hostname, details in exporter_data.items():
        if hostname not in csv_data:
            csv_data[hostname] = create_row(hostname, details, exporter_name_os, exporter_name_app)
        else:
            if exporter_name_app:
                for i in range(1, 4):
                    app_key = f'Exporter_name_app_{i}' if i != 1 else 'Exporter_name_app'
                    port_key = f'App-Listen-Port-{i}' if i != 1 else 'App-Listen-Port'
                    if not csv_data[hostname].get(app_key):
                        csv_data[hostname][app_key] = exporter_name_app
                        csv_data[hostname][port_key] = details.get('listen_port', '')
                        break




def yaml_to_csv(yaml_file_path, csv_file_path):
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    csv_data = {}

    os_exporters = ['exporter_linux', 'exporter_windows', 'exporter_verint', 'exporter_vmware']
    app_exporters = [
    'exporter_cms', 'exporter_avayasbc', 'exporter_aes', 'exporter_verint',
    'exporter_gateway', 'exporter_breeze', 'exporter_sm', 'exporter_acm',
    'exporter_jmx', 'exporter_kafka', 'exporter_callback',
    'exporter_drac', 'exporter_genesyscloud', 'exporter_tcti',
    'exporter_aaep', 'exporter_pfsense', 'exporter_aic',
    'exporter_aam', 'exporter_ipoffice', 'exporter_iq',
    'exporter_ams', 'exporter_pc5', 'exporter_wfodb',
    'exporter_baas', 'exporter_redis', 'exporter_mpp', 'exporter_network',
    'exporter_weblm', 'exporter_audiocodesbc', 'exporter_voice_portal'
]
    ssl_exporters = ['exporter_ssl']
    bb_exporters = ['exporter_blackbox']

    # Create a new dictionary with hostname as the main key
    for exporter_name, exporter_data in data.items():
        if exporter_name in os_exporters:
            process_exporter_data_os(exporter_data, csv_data, exporter_name=exporter_name)
        elif exporter_name in app_exporters:
            process_exporter_data_app(exporter_data, csv_data, exporter_name_app=exporter_name, exporter_name_os=os_exporters)
        elif exporter_name in bb_exporters:
            process_exporter_data_bb(exporter_data, csv_data)
        elif exporter_name in ssl_exporters:
            process_exporter_data_ssl(exporter_data, csv_data)

    write_to_csv(csv_data, csv_file_path)

def write_to_csv(csv_data, csv_file_path):
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for hostname in csv_data:
            writer.writerow(csv_data[hostname])


def handle_exporter(exporter_data, exporter_name_os, exporter_name_app, csv_data):
    for hostname, details in exporter_data.items():
        app_index = next((i for i in range(1, 4) if details['ip_address'] not in csv_data or not csv_data[details['ip_address']].get(f'Exporter_name_app_{i}')), None)
        if app_index is None:
            print(f"Warning: Host {hostname} has more than 3 application exporters.")
            continue
        if details['ip_address'] in csv_data:
            csv_data[details['ip_address']][f'Exporter_name_app_{app_index}'] = exporter_name_app
            csv_data[details['ip_address']][f'App-Listen-Port-{app_index}'] = details.get('listen_port', '')
        else:
            row = create_row(hostname, details, exporter_name_os, exporter_name_app, app_index)
            csv_data[details['ip_address']] = row

def process_exporter_data_bb(exporter_data, csv_data):
    for hostname, hostname_data in exporter_data.items():
        for ip, ip_data in hostname_data.items():
            if hostname not in csv_data:
                csv_data[hostname] = dict.fromkeys(FIELDNAMES)
                csv_data[hostname]['Hostnames'] = hostname.split('.')[0]
                csv_data[hostname]['FQDN'] = hostname
                csv_data[hostname]['Domain'] = hostname.split('.')[1] if len(hostname.split('.')) > 1 else ''
                csv_data[hostname]['IP Address'] = ip_address
                csv_data[hostname]['Configuration Item Name'] = ip_data.get('config_item_name', '')
                csv_data[hostname]['Location'] = ip_data.get('location', '')
                csv_data[hostname]['Country'] = ip_data.get('country', '')
                
            # Setting icmp, ssh-banner, tcp-connect to TRUE if the module type is present
            module = ip_data.get('module', '')
            if module == 'icmp':
                csv_data[hostname]['icmp'] = 'TRUE'
            elif module == 'ssh_banner':
                csv_data[hostname]['ssh-banner'] = 'TRUE'
            elif module == 'tcp-connect':
                csv_data[hostname]['tcp-connect'] = 'TRUE'


def process_exporter_data_ssl(exporter_data, csv_data):
    for hostname, hostname_data in exporter_data.items():
        if hostname not in csv_data:
            csv_data[hostname] = dict.fromkeys(FIELDNAMES)
            csv_data[hostname]['Hostnames'] = hostname.split('.')[0]
            csv_data[hostname]['FQDN'] = hostname
            csv_data[hostname]['Domain'] = hostname.split('.')[1] if len(hostname.split('.')) > 1 else ''

        csv_data[hostname]['Exporter_SSL'] = 'TRUE'  # Setting SNMP to 'TRUE' if exporter_ssl is present


FIELDNAMES = ['Configuration Item Name', 'Location', 'Country', 'Domain', 'Hostnames', 
              'FQDN', 'IP Address', 'Exporter_name_os', 'OS-Listen-Port', 
              'Exporter_name_app', 'App-Listen-Port', 'Exporter_name_app_1', 'App-Listen-Port-1',
              'Exporter_name_app_2', 'App-Listen-Port-2', 
              'Exporter_name_app_3', 'App-Listen-Port-3', 'http_2xx', 'icmp', 'ssh-banner', 'tcp-connect', 
              'SNMP', 'Exporter_SSL', 'Notes', 'Description', 'Story #', 'Completed', 'Review comments', 'MaaS alarm', 
              'Resolution', 'comm_string', 'ssh_username', 'ssh_password', 'jmx_ports', 'snmp_version', 'snmp_user', 
              'snmp_password']


if __name__ == '__main__':
    yaml_file_path = sys.argv[1]
    csv_file_path = sys.argv[2]
    yaml_to_csv(yaml_file_path, csv_file_path)
