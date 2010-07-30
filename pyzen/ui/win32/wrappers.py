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
    RegisterClassEx(byref(wc))
    return CreateWindowEx(0, wc.lpszClassName, name, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, wc.hInstance, 0)
    

# def register_window_class(inst, name, wndproc):
#     import win32con
#     class WNDCLASS(Structure):
#         _fields_ = [('style', c_uint),
#                     ('lpfnWndProc', WNDPROC),
#                     ('cbClsExtra', c_int),
#                     ('cbWndExtra', c_int),
#                     ('hInstance', c_int),
#                     ('hIcon', c_int),
#                     ('hCursor', c_int),
#                     ('hbrBackground', c_int),
#                     ('lpszMenuName', c_char_p),
#                     ('lpszClassName', c_char_p)]
# 
#     
#     wndclass = WNDCLASS()
#     wndclass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
#     wndclass.lpfnWndProc = WNDPROC(wndproc)
#     wndclass.cbClsExtra = wndclass.cbWndExtra = 0
#     wndclass.hInstance = inst
#     wndclass.hIcon = windll.user32.LoadIconA(None, c_int(win32con.IDI_APPLICATION))
#     wndclass.hCursor = windll.user32.LoadCursorA(None, c_int(win32con.IDC_ARROW))
#     wndclass.hbrBackground = windll.gdi32.GetStockObject(c_int(win32con.WHITE_BRUSH))
#     wndclass.lpszMenuName = None
#     wndclass.lpszClassName = name
#     # Register Window Class
#     if not windll.user32.RegisterClassA(byref(wndclass)):
#         raise WinError()
    #return wndclass.hInstance
    
    # import win32con
    # hwnd = CreateWindowEx(0,
    #                       name,
    #                       'PyZen',
    #                       win32con.WS_OVERLAPPEDWINDOW,
    #                       win32con.CW_USEDEFAULT,
    #                       win32con.CW_USEDEFAULT,
    #                       win32con.CW_USEDEFAULT,
    #                       win32con.CW_USEDEFAULT,
    #                       win32con.NULL,
    #                       win32con.NULL,
    #                       wndclass.hInstance,
    #                       win32con.NULL)
    # return CreateWindowEx(0, name, 'PyZen', WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, inst, 0)
    # 
    # print hwnd


# def create_window(inst, class_name, name):
#     return CreateWindowEx(0, class_name, name, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, inst, 0)
# 
# def create_window(inst, class_name, name):
#     import win32con
#     hwnd = CreateWindowEx(0,
#                           class_name,
#                           name,
#                           win32con.WS_OVERLAPPEDWINDOW,
#                           win32con.CW_USEDEFAULT,
#                           win32con.CW_USEDEFAULT,
#                           win32con.CW_USEDEFAULT,
#                           win32con.CW_USEDEFAULT,
#                           win32con.NULL,
#                           win32con.NULL,
#                           inst,
#                           win32con.NULL)
#     return hwnd