from ctypes import *
from pyzen.ui.base import img_path

# Some basic Windows types
DWORD = c_ulong
HWND = c_void_p
UINT = c_uint
HICON = c_void_p
TCHAR = c_char
BOOL = c_int
HINSTANCE = c_void_p
LPCTSTR = c_char_p
HMENU  = c_void_p
LPVOID = c_void_p
HCURSOR = c_void_p
BRUSH = c_void_p
ATOM = c_ushort

class GUID(Structure):
    _fields_ = [
        ('Data1', c_ulong),
        ('Data2', c_ushort),
        ('Data3', c_ushort),
        ('Data4', c_byte*8),
    ]

# Shell_NotifyIcon
class NOTIFYICONDATA(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('hWnd', HWND),
        ('uID', UINT),
        ('uFlags', UINT),
        ('uCallbackMessage', UINT),
        ('hIcon', HICON),
        ('szTip', TCHAR*64),
        ('dwState', DWORD),
        ('dwSTateMask', DWORD),
        ('szInfo', TCHAR*256),
        ('uTimeout', UINT), # Also is uVersion
        ('szInfoTitle', TCHAR*64),
        ('dwInfoFlags', DWORD),
        ('guidItem', GUID),
        ('hBalloonIcon', HICON),
    ]

NIM_ADD = 0
NIM_MODIFY = 1
NIM_DELETE = 2
NIM_SETFOCUS = 3
NIM_SETVERSION = 4

NIF_MESSAGE = 0x0001
NIF_ICON = 0x0002
NIF_TIP = 0x0004
NIF_STATE = 0x0008
NIF_INFO = 0x0010
NIF_GUID = 0x0020
NIF_REALTIME = 0x0040
NIF_SHOWTIP = 0x0080

Shell_NotifyIcon = windll.shell32.Shell_NotifyIcon
Shell_NotifyIcon.argtypes = [DWORD, POINTER(NOTIFYICONDATA)]
Shell_NotifyIcon.restype = BOOL

# LoadImage
LoadImage = windll.user32.LoadImageA
LoadImage.argtypes = [HINSTANCE, LPCTSTR, UINT, c_int, c_int, UINT]
LoadImage.restype = c_void_p

IMAGE_BITMAP = 0
IMAGE_CURSOR = 2
IMAGE_ICON = 1

LR_LOADFROMFILE = 16

# CreateWindowEx
CreateWindowEx = windll.user32.CreateWindowExA
CreateWindowEx.argtypes = [DWORD, LPCTSTR, LPCTSTR, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowEx.restype = HWND

# RegisterClassEx
class WNDCLASSEX(Structure):
    _fields_ = [
        ('cbSize', UINT), #UINT      cbSize;
        ('style', UINT), #UINT      style;
        ('lpfnWndProc', WNDPROC), #WNDPROC   lpfnWndProc;
        ('cbClsExtra', c_int), #int       cbClsExtra;
        ('cbWndExtra', c_int), #int       cbWndExtra;
        ('hInstance', HINSTANCE), #HINSTANCE hInstance;
        ('hIcon', HICON), #HICON     hIcon;
        ('hCursor', HCURSOR), #HCURSOR   hCursor;
        ('hbrBackground', HBRUSH), #HBRUSH    hbrBackground;
        ('lpszMenuName', LPCTSTR), #LPCTSTR   lpszMenuName;
        ('lpszClassName', LPCTSTR), #LPCTSTR   lpszClassName;
        ('hIconSm', HICON), #HICON     hIconSm;
    ]

RegisterClassEx = windll.user32.RegisterClassExA
RegisterClassEx.argtypes = [POINTER(WNDCLASSEX)]
RegisterClassEx.restype = ATOM
    

def load_icon(name):
    return LoadImage(c_void_p(), img_path(name), IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

def systray_add(name):
    nid = NOTIFYICONDATA()
    nid.cbSize = sizeof(NOTIFYICONDATA)
    nid.uID = 1
    nid.uFlags = NIF_ICON
    nid.hIcon = load_icon(name)
    Shell_NotifyIcon(NIM_ADD, byref(nid))

systray_add('green.ico')
