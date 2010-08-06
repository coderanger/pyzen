from pyzen.ui.base import img_path, PyZenUI

try:
    import pynotify
except ImportError:
    pynotify = None

class LibnotifyUI(PyZenUI):
    """A PyZen UI that uses libnotify (via pynotify)."""
    
    name = 'libnotify'
    platform = 'linux2'

    def __init__(self):
        self.has_notify = pynotify.init('PyZen')
    
    @classmethod
    def enabled(cls):
        return super(LibnotifyUI, cls).enabled() and pynotify is not None
    
    def notify(self, failure, title, msg, icon):
        if self.has_notify:
            n = pynotify.Notification(title, msg, 'file://'+img_path(icon+'.png'))
            n.show()
