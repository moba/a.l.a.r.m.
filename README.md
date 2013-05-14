# A.L.A.R.M. - A Laptop A/C Removal Monitor

ALARM used to be a small Windows-only daemon that monitors
A/C power removal whenever you lock your laptop, and plays a loud
alarm sound when that happens. 

This aims to be a more flexible implementation that supports
two types of plugins, and works primarily on Linux.

## Plugins

### Monitor Plugins

Monitor plugins are activated whenever a user locks his screen.
They know about the existing action plugins, and can trigger
actions whenever necessary. Usally, they watch out for some event.

Event ideas:

  * A/C removal
  * USB changes
  * acceleration sensor movement (eg. Thinkpad, modern hard drives)

### Action plugins

Action plugins are invoked by monitor plugins, and disabled 
whenever a user unlocks his screen.

Action ideas:

  * raise an alarm (unmute, volume 100%, play sound)
  * hibernate
  * just log

