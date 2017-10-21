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
        if directives['action'] == 'store':
            sql.declare(directives['tablename'], directives['pk'], directives['schema'])
    return sql

@pytest.fixture(scope="module")
def sample_entry():
    return "L0 time time_response mac_source ip_source squid_request_status http_status_code 55 http_request_method http_request_url user_name squid_hier_code ip_destination http_content_type"