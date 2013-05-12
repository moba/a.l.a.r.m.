from yapsy.IPlugin import IPlugin
from IAlarmPlugin import IMonitorPlugin, IAlarmPlugin

AC_STATE_LOCATION = '/sys/class/power_supply/AC/online'

import pyinotify

class MonitorAC(IMonitorPlugin):
   class EventHandler(pyinotify.ProcessEvent):
      def process_IN_ACCESS(self, event):
         print "In access:", event.pathname

   def setup(self,actions):
      self.actions = actions
      self.AlarmRaised = False
      self.wm = pyinotify.WatchManager()
      self.mask = pyinotify.IN_ACCESS
      self.notifier = pyinotify.ThreadedNotifier(self.wm, self.EventHandler())
      self.notifier.start()

   def activate(self):
      self.alarmRaised = False
      self.wdd = self.wm.add_watch(AC_STATE_LOCATION, self.mask, rec=False)

   def deactivate(self):
      self.alarmRaised = False
      if self.wdd and self.wdd[AC_STATE_LOCATION]>0:
         self.wm.rm_watch(self.wdd[AC_STATE_LOCATION], rec=False)

