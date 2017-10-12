import pytest
from ..legionperk import config

def test_config():
    """Test the configuration module."""
    config_dict = config.parse('test.yml')
    assert config_dict['ingest']['bufferoutput'] == 'b(\\d)'
    assert config_dict['process']['data']['schema']['ip_source'] == 'String'