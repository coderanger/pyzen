import subprocess

from pyzen.ui.base import img_path

class AppleScriptError(Exception):
    pass


def run_script(script):
    proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(script)
    if proc.returncode != 0:
        raise AppleScriptError('osascript failure: %s'%err)
    out = out.strip()
    if out == 'true':
        return True
    elif out == 'false':
        return False
    elif out.isdigit():
        return int(out)
    else:
        return out

def is_growl_running():
    """Check if Growl is running. Run this before any other Growl functions."""
    script = """
    tell application "System Events"
        return count of (every process whose name is "GrowlHelperApp") > 0
    end tell
    """
    return run_script(script)

def register_app():
    script= """
    tell application "GrowlHelperApp"
     -- Make a list of all the notification types 
     -- that this script will ever send:
     set the notificationsList to {"Test Successful" , "Test Failure"}

     -- Register our script with growl.
     -- You can optionally (as here) set a default icon 
     -- for this script's notifications.
     register as application "ZenTest" all notifications notificationsList default notifications notificationsList
    end tell"""
    run_script(script)

def notify(type, title, msg):
    script= """
    tell application "GrowlHelperApp"
     notify with name "%s" title "%s" description "%s" application name "ZenTest" image from location "file://%s"
    end tell"""%(type, title, msg, img_path('logo.png'))
    print script
    run_script(script)

if is_growl_running():
    register_app()
    notify('Test Successful', 'Test Successful', 'Run 1 test(s) in 0.001 seconds')