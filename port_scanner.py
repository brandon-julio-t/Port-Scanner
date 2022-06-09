import socket
from common_ports import ports_and_services


def get_open_ports(target, port_range, is_verbose=False):
    open_ports = []

    ip = target

    is_ip = ip[0].isnumeric()
    if not is_ip:
        try:
            ip = socket.gethostbyname(ip)
        except:
            return 'Error: Invalid hostname'

    try:
        socket.inet_aton(ip)
    except socket.error:
        return 'Error: Invalid IP address'

    [start, end] = port_range
    for port in range(start, end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.75)
        result = s.connect_ex((ip, port))
        # print(f'{target} => {ip}:{port} => {result}')
        if result == 0:
            open_ports.append(port)
        s.close()

    if not is_verbose:
        return(open_ports)

    hostname = target

    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        pass

    message = f'Open ports for {hostname}'

    if hostname[0].isalpha():
        message += f' ({ip})'

    header = 'PORT     SERVICE'
    body = ''
    for port in open_ports:
        service_name = ports_and_services[port]
        body += str(port).ljust(9) + service_name + '\n'
    message += f'\n{header}\n{body}'
    return message.strip()

# print(get_open_ports("104.26.10.78", [440, 450], True))