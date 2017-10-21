import os
import re
import pytest
from ..logrdis import config, db


def test_declare(test_yaml):
    """Declare and test config file entries."""
<<<<<<< HEAD
    cfg = test_yaml()
=======
    cfg = test_yaml
>>>>>>> f061c540c3a4286ec65526dc6aab5ea48586e859
    sql = db.Adapter(cfg['engine'])
    for process, directives in cfg['process'].items():
        if directives['action'] == 'store':
            sql.declare(directives['tablename'], directives['pk'], directives['schema'])

            assert directives['tablename'] in sql.tables
            for key in sql.definitions[directives['tablename']].keys():
                assert key in sql.definitions[directives['tablename']]

    assert len(sql.tables) == 1
    os.remove('test.sql')

def test_create(setup_db):
    """Test create function."""
    sql = setup_db
    results = sql.query('access_logs', 'mac_source').all()
    assert results == list()

def test_store(sample_entry, setup_db, test_yaml):
    """Test store function."""
<<<<<<< HEAD
    cfg = test_yaml()
=======
    cfg = test_yaml
>>>>>>> f061c540c3a4286ec65526dc6aab5ea48586e859
    sql = setup_db
    sample_regex = re.compile(cfg['ingest']['data'])
    sample_match = sample_regex.search(sample_entry)

    sql.store('access_logs', sample_match)

    results = sql.query('access_logs', 'mac_source').one()
    assert results[0] == 'mac_source'
    results = sql.query('access_logs', 'id').one()
    assert results[0] == 0