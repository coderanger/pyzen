import sys
import os
import copy
import imp
import unittest

from pyzen import core

def run_tests(argv):
    # Do this up here to avoid module errors w/ unittest, probably because
    # of my futzing with sys.modules below
    result = unittest.TestResult()
    result.total = -1
    
    # Munge sys.path and sys.argv
    path = argv[0]
    base = os.path.abspath(os.path.dirname(path))
    sys.path.insert(0, base)
    sys.argv[:] = argv
    
    # Create a new __main__ module
    mod = imp.new_module('__main__')
    mod.__file__ = path
    mod.__mtime__ = os.stat(path).st_mtime
    compiled = compile(open(path).read(), mod.__file__, 'exec')
    sys.modules['__main__'] = mod
    
    # Run the code
    fail = False
    try:
        exec compiled in mod.__dict__
    except SystemExit, e:
        if e.code:
            fail = True
    
    # len(failures)==1 indicates failure
    if fail:
        result.failures.append(None)
    return result
        
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    try:
        core.main(None, run_tests, argv)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()