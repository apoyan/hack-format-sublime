import sublime, sublime_plugin
import subprocess, os, re, threading

class FormatHackCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.client = None
		proc = self.formatCode()
		stdout = proc.communicate()
	
	def formatCode(self):
		filename = self.window.active_view().file_name();
		directory = os.path.dirname(self.window.active_view().file_name())
		return subprocess.Popen(
            [
                which('hh_format'),"-i", filename 
            ],
            cwd = directory,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
