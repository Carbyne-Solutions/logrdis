import logging
import re
import socket
import sys
import threading
import time
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
    cfg = test_yaml()
    results = query_check(cfg)
    for res in results:
        assert re.search("[\d\w\:]+", res['mac_source'])

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
    cfg = test_yaml()
    results = query_check(cfg)
    for res in results:
        assert re.search("[\d\w\:]+", res['mac_source'])

    server.stop()

def test_socket_tcp_multiple_same_conn(log_server, sample_entries, test_yaml):
    """Test the TCP server."""
    # Send a log message
    server = log_server('tcp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LOGGER.debug('Sending test message to localhost:4444')
    sock.connect(('localhost', 4444))
    for msg in sample_entries:
        sock.send(msg.encode() + "\n".encode())
    sock.close()

    time.sleep(1)

    # verify that our log message was received
    cfg = test_yaml()
    results = query_check(cfg)
    index = 0
    for res in results:
        if index == 0:
            assert res['http_request_url'] == '172.217.5.228:1'
        elif index == 1:
            assert res['http_request_url'] == '172.217.5.228:2'
        elif index == 2:
            assert res['http_request_url'] == '172.217.5.228:3'
        index += 1
        assert re.search("[\d\w\:]+", res['mac_source'])

    server.stop()

def test_socket_tcp_multiple_multi_conn(log_server, sample_entries, test_yaml):
    """Test the TCP server."""
    # Send a log message
    server = log_server('tcp')
    for msg in sample_entries:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        LOGGER.debug('Sending test message to localhost:4444')
        sock.connect(('localhost', 4444))
        sock.send(msg.encode() + "\n".encode())
        sock.close()
        time.sleep(1)

    # verify that our log message was received
    cfg = test_yaml()
    results = query_check(cfg)
    index = 0
    for res in results:
        if index == 0:
            assert res['http_request_url'] == '172.217.5.228:1'
        elif index == 1:
            assert res['http_request_url'] == '172.217.5.228:2'
        elif index == 2:
            assert res['http_request_url'] == '172.217.5.228:3'
        index += 1
        assert re.search("[\d\w\:]+", res['mac_source'])

    server.stop()

def test_socket_udp_multiple_same_conn(log_server, sample_entries, test_yaml):
    """Test the UDP server."""
    # Send a log message
    server = log_server('udp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    LOGGER.debug('Sending test message to localhost:4444')
    for msg in sample_entries:
        sock.sendto(msg.encode(), ('localhost', 4444))
    sock.close()

    time.sleep(1)

    # verify that our log message was received
    cfg = test_yaml()
    results = query_check(cfg)
    index = 0
    for res in results:
        if index == 0:
            assert res['http_request_url'] == '172.217.5.228:1'
        elif index == 1:
            assert res['http_request_url'] == '172.217.5.228:2'
        elif index == 2:
            assert res['http_request_url'] == '172.217.5.228:3'
        index += 1
        assert re.search("[\d\w\:]+", res['mac_source'])

    server.stop()

def test_socket_udp_multiple_multi_conn(log_server, sample_entries, test_yaml):
    """Test the UDP server."""
    # Send a log message
    server = log_server('udp')
    for msg in sample_entries:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        LOGGER.debug('Sending test message to localhost:4444')
        sock.sendto(msg.encode(), ('localhost', 4444))
        sock.close()
        time.sleep(1)

    # verify that our log message was received
    cfg = test_yaml()
    results = query_check(cfg)
    index = 0
    for res in results:
        if index == 0:
            assert res['http_request_url'] == '172.217.5.228:1'
        elif index == 1:
            assert res['http_request_url'] == '172.217.5.228:2'
        elif index == 2:
            assert res['http_request_url'] == '172.217.5.228:3'
        index += 1
        assert re.search("[\d\w\:]+", res['mac_source'])

    server.stop()
