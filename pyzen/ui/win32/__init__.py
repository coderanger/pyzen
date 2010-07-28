from pyzen.ui.win32.wrappers import *

def window_proc(hwnd, msg, wparam, lparam):
    print 'In window_proc %s'%msg
    if msg == WM_INITDIALOG:
        systray_add('green.ico', hwnd)
        return True
    return DefWindowProc(hwnd, msg, wparam, lparam)

def main():
    register_window_class('PyZenHiddenWindow', window_proc)
    create_window('PyZenHiddenWindow', 'PyZen')
    msg = MSG()
    while 0:
        print '.'
        got_message = GetMessage(byref(msg), HWND(), 0, 0)
        if got_message == 0 or got_message == -1:
            break
        print 'Got a message'
        TranslateMessage(byref(msg))
        DispatchMessage(byref(msg))

if __name__ == '__main__':
    main()
