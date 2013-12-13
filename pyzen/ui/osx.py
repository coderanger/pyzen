import subprocess
import os

from pyzen.ui.base import img_path, PyZenUI


class AppleScriptError(Exception):
    pass


class TerminalNotifierError(Exception):
    pass


def run_script(script):
    proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(script)
    if proc.returncode != 0:
        raise AppleScriptError('osascript failure: %s' % err)
    out = out.strip()
    if out == 'true':
        return True
    elif out == 'false':
        return False
    elif out.isdigit():
        return int(out)
    else:
        return out


def run_notifier(**kwargs):
    args = list()
    for (k, v) in kwargs.iteritems():
        if (k in ['message', 'title', 'subtitle', 'sound', 'group', 'list', 'activate', 'sender', 'open', 'execute']):
            args += ['-' + k, v]
    proc = subprocess.Popen(['terminal-notifier'] + args,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise TerminalNotifierError('terminal-notifier failure: %s' % err)
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


def is_notifier_installed():
    """Check if terminal-notifier is installed. Run this before any other functions."""
    return os.system("which terminal-notifier") == 0


def register_app():
    script = """
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


def notify(type, title, msg, img='logo.png'):
    script = """
    tell application "GrowlHelperApp"
     notify with name "%s" title "%s" description "%s" application name "ZenTest" image from location "file://%s"
    end tell""" % (type, title, msg, img_path(img))
    run_script(script)


class OSXUI(PyZenUI):

    """A PyZen UI that uses Growl. Only supported on OS X."""

    name = 'osx'
    platform = 'darwin'

    def __init__(self):
        self.has_notifier = is_notifier_installed()
        self.has_growl = is_growl_running()
        if self.has_growl:
            register_app()
        elif self.has_notifier:
            pass

    def notify(self, failure, title, msg, icon):
        type = failure and 'Test Failure' or 'Test Successful'
        if self.has_growl:
            notify(type, title, msg, icon + '.png')
        elif self.has_notifier:
            run_notifier(message=msg, title=title, subtitle=type)


# Random test stuff
if __name__ == '__main__':
    if is_notifier_installed():
        run_notifier(subtitle='Test Successful', title='Test Successful', message='Run 1 test(s) in 0.001 seconds')
    if is_growl_running():
        register_app()
        notify('Test Successful', 'Test Successful', 'Run 1 test(s) in 0.001 seconds', 'red.png')
