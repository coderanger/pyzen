import time
import unittest

try:
    import colorama
except ImportError:
    from pyzen import _colorama as colorama

COLOR_SUCCESS = colorama.Fore.GREEN
COLOR_FAIL = colorama.Fore.RED
COLOR_RESET = colorama.Fore.RESET

class ColoredTextTestResult(unittest._TextTestResult):
    
    def addSuccess(self, test):
        self.stream.write(COLOR_SUCCESS)
        unittest._TextTestResult.addSuccess(self, test)
        self.stream.write(COLOR_RESET)
    
    def addError(self, test, err):
        self.stream.write(COLOR_FAIL)
        unittest._TextTestResult.addError(self, test, err)
        self.stream.write(COLOR_RESET)
    
    def addFailure(self, test, err):
        self.stream.write(COLOR_FAIL)
        unittest._TextTestResult.addFailure(self, test, err)
        self.stream.write(COLOR_RESET)

    def printErrorList(self, flavour, errors):
            for test, err in errors:
                self.stream.writeln(self.separator1)
                self.stream.write(COLOR_FAIL)
                self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
                self.stream.write(COLOR_RESET)
                self.stream.writeln(self.separator2)
                self.stream.writeln("%s" % err)

class ColoredTextTestRunner(unittest.TextTestRunner):
    
    def __init__(self, *args, **kwargs):
        unittest.TextTestRunner.__init__(self, *args, **kwargs)
        wrapper = colorama.AnsiToWin32(self.stream)
        if wrapper.should_wrap():
            self.stream = wrapper.stream
    
    def _makeResult(self):
        return ColoredTextTestResult(self.stream, self.descriptions, self.verbosity)
    
    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()
        if not result.wasSuccessful():
            self.stream.write(COLOR_FAIL)
            self.stream.write("FAILED (")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                self.stream.write("failures=%d" % failed)
            if errored:
                if failed: self.stream.write(", ")
                self.stream.write("errors=%d" % errored)
            self.stream.writeln(")")
        else:
            self.stream.write(COLOR_SUCCESS)
            self.stream.writeln("OK")
        self.stream.write(COLOR_RESET)
        return result

def get_test_runner(nocolor):
    if nocolor:
        return unittest.TextTestRunner
    else:
        return ColoredTextTestRunner