import multiprocessing.connection
import os
import sys

from pyzen.ui.base import PyZenUI

class SublimeUI(PyZenUI):
    """A PyZen UI that talks to Sublime Text 2."""

    name = 'sublime'

    @classmethod
    def _read_pidfile(cls):
        if sys.platform == 'darwin':
            base_path = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'Sublime Text 2')
        pid_path = os.path.join(base_path, 'sublime2.pid')
        if not os.path.exists(pid_path):
            return None
        pid_file = open(pid_path, 'r')
        pid = int(pid_file.read().strip())
        pid_file.close()
        return pid

    @classmethod
    def _conn_path(cls):
        pid = cls._read_pidfile()
        if not pid:
            return None
        return '/tmp/.sublimepyzen.%s'%pid

    @classmethod
    def enabled(cls):
        path = cls._conn_path()
        if not path:
            return False
        try:
            client = multiprocessing.connection.Client(path)
            client.send(['PING', None])
            client.close()
            return True
        except Exception:
            return False

    def notify(self, failure, title, msg, icon):
        path = self._conn_path()
        if path:
            client = multiprocessing.connection.Client(path)
            client.send([os.getcwd(), (failure, title, msg)])
            client.close()
