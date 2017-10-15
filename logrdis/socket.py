import logging
import sys
from logrdis.db import Adapter

# Currently only support Python3 Asynchio implementation
if sys.version_info >= (3, 0):
    from ._socket3 import AsynchSocketServer as Server
else:
    raise ImportError('Require Python 3.0+')

LOGGER = logging.getLogger()

class SocketServer:
    def run_forever(self, cfg, sql):
        """Start a listener socket."""
        self.server = Server()
        self.server.run_forever(cfg, sql)

    def stop(self):
        self.server.stop()