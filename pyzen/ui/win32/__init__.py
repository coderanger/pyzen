from pyzen.ui.win32.wrappers import *

def window_proc(hwnd, msg, wparam, lparam):
    print 'In window_proc %s'%msg
    if msg == WM_CREATE:
        systray_add('green.ico', hwnd)
        return True
    return DefWindowProc(hwnd, msg, wparam, lparam)

def main():    
    create_window('PyZen', window_proc)
    msg = MSG()
    while 1:
        got_message = GetMessage(byref(msg), None, 0, 0)
        if got_message == 0 or got_message == -1:
            break
        print 'Got a message'
        TranslateMessage(byref(msg))
        DispatchMessage(byref(msg))

if __name__ == '__main__':
    main()
