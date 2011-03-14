import sys
import os

def img_path(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', name)

class PyZenUIMeta(type):
    uis = []
    def __init__(self, name, bases, d):
        super(PyZenUIMeta, self).__init__(name, bases, d)
        if name != 'PyZenUI':
            self.uis.append(self)


class PyZenUI(object):
    """Base class for PyZen UIs."""
    
    __metaclass__ = PyZenUIMeta
    
    name = None
    platform = None
    
    @classmethod
    def enabled(cls):
        return sys.platform == cls.platform
    
    def handle(self, failures, errors, total, time):
        if failures or errors:
            self.fail(failures, errors, total, time)
        else:
            self.success(total, time)
    
    def success(self, total, time):
        if total == -1:
            msg = 'Ran tests in %0.3f seconds'%time
        else:
            msg = 'Ran %s test%s in %0.3f seconds'%(total, total==1 and '' or 's', time)
        self.notify(False, 'Test Successful', msg, 'green')
    
    def fail(self, failures, errors, total, time):
        if total == -1:
            msg = 'Ran tests in %0.3f seconds'%time
        else:
            submsg = []
            if failures:
                submsg.append('failures=%s'%failures)
            if errors:
                submsg.append('errors=%s'%errors)
            msg = 'Ran %s test%s in %0.3f seconds (%s)'%(total, total==1 and '' or 's', time, ' '.join(submsg))
        self.notify(True, 'Test Failure', msg, 'red')
    
    def notify(self, failure, title, msg, icon):
        raise NotImplementedError
    
    def shutdown(self):
        pass

def load_ui(override):
    if override:
        if isinstance(override, basestring):
            override = set(override.split(','))
        for ui in PyZenUIMeta.uis:
            if ui.name in override:
                yield ui()
    else:
        for ui in PyZenUIMeta.uis:
            if ui.enabled():
                yield ui()
    