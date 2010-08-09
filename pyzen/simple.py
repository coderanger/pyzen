import sys
import os
import copy
import imp

from pyzen import core

def run_tests(argv):
    path = argv[0]
    base = os.path.abspath(os.path.dirname(path))
    sys.path.insert(0, base)
    sys.argv[:] = argv
    mod = imp.new_module('__main__')
    mod.__file__ = path
    mod.__mtime__ = os.stat(path).st_mtime
    compiled = compile(open(path).read(), mod.__file__, 'exec')
    sys.modules['__main__'] = mod
    exec compiled in mod.__dict__

def main(*argv):
    try:
        core.main(None, run_tests, argv)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main(*sys.argv[1:])