import threading

from pyzen.ui.win32.types import *

def load_icon(name):
    return LoadImage(None, img_path(name), IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

def load_cursor(name):
    return LoadCursor(None, name)

def systray_add(name, hwnd):
    nid = NOTIFYICONDATA()
    nid.cbSize = sizeof(NOTIFYICONDATA)
    nid.uID = 1
    nid.uFlags = NIF_ICON | NIF_TIP
    nid.hIcon = load_icon(name)
    nid.hWnd = hwnd
    tip = 'PyZen'
    memmove(addressof(nid)+NOTIFYICONDATA.szTip.offset, tip, min(255, len(tip)))
    Shell_NotifyIcon(NIM_ADD, byref(nid))

def systray_delete(hwnd):
    nid = NOTIFYICONDATA()
    nid.cbSize = sizeof(NOTIFYICONDATA)
    nid.uID = 1
    nid.hWnd = hwnd
    Shell_NotifyIcon(NIM_DELETE, byref(nid))

def systray_modify(name, title, msg, hwnd):
    nid = NOTIFYICONDATA()
    nid.cbSize = sizeof(NOTIFYICONDATA)
    nid.uID = 1
    nid.uFlags = NIF_ICON | NIF_INFO | NIF_TIP
    nid.dwInfoFlags = NIIF_USER
    nid.hIcon = load_icon(name)
    tip = 'PyZen: '+title
    memmove(addressof(nid)+NOTIFYICONDATA.szTip.offset, tip, min(255, len(tip)))
    memmove(addressof(nid)+NOTIFYICONDATA.szInfo.offset, msg, min(255, len(msg)))
    memmove(addressof(nid)+NOTIFYICONDATA.szInfoTitle.offset, title, min(63, len(title)))
    nid.uTimeout = 10000
    nid.hWnd = hwnd
    Shell_NotifyIcon(NIM_MODIFY, byref(nid))

def create_window(name, wndproc):
    wc = WNDCLASSEX()
    wc.cbSize = sizeof(WNDCLASSEX)
    wc.lpfnWndProc = WNDPROC(wndproc)
    wc.lpszClassName = name + 'Window'
    wc.hInstance = GetModuleHandle(None)
    wc.hIcon = load_icon('logo.ico')
    RegisterClassEx(pointer(wc))
    return CreateWindowEx(0, wc.lpszClassName, name, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, wc.hInstance, 0)

def message_loop(hwnd, wndproc):
    msg = MSG()
    while 1:
        got_message = GetMessage(byref(msg), None, 0, 0)
        if got_message == 0 or got_message == -1:
            wndproc(hwnd, WM_QUIT, msg.wParam, msg.lParam)
            break
        try:
            if IsDialogMessage(hwnd, byref(msg)):
                continue
            TranslateMessage(byref(msg))
            if msg.message == WM_APP:
                wndproc(hwnd, msg.message, msg.wParam, msg.lParam)
            else:
                DispatchMessage(byref(msg))
        except WindowsError:
            print 'Error processing msg(%s, %s, %s)'%(msg.message, msg.wParam, msg.lParam)
            continue

class NotifyData(Structure):
    _fields_ = [
        ('title', c_char_p),
        ('msg', c_char_p),
        ('icon', c_char_p),
    ]

class SystrayIconThread(threading.Thread):
    
    def run(self):
        self.hwnd = create_window('PyZen', self.window_proc)
        message_loop(self.hwnd, self.window_proc)

    def window_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_CREATE:
            systray_add('green.ico', hwnd)
            #systray_modify('green.ico', 'Message', 'Testing', hwnd)
            return True
        if msg == WM_QUIT:
            systray_delete(hwnd)
            return True
        if msg == WM_APP:
            pnd = cast(lparam, POINTER(NotifyData))
            nd = pnd.contents
            systray_modify(nd.icon, nd.title, nd.msg, hwnd)
            return True
        return DefWindowProc(hwnd, msg, wparam, lparam)
    
    def post_message(self, msg, wparam, lparam):
        PostThreadMessage(self.ident, msg, wparam, lparam)
    
    def quit(self):
        self.post_message(WM_QUIT, 0, 0)
    
    def notify(self, title, msg, icon):
        nd = NotifyData()
        nd.title = title
        nd.msg = msg
        nd.icon = icon
        self.post_message(WM_APP, 0, cast(pointer(nd), LPARAM))
