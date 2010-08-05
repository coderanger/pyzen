from multiprocessing import Process, Queue
from threading import Thread

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

def reloader(q, func, args, kwargs):
    t = Thread(target=func, args=args, kwargs=kwargs)
    t.start()
    _reloader_thread()

def main(func, *args, **kwargs):
    while True:
        q = Queue()
        p = Process(target=reloader, args=(q, func, args, kwargs))
        p.daemon = True
        p.start()
        try:
            cmd = q.get(True, _SLEEP_TIME)
        except Queue.Empty:
            # Timed out, check if we need to restart
            if not p.is_alive() and p.exitcode != 3:
                break


