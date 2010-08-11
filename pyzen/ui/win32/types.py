from win32con import *
from ctypes import *
from ctypes.wintypes import *
from pyzen.ui.base import img_path

NULL = c_void_p()

class errcheck(object):
    
    def __init__(self, error_value=None):
        self.error_value = error_value
    
    def __call__(self, result, func, arguments):
        if result == self.error_value:
            raise WinError()
        return result

# Some basic Windows types
TCHAR = c_char
LPCTSTR = LPCSTR
LPTSTR = LPSTR
HCURSOR = c_ulong

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
        ('szTip', TCHAR*128),
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

NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
NIF_STATE = 0x00000008
NIF_INFO = 0x00000010
NIF_GUID = 0x00000020
NIF_REALTIME = 0x00000040
NIF_SHOWTIP = 0x00000080

NIIF_NONE = 0x0000
NIIF_INFO = 0x0001
NIIF_WARNING = 0x0002
NIIF_ERROR = 0x0003
NIIF_USER = 0x0004

Shell_NotifyIcon = windll.shell32.Shell_NotifyIcon
Shell_NotifyIcon.argtypes = [DWORD, POINTER(NOTIFYICONDATA)]
Shell_NotifyIcon.restype = BOOL

# MAKEINTRESOURCE
MAKEINTRESOURCE = lambda n: cast(n, c_char_p)

# LoadImage
LoadImage = windll.user32.LoadImageA
LoadImage.argtypes = [HINSTANCE, LPCTSTR, UINT, c_int, c_int, UINT]
LoadImage.restype = c_void_p
LoadImage.errcheck = errcheck()

IMAGE_BITMAP = 0
IMAGE_CURSOR = 2
IMAGE_ICON = 1

LR_LOADFROMFILE = 16

# LoadCursor
LoadCursor = windll.user32.LoadCursorA
#LoadCursor.argtypes = [HINSTANCE, LPCTSTR]
LoadCursor.restype = HCURSOR
LoadCursor.errcheck = errcheck()

IDC_ARROW = MAKEINTRESOURCE(32512)

# CreateWindowEx
CreateWindowEx = windll.user32.CreateWindowExA
CreateWindowEx.argtypes = [DWORD, LPCTSTR, LPCTSTR, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowEx.restype = HWND
CreateWindowEx.errcheck = errcheck()    

# RegisterClassEx
LRESULT = c_long
WPARAM = c_int
LPARAM = c_void_p
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
#WNDPROC = CFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
#WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)

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
RegisterClassEx.errcheck = errcheck()

# GetClassInfoEx
GetClassInfoEx = windll.user32.GetClassInfoExA
GetClassInfoEx.argtypes = [HINSTANCE, LPCTSTR, POINTER(WNDCLASSEX)]
GetClassInfoEx.restype = BOOL

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

# IsDialogMessage
IsDialogMessage = windll.user32.IsDialogMessageA
IsDialogMessage.argtypes = [HWND, POINTER(MSG)]
IsDialogMessage.restype = BOOL

# SendMessage
SendMessage = windll.user32.SendMessageA
SendMessage.argtype = [HWND, UINT, WPARAM, LPARAM]
SendMessage.restype = LRESULT

# PostMessage
PostMessage = windll.user32.PostMessageA
PostMessage.argtype = [HWND, UINT, WPARAM, LPARAM]
PostMessage.restype = BOOL
PostMessage.errcheck = errcheck(0)

# PostQuitMessage
PostQuitMessage = windll.user32.PostQuitMessage
PostQuitMessage.argtypes = [c_int]

# PostThreadMessage
PostThreadMessage = windll.user32.PostThreadMessageA
PostThreadMessage.argtypes = [DWORD, UINT, WPARAM, LPARAM]
PostThreadMessage.restype = BOOL
PostThreadMessage.errcheck = errcheck(0)

# UpdateWindow
UpdateWindow = windll.user32.UpdateWindow
UpdateWindow.argtypes = [HWND]
UpdateWindow.restype = BOOL

# GetWindowThreadProcessId
GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [HWND, POINTER(DWORD)]
GetWindowThreadProcessId.restype = DWORD

# GetCurrentThreadId
GetCurrentThreadId = windll.kernel32.GetCurrentThreadId
GetCurrentThreadId.argtypes = []
GetCurrentThreadId.restype = DWORD

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
WM_CREATE = 0x0001
WM_QUIT = 0x0012
WM_INITDIALOG = 0x0110
WM_APP = 0x8000
