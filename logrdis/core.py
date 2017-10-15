import logging
import os
import click
from logrdis.config import parse
from logrdis.db import Adapter
from logrdis.socket import SocketServer

LOGGER = logging.getLogger()

# Create thread pool, each worker consumes from a queue
# Each worker is configured for sql; queue passes socket/address tuples

@click.command()
@click.option('--config', '-c', default='/etc/logrdis/logrdis.yml', help='logrdis configuration directives; this file defaults to /etc/logrdis/logrdis.yml')
def run_log_server(config):
    """Entry point function.

    :param config_path: str. a filepath to the YAML configuration directive
    :raises: OSError, KeyError
    """
    if not os.path.exists(config):
        raise OSError('{} does not exist'.format(config))
    config_directives = parse(config)

    if not 'engine' in config_directives:
        raise KeyError('engine not defined in configuration')
    sql = Adapter(config_directives['engine'])
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

    socket_server = SocketServer()
    socket_server.run_forever(cfg)

    LOGGER.info('Exiting')