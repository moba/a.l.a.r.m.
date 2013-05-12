import sys
import os
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from AlarmPlugin import IMonitorPlugin

import pyudev

class MonitorUSB(IMonitorPlugin):
   def run(self):
      self.AlarmRaised = False
      self.isActive = False
      context = pyudev.Context()
      monitor = pyudev.Monitor.from_netlink(context)
      self.observer = pyudev.MonitorObserver(monitor, self.udev_callback)
# observer.start() and .stop() in activate/deactivate does not work, so run globally...
      self.observer.start() 

   def setActions(self, actions):
      self.actions = actions

   def udev_callback(self, action, device):
      if self.isActive and not self.alarmRaised: 
         if action == 'remove' or action == 'add':
            print "Monitor USB: {0} {1} ({2})".format(action, device.device_node, device.device_type)
            self.alarmRaised = True
            for action in self.actions.values(): 
                action.activate()

   def activate(self):
      self.isActive = True
      self.alarmRaised = False

   def deactivate(self):
      self.isActive = False
      self.alarmRaised = False
