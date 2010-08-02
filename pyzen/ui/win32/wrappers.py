from pyzen.ui.win32.types import *

#class WindowsError(Exception):
#    def __init__(self, msg, *args):
#        last_error = GetLastError()
#        error_msg = c_char_p()
#        FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, c_void_p(), last_error, 0, byref(error_msg), 0, c_void_p())
#        super(WindowsError, self).__init__((msg%args)+': '+error_msg.value)

def load_icon(name):
    return LoadImage(None, img_path(name), IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

def load_cursor(name):
    return LoadCursor(None, name)

def systray_add(name, hwnd):
    nid = NOTIFYICONDATA()
    nid.cbSize = sizeof(NOTIFYICONDATA)
    nid.uID = 1
    nid.uFlags = NIF_ICON
    nid.hIcon = load_icon(name)
    nid.hWnd = hwnd
    Shell_NotifyIcon(NIM_ADD, byref(nid))

def create_window(name, wndproc):
    wc = WNDCLASSEX()
    wc.cbSize = sizeof(WNDCLASSEX)
    wc.lpfnWndProc = WNDPROC(wndproc)
    wc.lpszClassName = name + 'Window'
    wc.hInstance = GetModuleHandle(None)
    wc.hIcon = load_icon('logo.ico')
    RegisterClassEx(pointer(wc))
    return CreateWindowEx(0, wc.lpszClassName, name, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, wc.hInstance, 0)

def message_loop(hwnd):
    msg = MSG()
    while 1:
        print 'Waiting for a message'
        got_message = GetMessage(byref(msg), None, 0, 0)
        print 'got_message=%r'%(got_message)
        if got_message == 0 or got_message == -1:
            break
        print 'message=%s hwnd=%s wparam=%s lparam=%s'%(msg.message, msg.hwnd, msg.wParam, msg.lParam)
        if IsDialogMessage(hwnd, byref(msg)):
            continue
        TranslateMessage(byref(msg))
        DispatchMessage(byref(msg))