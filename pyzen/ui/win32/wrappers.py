from pyzen.ui.win32.types import *

class WindowsError(Exception):
    def __init__(self, msg, *args):
        last_error = GetLastError()
        error_msg = c_char_p()
        FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, c_void_p(), last_error, 0, byref(error_msg), 0, c_void_p())
        super(WindowsError, self).__init__((msg%args)+': '+error_msg.value)

def load_icon(name):
    return LoadImage(c_void_p(), img_path(name), IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

def systray_add(name, hwnd):
    nid = NOTIFYICONDATA()
    nid.cbSize = sizeof(NOTIFYICONDATA)
    nid.uID = 1
    nid.uFlags = NIF_ICON
    nid.hIcon = load_icon(name)
    nid.hWnd = hwnd
    Shell_NotifyIcon(NIM_ADD, byref(nid))

def register_window_class(name, wndproc):
    wc = WNDCLASSEX()
    wc.cbSize = sizeof(WNDCLASSEX)
    wc.lpfnWndProf = WNDPROC(wndproc)
    wc.lpszClassName = name
    wc.hInstance = GetModuleHandle(c_char_p())
    if not RegisterClassEx(byref(wc)):
        raise WindowsError('Unable to register window class %s'%name)

def create_window(class_name, name):
    hwnd = CreateWindowEx(0, class_name, name, 0, 0, 0, 0, 0, c_void_p(), c_void_p(), GetModuleHandle(c_char_p()), c_void_p())
    if not hwnd:
        raise WindowsError('Unable to create window %s'%name)
    return hwnd
