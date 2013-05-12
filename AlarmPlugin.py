import os
import sys
import threading

class IAlarmPlugin(threading.Thread):
   def run(self,actions):
      pass
   def activate(self,actions):
      pass
   def deactivate(self,actions):
      pass

class IMonitorPlugin(IAlarmPlugin):
   def setActions(self,actionManager):
      pass

class IActionPlugin(IAlarmPlugin):
   pass

class PluginLoader():
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        for (dirpath, dirs, files) in os.walk(self.path):
            if not dirpath in sys.path:
                sys.path.insert(0, dirpath)
        for file in files:
                (name, ext) = os.path.splitext(file)
                if ext == os.extsep + "py":
                    yield __import__(name)

