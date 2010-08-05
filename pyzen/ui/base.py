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
        raise NotImplementedError
    
    def fail(self, failures, errors, total, time):
        raise NotImplementedError
    
    def shutdown(self):
        pass

def load_ui(override):
    if override:
        for ui in PyZenUIMeta.uis:
            if ui.name == override:
                return ui()
    else:
        for ui in PyZenUIMeta.uis:
            if ui.enabled():
                return ui()
    