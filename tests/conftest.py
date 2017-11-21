import threading
import time
import os
import pytest
from ..logrdis import config
from ..logrdis import db
from ..logrdis.socket import SocketServer

server = SocketServer()

def find_test_yaml(test_file):
    for root, dirs, files in os.walk('.'):
        if test_file in files:
            return os.path.join(root, test_file)

def load_test_yaml(test_file='test.yml'):
    config_file = find_test_yaml(test_file)
    assert config_file, 'Could not find the {} configuration file!'.format(test_file)
    cfg = config.parse(config_file)
    return cfg

def run_test_server(socket):
    cfg = load_test_yaml()
    cfg['socket'] = socket
    sql = db.Adapter(cfg['engine'])

    for process, directives in cfg['process'].items():
        if not 'pk' in directives:
            directives['pk'] = "_id"
        if directives['action'] == 'store':
            sql.declare(directives['tablename'], directives['pk'], directives['schema'])

    server.run_forever(cfg, sql)

@pytest.fixture(scope="function")
def test_yaml():
	def int_fn():
		return load_test_yaml()
	return int_fn

@pytest.fixture(scope="function")
def log_server(request):
    """Log server, returns SocketServer instance."""
    def fin():
        os.remove('test.sql')
    request.addfinalizer(fin)

    def int_fn(socket):
        global server
        thr = threading.Thread(target=run_test_server, args=(socket,))
        thr.start()
        time.sleep(1)
        return server

    return int_fn

@pytest.fixture(scope="function")
def setup_db(request):
    """Fixture, returns sql Adapter object initialized."""
    def fin():
        os.remove('test.sql')
    request.addfinalizer(fin)

    cfg = load_test_yaml()
    sql = db.Adapter(cfg['engine'])

    for process, directives in cfg['process'].items():
        if not 'pk' in directives:
            directives['pk'] = '_id'
        if directives['action'] == 'store':
            sql.declare(directives['tablename'], directives['pk'], directives['schema'])
    return sql

@pytest.fixture(scope="module")
def sample_entry():
    return "time 2017-10-22_18:20:05+0000 time_response 60 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.228:443 user_name - squid_hier_code ORIGINAL_DST ip_destination 172.217.5.228 http_content_type -"

@pytest.fixture(scope="module")
def sample_entries():
    return ["time 2017-10-22_18:20:05+0000 time_response 60 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.228:1 user_name - squid_hier_code ORIGINAL_DST ip_destination 172.217.5.228 http_content_type -", "time 2017-10-22_18:20:05+0000 time_response 60 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.228:2 user_name - squid_hier_code ORIGINAL_DST ip_destination 172.217.5.228 http_content_type -", "time 2017-10-22_18:20:05+0000 time_response 60 mac_source 08:00:27:f4:c8:4b ip_source 10.0.2.16 squid_request_status TAG_NONE http_status_code 200 http_reply_size 0 http_request_method CONNECT http_request_url 172.217.5.228:3 user_name - squid_hier_code ORIGINAL_DST ip_destination 172.217.5.228 http_content_type -"] 