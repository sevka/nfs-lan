# -*- coding: utf-8 -*-
#
#		nfs-browse-nautilus.py
#
#       Copyright 2011 Sevka <sevka@ukr.net>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
import urllib
from nfs_lan.nfs_browse import AvahiNFSBrowse
#from ConfigParser import ConfigParser
from gi.repository import Nautilus, GObject, Gtk, GdkPixbuf

#config = ConfigParser({'net_folder':'/net'})
#config.read(os.path.expanduser('~/.nfs-lan'))
netFolder = '/net'	#config.get('main', 'net_folder')

class NfsBrowseExtension(GObject.GObject, Nautilus.MenuProvider, Nautilus.InfoProvider):
	"""
	Nautilus extension
	"""

	def __init__(self):
#		self.client = gconf.client_get_default()
		self.net_folder = netFolder
	
	def menu_activate_cb(self, menu, file):
		self.__refresh()

	def menu_background_activate_cb(self, menu, file): 
		self.__refresh()
	
	def __refresh(self):
		a = AvahiNFSBrowse(self.net_folder)
		a.walk_comps()
		'''
		if config.has_option('main', 'manual_shares'):
			manual_shares = config.get('main', 'manual_shares')
			for comp in manual_shares.split():
				os.system("cd " + self.net_folder + "/" + comp)
		'''	
	def get_file_items(self, window, files):
		if len(files) != 1 or (len(files) == 0 and not files[0].is_directory()):
			return
		filename = urllib.unquote(files[0].get_uri()[7:])
		if not filename.startswith(self.net_folder):
			return
		item = Nautilus.MenuItem(name='nfs-lan::file-refresh',
								 label='Refresh NFS',
								 tip='Refresh NFS')
		item.set_property('icon', 'gtk-refresh')
		item.connect('activate', self.menu_activate_cb, file)
		return [item]
	
	def get_background_items(self, window, file):
		if not file:
			return
		filename = urllib.unquote(file.get_uri()[7:])
		if not file.is_directory() or not filename.startswith(self.net_folder):
			return
		
		item = Nautilus.MenuItem(name='nfs-lan::background-refresh',
								 label='Refresh NFS',
								 tip='Refresh NFS')
		item.set_property('icon', 'gtk-refresh')
		item.connect('activate', self.menu_background_activate_cb, file)
		
		return [item]
#-------------------------------------------------------------------------------

class InfoPanel(Gtk.HBox):
	
	def __openComp(self, sender):
		compName = self.entry.get_text()
		os.system("cd " + self.net_folder + "/" + compName)
		os.system("cd " + self.net_folder + "/" + compName + '.local')
		self.entry.set_text("")
		
	def refresh(self, sender = None):
		a = AvahiNFSBrowse(self.net_folder)
		a.walk_comps()
		
	def __init__(self, label):
		Gtk.HBox.__init__(self, False)
		self.net_folder = netFolder		
#		image =  Gtk.image_new_from_gicon(gio.ThemedIcon('preferences-system-network'),Gtk.ICON_SIZE_LARGE_TOOLBAR)
#		image.set_from_stock(Gtk.STOCK_CONNECT, Gtk.ICON_SIZE_LARGE_TOOLBAR)
		label = Gtk.Label('<b>NFS network</b>')
		label.set_use_markup(True)
		btn = Gtk.Button(Gtk.STOCK_REFRESH)
		btn.set_use_stock(True)
		label3 = Gtk.Label('Computer name or ip:')
		self.entry = Gtk.Entry()
		btn2 = Gtk.Button('Ok', Gtk.STOCK_OK)
		btn.connect('clicked',self.refresh)
		btn2.connect('clicked', self.__openComp)
		btn3 = Gtk.Button('Help', Gtk.STOCK_HELP)
		btn4 = Gtk.Button('Preferences', Gtk.STOCK_PREFERENCES)
		
		hbox2 = Gtk.HBox(False)
		hbox2.pack_start(label3, False, False, 10)
		hbox2.pack_start(self.entry, False, False, 10)
		hbox2.pack_start(btn2, False, False, 10)
		
#		self.pack_start(image, False, False, 10)
		self.pack_start(label, False, False, 10)
		self.pack_start(btn, False, False, 10)
		self.pack_start(hbox2, False, False, 10)
		#self.pack_start(btn3, False,False, 10)
		#self.pack_start(btn4, False,False, 10)

class LocationPanel(GObject.GObject, Nautilus.LocationWidgetProvider):
	def __init__(self):
		LocationPanel.refreshed = False
		self.frame = False
	
	def get_widget(self, uri, window):
		if not uri:
			return False
		filename = urllib.unquote(uri[7:])
		if not filename.startswith(netFolder):
			return False
		if not self.frame:
			self.frame = Gtk.Frame()
			self.frame.hbox = InfoPanel('Test')
			self.frame.add(self.frame.hbox)
			self.frame.show_all()
		if not LocationPanel.refreshed:
			self.frame.hbox.refresh(self)
			LocationPanel.refreshed = True
		return self.frame