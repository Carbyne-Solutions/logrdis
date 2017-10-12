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
            assert directives['schema'] == sql.__table_definitions[directives['tablename']]

    assert len(sql.tables) == 1