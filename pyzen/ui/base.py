import os

def img_path(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', name)

class PyZenUI(object):
    """Base class for PyZen UIs."""
    
    def handle(self, failures, errors, total, time):
        if failures or errors:
            self.fail(failures, errors, total, time)
        else:
            self.success(total, time)
    
    def success(self, total, time):
        raise NotImplementedError
    
    def fail(self, failures, errors, total, time):
        raise NotImplementedError

