import sys
import os
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from AlarmPlugin import IActionPlugin

SOUNDFILE = 'HouseAlarm.mp3'

import alsaaudio
import pyglet
import gtk

class ActionSound(IActionPlugin):    
   def run(self):
      gtk.gdk.threads_init()
      self.mixer = alsaaudio.Mixer()
      self.volume = self.mixer.getvolume()[0]
      self.wasMute = self.mixer.getmute()[0]
      self.isPlaying = False
      self.player = pyglet.media.Player()
      self.player.eos_action = 'loop'
      source = pyglet.media.load(SOUNDFILE, streaming=False)
      self.player.queue(source)      
      pyglet.app.run()

   def activate(self):
      if not self.isPlaying:
         self.volume = self.mixer.getvolume()[0]
         self.wasMute = self.mixer.getmute()[0]      
         self.mixer.setmute(0)
         self.mixer.setvolume(100)
         self.player.play()
         self.isPlaying = True

   def deactivate(self):
      if self.isPlaying:
         self.player.pause()
         self.mixer.setvolume(self.volume)
         self.mixer.setmute(self.wasMute)
         self.isPlaying = False
