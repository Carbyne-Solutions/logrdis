import os
import pytest
from ..logrdis import config

def test_config(test_yaml):
    """Test the configuration module."""
    config_dict = test_yaml()
    assert config_dict['ingest']['bufferoutput'] == '^b(\\d)'
    assert config_dict['process']['data']['schema']['ip_source'] == 'String'

def test_config_env_sparse(request, test_yaml):
    def fin():
        del os.environ['DB_PROTO']
        del os.environ['DB_HOST']
        del os.environ['DB_NAME']

    request.addfinalizer(fin)
    os.environ['DB_PROTO'] = 'postgresql'
    os.environ['DB_HOST'] = 'squid_host'
    os.environ['DB_NAME'] = 'squid_name'

    config_dict = test_yaml()
    assert config_dict['engine'] == 'postgresql://squid_host/squid_name'

def test_config_env_rich(request, test_yaml):
    def fin():
        del os.environ['DB_PROTO']
        del os.environ['DB_HOST']
        del os.environ['DB_PORT']
        del os.environ['DB_NAME']
        del os.environ['DB_USER']
        del os.environ['DB_PASS']
        del os.environ['SOCKET']
        del os.environ['LISTEN_HOST']
        del os.environ['LISTEN_PORT']

    request.addfinalizer(fin)
    os.environ['DB_PROTO'] = 'postgresql'
    os.environ['DB_HOST'] = 'squidh'
    os.environ['DB_PORT'] = '5432'
    os.environ['DB_NAME'] = 'squidn'
    os.environ['DB_USER'] = 'squid'
    os.environ['DB_PASS'] = 'pass'
    os.environ['SOCKET'] = 'tcp'
    os.environ['LISTEN_HOST'] = '0.0.0.0'
    os.environ['LISTEN_PORT'] = '5555'

    config_dict = test_yaml()

    assert config_dict['engine'] == 'postgresql://squid:pass@squidh:5432/squidn'
    assert config_dict['socket'] == 'tcp'
    assert config_dict['listen_host'] == '0.0.0.0'
    assert config_dict['listen_port'] == '5555'