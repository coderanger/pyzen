import sys
import os
import time
import traceback
from multiprocessing import Process, Queue
from threading import Thread
from Queue import Empty

from pyzen.ui import load_ui

_SLEEP_TIME = 1

def _reloader_thread():
    """When this function is run from the main thread, it will force other
    threads to exit when any modules currently loaded change.
    
    @param modification_callback: a function taking a single argument, the
        modified file, which is called every time a modification is detected
    """
    mtimes = {}
    while True:
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
                sys.exit(3)
        time.sleep(_SLEEP_TIME)

def _runner_thread(q, func, args, kwargs):
    try:
        start_time = time.clock()
        result = func(*args, **kwargs)
        end_time = time.clock()
        q.put({
            'failures': len(result.failures),
            'errors': len(result.errors),
            'total': result.testsRun,
            'time': end_time - start_time,
        })
    except Exception:
        traceback.print_exc()
        q.put({
            'failures': -1,
            'errors': -1,
            'total': -1,
            'time': 0,
        })

def reloader(q, func, args, kwargs):
    t = Thread(target=_runner_thread, args=(q, func, args, kwargs))
    t.start()
    try:
        _reloader_thread()
    except KeyboardInterrupt:
        pass

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
                        if p.exitcode == 3:
                            break # This means we need to restart it
                        else:
                            return p.exitcode # Any other return code should be considered real
    finally:
        for ui in uis:
            ui.shutdown()
        if p is not None:
            p.terminate()


