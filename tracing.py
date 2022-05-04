import sys
import re
from subprocess import Popen, PIPE
import json
import requests
import socket

IP_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
AS_pattern = re.compile(r'AS\d+')
country_pattern = re.compile(r'[A-Za-z]+\s[A-Za-z]+')


def trace(address: str) -> list:
    ip_address = convert_domain_to_ip(address)
    cmd = f"tracert {ip_address}"
    pipe = Popen(cmd, shell=True, universal_newlines=True, stdout=PIPE)
    stdout = pipe.stdout.read()
    return IP_pattern.findall(stdout)


def convert_domain_to_ip(domain: str) -> str:
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        print('Неккоректное доменное имя')
        sys.exit()


def get_ip_data(ip_list: list):
    ips_data = [[]]
    for ip in ip_list:
        info = get_info_by_ip(ip)
        ips_data.append(info)
    return ips_data


def get_info_by_ip(ip: str) -> list:
    if is_gray_ip(ip):
        return [ip, '-', '-', '-']
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        response_json = json.loads(response.content)
        org_info = response_json["org"]
        a_s = AS_pattern.findall(org_info)[0]
        provider = country_pattern.findall(org_info)[0]
        country = response_json["country"]
        return [ip, a_s, country, provider]
    except Exception:
        return [ip, 'No info', 'No info', 'No info']


def is_gray_ip(ip: str) -> bool:
    return ip.startswith('10.')\
           or ip.startswith('192.168.')\
           or (ip.startswith('172.') and 15 < int(ip.split('.')[1]) < 32)


def get_table_string(number: int, ip_data) -> str:
    if number == 0:
        n = 'N'
        ip = 'IP'
        a_system = 'AS'
        country = 'COUNTRY'
        provider = 'PROVIDER'
    else:
        n = str(number)
        ip = ip_data[0]
        a_system = ip_data[1]
        country = ip_data[2]
        provider = ip_data[3]
    return f'| {n}' + ' ' * (3 - len(n)) + '| ' + ip + ' ' * (15 - len(ip)) + '| ' + a_system + ' ' * \
           (15 - len(a_system)) + '| ' + country + ' ' * (15 - len(country)) + '| ' + provider + ' ' * \
           (16 - len(provider)) + '|' + '\n'


def main():
    if len(sys.argv) != 2:
        print('To get information about usage print tracing.py --help')
        sys.exit(1)
    if sys.argv[1] == "--help":
        print('Usage: tracing.py \'domain or ip\'')
        sys.exit(1)
    else:
        address = sys.argv[1]
    ip_list = trace(address)
    ip_data = get_ip_data(ip_list)
    with open('out.txt', 'w') as f:
        for i in range(len(ip_data)):
            f.write(get_table_string(i, ip_data[i]))


if __name__ == '__main__':
    main()
