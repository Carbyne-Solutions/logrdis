"""Utility functions."""

import socket
import time

def wait_for(ip, port, timeout, _type='tcp'):
    """Wait for service by attempting socket connection to a tuple addr pair.

    :param ip: str. an IP address to test if it's up
    :param port: int. an associated port to test if a server is up
    :param timeout: int. timeout in number of seconds (*2), multiply by two
    because the socket timeout is set to 2 seconds
    :param _type: can be either tcp or udp
    :returns: bool. True if a connection was made, False otherwise
    """
    if _type == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif _type == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        raise AttributeError('Invalid socket type specified: {}'.format(_type))

    sock.settimeout(2)
    for counter in range(timeout):
        try:
            sock.connect((ip, int(port)))
            sock.close()
            return True
        except socket.error as err:
            pass
        time.sleep(1)
    return False
