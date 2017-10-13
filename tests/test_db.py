import pytest
from ..legionperk import config, db


def test_declare():
    """Declare and test config file entries."""
    cfg = config.parse('test.yml')
    sql = db.Adapter(cfg['engine'])
    for process, directives in cfg['process'].iteritems():
        if directives['action'] == 'store':
            sql.declare(directives['tablename'], directives['pk'], directives['schema'])

            assert directives['tablename'] in sql.tables
            for key in sql.definitions[directives['tablename']].iterkeys():
                assert key in sql.definitions[directives['tablename']]

    assert len(sql.tables) == 1


def test_create():
    """Test create function."""
    cfg = config.parse('test.yml')
    sql = db.Adapter(cfg['engine'])

    for process, directives in cfg['process'].iteritems():
        if directives['action'] == 'store':
            sql.declare(directives['tablename'], directives['pk'], directives['schema'])

    results = sql.query('access_logs', 'mac_source')
