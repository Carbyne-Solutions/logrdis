import os
import yaml


def parse(filename):
    """Parse a yaml config file.

    Will parse a yaml configuration file for configuration directives.
    Some configuration directives can be overriden by passing arguments in
    the environment. In this case, there are certain rules:

        - If overriding the DATABASE protocol, define the DB_PROTO variable,
          see http://docs.sqlalchemy.org/en/latest/core/engines.html for
          configuration hints.
        - If configuring sqlite as the database backend, set DB_PROTO=sqlite, and
          optionally provide a path such as DB_URI=/var/lib/logrdis/logrdis.sql.
        - If configuring postgres for instance, set DB_PROTO=postgresql and at
          a minimum, define DB_HOST=postgres (see links in docker-compose.yml) as
          well as the DB_NAME (for instance, DB_NAME=logrdis).
        - It is also possible to override any of the top level configuration
          primitives, such as LISTEN_PORT, LISTEN_HOST and SOCKET.

    :param filename: a filename / filepath
    :returns: dict. a parsed configuration object
    :raises: KeyError. if required arguments are missing
    """
    with open(filename) as fptr:
        data = yaml.load(fptr.read())
    # Allow overrides of environmental variables
    db_proto = os.environ.get('DB_PROTO', None)
    if db_proto:  # if the DB_PROTO environmental variable is defined, override the data['engine'] setting
        data['engine'] = ""  # Override DB setting

        if db_proto == 'sqlite':
            db_uri = os.environ.get('DB_URI', ':memory:')
            data['engine'] = 'sqlite:///{}'.format(db_uri)
        else:
            db_user = os.environ.get('DB_USER', '')
            db_pass = os.environ.get('DB_PASS', '')
            db_host = os.environ.get('DB_HOST', '')
            db_port = os.environ.get('DB_PORT', '')
            db_name = os.environ.get('DB_NAME', '')

            if not db_host or not db_name:
                raise KeyError('Invalid configuration setting (DB_HOST and DB_NAME are required)')

            if db_user and db_pass:
                data['engine'] += "{}:{}@".format(db_user, db_pass)
            data['engine'] += db_host
            if db_port:
                data['engine'] += ":{}".format(db_port)
            data['engine'] += "/{}".format(db_name)

        LOGGER.info('Setting engine: {}'.format(data['engine']))

    # Override LISTEN_PORT, LISTEN_HOST and SOCKET directives
    listen_port = os.environ.get('LISTEN_PORT', None)
    listen_host = os.environ.get('LISTEN_HOST', None)
    socket = os.environ.get('SOCKET', None)

    if listen_port:
        data['listen_port'] = listen_port
        LOGGER.info('Setting listen_port: {}'.format(listen_port))

    if listen_host:
        data['listen_host'] = listen_host
        LOGGER.info('Setting listen_host: {}'.format(listen_host))

    if socket:
        data['socket'] = socket
        LOGGER.info('Setting socket: {}'.format(socket))

    return data