import logging
import threading
import time
import socket
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..logrdis import config
from ..logrdis.db import Adapter

LOGGER = logging.getLogger()

def query_check(cfg):
    engine = create_engine(cfg['engine'])
    Session = sessionmaker(bind=engine)
    session = Session()
    results = session.execute('SELECT * from access_logs')
    return results

def test_socket_tcp(log_server, sample_entry, test_yaml):
    """Test the TCP server."""
    # Send a log message
    server = log_server('tcp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LOGGER.debug('Sending test message to localhost:4444')
    sock.connect(('localhost', 4444))
    sock.send(sample_entry.encode())
    sock.close()

    time.sleep(1)

    # verify that our log message was received
<<<<<<< HEAD
    cfg = test_yaml()
=======
    cfg = test_yaml
>>>>>>> f061c540c3a4286ec65526dc6aab5ea48586e859
    results = query_check(cfg)
    for res in results:
        assert res['mac_source'] == 'mac_source'

    server.stop()

def test_socket_udp(log_server, sample_entry, test_yaml):
    """Test the UDP server."""
    server = log_server('udp')
    # Send a log message
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    LOGGER.debug('Sending test message to localhost:4444')
    sock.sendto(sample_entry.encode(), ('localhost', 4444))
    sock.close()

    time.sleep(1)

    # verify that our log message was received
<<<<<<< HEAD
    cfg = test_yaml()
=======
    cfg = test_yaml
>>>>>>> f061c540c3a4286ec65526dc6aab5ea48586e859
    results = query_check(cfg)
    for res in results:
        assert res['mac_source'] == 'mac_source'
 
    server.stop()