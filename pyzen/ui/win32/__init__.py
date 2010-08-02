import threading

from pyzen.ui.win32.wrappers import *

class SystrayIconThread(threading.Thread):
    
    def run(self):
        self.hwnd = create_window('PyZen', self.window_proc)
        message_loop(self.hwnd)

    def window_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_CREATE:
            systray_add('green.ico', hwnd)
            return True
        if msg == WM_APP:
            print 'HELLO WORLD'
            return True
        return DefWindowProc(hwnd, msg, wparam, lparam)
    
    def post_message(self, msg, wparam, lparam):
        print 'Sending %s to %s'%(msg, self.hwnd)
        PostMessage(self.hwnd, msg, wparam, lparam)
    
    def quit(self):
        PostQuitMessage(0)

def main():    
    import time
    t = SystrayIconThread()
    t.start()
    time.sleep(2)
    t.post_message(WM_APP, 1, 2)
    #time.sleep(1)
    #print 'Sending quit'
    #t.quit()

if __name__ == '__main__':
    main()
