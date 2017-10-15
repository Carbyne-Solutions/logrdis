import logging
from .config import parse
from .db import Adapter
from .socket import run_forever

LOGGER = logging.getLogger()

# Create thread pool, each worker consumes from a queue
# Each worker is configured for sql; queue passes socket/address tuples

def run_log_server(config_path):
    """Entry point function.

    :param config_path: str. a filepath to the YAML configuration directive
    :raises: OSError, KeyError
    """
    if not os.path.exists(config_path):
        raise OSError('{} does not exist'.format(config_path))
    config = parse(config_path)

    if not 'engine' in config:
        raise KeyError('engine not defined in configuration')
    sql = Adapter(config['engine'])
    for process, directives in cfg['process'].items():
        if directives['action'] == 'store':
            if 'pk' not in directives:
                raise KeyError('No pk field declared in process config')
            if 'tablename' not in directives:
                raise KeyError('No tablename field declared in process config')
            if 'schema' not in directives:
                raise KeyError('No schema field declared in process config')
            sql.declare(directives['tablename'], directives['pk'], directives['schema'])
            LOGGER.info('Stored directive {}'.format(directives['tablename']))

    run_forever(cfg)

    LOGGER.info('Exiting')