import sys
import os
import time
import traceback
from multiprocessing import Process, Queue
from threading import Thread, Lock
from Queue import Empty

from pyzen.ui import load_ui

_SLEEP_TIME = 1

MAGIC_RETURN_CODE = 254

class ReloaderThread(Thread):
    def __init__(self):
        super(ReloaderThread, self).__init__()
        self.daemon = False
        self._quit = False
        self._quit_lock = Lock()
        self.do_reload = False

    def run(self):
        """When this is run, it will force other
        threads to exit when any modules currently loaded change.
        """
        mtimes = {}
        while True:
            with self._quit_lock:
                if self._quit:
                    return

            for filename in filter(None, [getattr(module, '__file__', None)
                                          for module in sys.modules.values()]):
                while not os.path.isfile(filename): # Probably in an egg or zip file
                    filename = os.path.dirname(filename)
                    if not filename:
                        break
                if not filename: # Couldn't map to physical file, so just ignore
                    continue

                if filename.endswith('.pyc') or filename.endswith('.pyo'):
                    filename = filename[:-1]

                if not os.path.isfile(filename):
                    # Compiled file for non-existant source
                    continue

                mtime = os.stat(filename).st_mtime
                if filename not in mtimes:
                    mtimes[filename] = mtime
                    continue
                if mtime > mtimes[filename]:
                    print >> sys.stderr, 'Detected modification of %s, restarting.' % filename
                    self.do_reload = True
                    sys.exit(MAGIC_RETURN_CODE)
            time.sleep(_SLEEP_TIME)

    def quit(self):
        with self._quit_lock():
            self._quit = True


class RunnerThread(Thread):
    """A thread to run the provided function and push the test results
    back to a Queue.
    """

    def __init__(self, q, func, args, kwargs):
        super(RunnerThread, self).__init__()
        self.q = q
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            start_time = time.clock()
            result = self.func(*self.args, **self.kwargs)
            end_time = time.clock()
            self.q.put({
                'failures': len(result.failures),
                'errors': len(result.errors),
                'total': result.testsRun,
                'time': end_time - start_time,
            })
        except Exception:
            traceback.print_exc()
            self.q.put({
                'failures': -1,
                'errors': -1,
                'total': -1,
                'time': 0,
            })


def reloader(q, func, args, kwargs):
    t = ReloaderThread()
    t.start()
    try:
        RunnerThread(q, func, args, kwargs).run()
    except KeyboardInterrupt:
        t.quit()
    finally:
        t.join()
        if t.do_reload:
            sys.exit(MAGIC_RETURN_CODE)


def main(ui_override, func, *args, **kwargs):
    p = None
    uis = list(load_ui(ui_override))
    try:
        while True:
            q = Queue()
            p = Process(target=reloader, args=(q, func, args, kwargs))
            p.daemon = True
            p.start()
            while True:
                try:
                    cmd = q.get(True, _SLEEP_TIME)
                    for ui in uis:
                        ui.handle(**cmd)
                except Empty:
                    # Timed out, check if we need to restart
                    if not p.is_alive():
                        if p.exitcode == MAGIC_RETURN_CODE:
                            break # This means we need to restart it
                        else:
                            return p.exitcode # Any other return code should be considered real
    finally:
        for ui in uis:
            ui.shutdown()
        if p is not None:
            p.terminate()
