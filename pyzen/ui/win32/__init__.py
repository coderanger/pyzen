from pyzen.ui.base import PyZenUI

class Win32UI(PyZenUI):
    """A PyZen UI that uses the Win32 system tray."""
    
    name = 'win32'
    platform = 'win32'
    
    def __init__(self):
        from pyzen.ui.win32.wrappers import SystrayIconThread
        self.thread = SystrayIconThread()
        self.thread.start()
    
    def success(self, total, time):
        self.thread.post_message(WM_APP, 0, 0)
    
    def fail(self, failures, errors, total, time):
        self.thread.post_message(WM_APP, 1, 0)
    
    def shutdown(self):
        self.thread.quit()
        self.thread.join()


def main():    
    import time
    t = SystrayIconThread()
    t.start()
    time.sleep(2)
    t.post_message(WM_APP, 1, 2)
    time.sleep(1)
    print 'Sending quit'
    t.quit()
    
if __name__ == '__main__':
    main()
