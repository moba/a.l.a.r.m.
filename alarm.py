#!/usr/bin/env python
# coding: utf-8
# vim: set et sw=3:

import os
_PLUGINDIR = os.path.join(os.path.dirname(__file__), 'plugins-enabled')

import threading
from gobject import MainLoop
from dbus import SessionBus
from dbus.mainloop.glib import DBusGMainLoop
import gtk
#from subprocess import Popen

import AlarmPlugin

actions = {}
monitors = {}

class MonitorScreensaver:
    def __init__(self): 
        DBusGMainLoop(set_as_default=True)
        self.bus=SessionBus()
        self.loop=MainLoop()
        if self.bus.name_has_owner('org.kde.ScreenSaver'):
           screensaver = self.bus.get_object('org.freedesktop.ScreenSaver', 
                                            '/org/freedesktop/ScreenSaver')
           screensaver.connect_to_signal('ActiveChanged',self.screensaverEvent)
        if self.bus.name_has_owner('org.gnome.ScreenSaver'):
           screensaver = self.bus.get_object('org.gnome.ScreenSaver', 
                                            '/org/gnome/ScreenSaver')
           screensaver.connect_to_signal('ActiveChanged',self.screensaverEvent)        
        print "Waiting for Screensaver event"
        self.loop.run()

    def screensaverEvent(self, ssOn):
        if ssOn == 1:
           print "Screensaver enabled."
           for name, monitor in monitors.iteritems():
              print "Monitor: " + name + " activate"
              monitor.activate()
        else:
           print "Screensaver disabled."
           for name, action in actions.iteritems():
              print "Action: " + name + " deactivate"
              action.deactivate()
           for name, monitor in monitors.iteritems():
              print "Monitor: " + name + " deactivate"
              monitor.deactivate()

if __name__ == "__main__":
   gtk.gdk.threads_init()

   # load all plugins
   for plugin in AlarmPlugin.PluginLoader(_PLUGINDIR):
       print "Loading " + plugin.__name__
       instance = getattr(plugin, plugin.__name__)()
       if isinstance(instance,AlarmPlugin.IMonitorPlugin):
          monitors[plugin.__name__] = instance
       else:
          actions[plugin.__name__] = instance
       instance.setDaemon(True)

   for name, action in actions.iteritems():
       print "Initializing Action " + name
       action.start()

   # let monitor plugins know about available actions
   for monitor in monitors.values(): 
       monitor.setActions(actions)

   for name, monitor in monitors.iteritems():
       print "Initializing Monitor " + name
       monitor.start()

   # DEBUG: ACTIVATE ALL MONITOR PLUGINS EVEN WITHOUT SCREENSAVER
   for monitor in monitors.values(): 
       monitor.activate()

   MonitorScreensaver()

   exit()


