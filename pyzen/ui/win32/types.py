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
HBRUSH = c_void_p
ATOM = c_ushort
HMODULE = c_void_p
LPCVOID = c_void_p
LPTSTR = c_char_p

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
LRESULT = c_long
WPARAM = c_int
LPARAM = c_long
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
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

# GetModuleHandle
GetModuleHandle = windll.kernel32.GetModuleHandleA
GetModuleHandle.argtypes = [LPCTSTR]
GetModuleHandle.restype = HMODULE

# GetSystemMetrics
GetSystemMetrics = windll.user32.GetSystemMetrics
GetSystemMetrics.argtypes = [c_int]
GetSystemMetrics.restype = c_int

SM_CXICON = 11
SM_CYICON = 12
SM_CXSMICON = 49
SM_CYSMICON = 50

# DefWindowProc
DefWindowProc = windll.user32.DefWindowProcA
DefWindowProc.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProc.restype = LRESULT

# GetMessage
class POINT(Structure):
    _fields_ = [
        ('x', c_long), # LONG x;
        ('y', c_long), # LONG y;
    ]

class MSG(Structure):
    _fields_ = [
        ('hwnd', HWND), # HWND   hwnd;
        ('message', UINT), # UINT   message;
        ('wParam', WPARAM), # WPARAM wParam;
        ('lParam', LPARAM), # LPARAM lParam;
        ('time', DWORD), # DWORD  time;
        ('pt', POINT), # POINT  pt;
    ]

GetMessage = windll.user32.GetMessageA
GetMessage.argtypes = [POINTER(MSG), HWND, UINT, UINT]
GetMessage.restype = BOOL

# TranslateMessage
TranslateMessage = windll.user32.TranslateMessage
TranslateMessage.argtypes = [POINTER(MSG)]
TranslateMessage.restype = BOOL

# DispatchMessage
DispatchMessage = windll.user32.DispatchMessageA
DispatchMessage.argtypes = [POINTER(MSG)]
DispatchMessage.restype = LRESULT

# UpdateWindow
UpdateWindow = windll.user32.UpdateWindow
UpdateWindow.argtypes = [HWND]
UpdateWindow.restype = BOOL

# GetLastError
GetLastError = windll.kernel32.GetLastError
GetLastError.argtypes = []
GetLastError.restype = DWORD

# FormatMessage
FormatMessage = windll.kernel32.FormatMessageA
FormatMessage.argtypes = [DWORD, LPCVOID, DWORD, DWORD, POINTER(LPTSTR), DWORD, c_void_p]
FormatMessage.restype = DWORD

FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_ARGUMENT_ARRAY = 0x00002000
FORMAT_MESSAGE_FROM_HMODULE = 0x00000800
FORMAT_MESSAGE_FROM_STRING = 0x00000400
FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200
FORMAT_MESSAGE_MAX_WIDTH_MASK = 0x000000FF

# Misc constants
WM_INITDIALOG = 0x0110
