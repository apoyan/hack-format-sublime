import sublime, sublime_plugin
import subprocess, os, re, threading

class HackFormat(threading.Thread):
    def __init__(self, window):
        super(HackFormat, self).__init__()
        self.window = window
        self.client = None

    def run(self):
        self.client = self.startClient()
        self.client.wait()
        self.client.communicate()

    def startClient(self):
        filename  = self.window.active_view().file_name();
        directory = os.path.dirname(filename)
        return subprocess.Popen(
            [
                which('hh_format'), "-i", filename 
            ],
            cwd    = directory,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

class HackFormatCommand(sublime_plugin.WindowCommand):
    def run(self):
        if not checkFileType(self.window.active_view()):
            return

        hack_format = HackFormat(self.window)
        hack_format.start()

def checkFileType(view):
    tag = view.substr(sublime.Region(0, 4))
    return tag == '<?hh'

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        pathenv = os.getenv("PATH") + os.pathsep + "/usr/local/bin/"
        for path in pathenv.split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    raise Exception("hh_format executable not found")