#!/usr/bin/env python 

#  
#  Copyright (C) 2011-2012 Cesar Suarez Ortega <suarez.ortega.cesar@gmail.com>
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
 
import atexit
import gobject
import glib
import dbus
import dbus.glib
import sys
import os
 
try:
	from dockmanager.dockmanager import DockManagerItem, DockManagerSink
	from dockmanager.dockmanager import RESOURCESDIR, DOCKITEM_IFACE
	from signal import signal, SIGTERM
	from sys import exit
except ImportError, e:
	exit()

hototdbus = 'org.hotot.service'
hototdbuspath = '/org/hotot/service'

class HototDBus():
	def __init__(self):
		bus = dbus.SessionBus()
		self.hotot = bus.get_object (hototdbus, hototdbuspath)
			
	def quit(self):
		self.hotot.quit()
		
	def show(self):
		self.hotot.show()
		
	def hide(self):
		self.hotot.hide()
	
	def get_unread(self):
		return self.hotot.unread()
		

class HototItem(DockManagerItem):
	def __init__(self, sink, path):
		DockManagerItem.__init__(self, sink, path)

		self.add_menu_item("Show", None, "Hotot Controls")
		self.add_menu_item("Hide", None, "Hotot Controls")
		self.add_menu_item("Update unread", "reload", "Hotot Controls")
		self.add_menu_item("Quit", "gtk-delete", "Hotot Controls")

		self.hotot = HototDBus()

		self.update_badge()

	def menu_pressed(self, menu_id):
 		if self.id_map[menu_id] == "Quit":
 			self.hotot.quit()
 		elif self.id_map[menu_id] == "Show":
 			self.hotot.show()
 		elif self.id_map[menu_id] == "Hide":
 			self.hotot.hide()
 		elif self.id_map[menu_id] == "Update unread":
 			self.update_badge()

 	def update_badge(self):
 		self.reset_badge()
 		unread_count = str(self.hotot.get_unread())
 		if not unread_count == "0":
 			self.set_badge(unread_count)


class HototSink(DockManagerSink):
 	def item_path_found(self, pathtoitem, item):
 		if item.Get(DOCKITEM_IFACE, "DesktopFile", dbus_interface="org.freedesktop.DBus.Properties").endswith ("hotot.desktop"):
 			self.items[pathtoitem] = HototItem(self, pathtoitem)
 
hototsink = HototSink()
 
def cleanup():
	hototsink.dispose()
 
if __name__ == "__main__":
	mainloop = gobject.MainLoop(is_running=True)

	atexit.register(cleanup)
	signal(SIGTERM, lambda signum, stack_frame: exit(1))

	mainloop.run()