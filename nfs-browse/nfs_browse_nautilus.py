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
import gtk
import nautilus
import gconf
import urllib
from nfs_lan.nfs_browse import AvahiNFSBrowse
#from ConfigParser import ConfigParser
import gio

#config = ConfigParser({'net_folder':'/net'})
#config.read(os.path.expanduser('~/.nfs-lan'))
netFolder = '/net'	#config.get('main', 'net_folder')

class NfsBrowseExtension(nautilus.MenuProvider, nautilus.InfoProvider):
	"""
	Nautilus extension
	"""

	def __init__(self):
		self.client = gconf.client_get_default()
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
		item = nautilus.MenuItem('nfs-lan::file-refresh',
								 'Refresh NFS',
								 'Refresh NFS')
		item.set_property('icon', 'gtk-refresh')
		item.connect('activate', self.menu_activate_cb, file)
		return item,
	
	def get_background_items(self, window, file):
		if not file:
			return
		filename = urllib.unquote(file.get_uri()[7:])
		if not file.is_directory() or not filename.startswith(self.net_folder):
			return
		
		item = nautilus.MenuItem('nfs-lan::background-refresh',
								 'Refresh NFS',
								 'Refresh NFS')
		item.set_property('icon', 'gtk-refresh')
		item.connect('activate', self.menu_background_activate_cb, file)
		
		return item,
	
	def get_toolbar_items(self, window, file):
		if not file:
			return
		try:
			filename = urllib.unquote(file.get_uri()[7:])
		except:
			filename = file.get_uri()[7:]
		
		if not file.is_directory() or not filename.startswith(self.net_folder):
			return
	
		item = nautilus.MenuItem('nfs-lan::toolbar-refresh',
								 'Refresh NFS',
								 'Refresh NFS' )
		item.set_property('icon', 'gtk-refresh')
		item.connect('activate', self.menu_background_activate_cb, file)

		return item,
#-------------------------------------------------------------------------------
class InfoPanel(gtk.HBox):
	
	
	def __openComp(self, sender):
		compName = self.entry.get_text()
		os.system("cd " + self.net_folder + "/" + compName)
		os.system("cd " + self.net_folder + "/" + compName + '.local')
		
	def refresh(self, sender = None):
		a = AvahiNFSBrowse(self.net_folder)
		a.walk_comps()
		
	def __init__(self, label):
		gtk.HBox.__init__(self, False)
		self.net_folder = netFolder		
		image =  gtk.image_new_from_gicon(gio.ThemedIcon('preferences-system-network'),gtk.ICON_SIZE_LARGE_TOOLBAR)
#		image.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_LARGE_TOOLBAR)
		label = gtk.Label('<b>NFS network</b>')
		label.set_use_markup(True)
		btn = gtk.Button(gtk.STOCK_REFRESH)
		btn.set_use_stock(True)
		label3 = gtk.Label('Computer name or ip:')
		self.entry = gtk.Entry()
		btn2 = gtk.Button('Go', gtk.STOCK_GO_FORWARD)
		btn.connect('clicked',self.refresh)
		btn2.connect('clicked', self.__openComp)
		btn3 = gtk.Button('Help', gtk.STOCK_HELP)
		btn4 = gtk.Button('Preferences', gtk.STOCK_PREFERENCES)
		
		hbox2 = gtk.HBox(False)
		hbox2.pack_start(label3, False)
		hbox2.pack_start(self.entry, False)
		hbox2.pack_start(btn2, False)		
		
		self.pack_start(image, False)
		self.pack_start(label, False, False, 10)
		self.pack_start(btn, False, False, 10)
		self.pack_start(hbox2, False, False, 10)
		#self.pack_start(btn3, False,False, 10)
		#self.pack_start(btn4, False,False, 10)		

class LocationProviderExample(nautilus.LocationWidgetProvider):
    def __init__(self):
        LocationProviderExample.refreshed = False
    
    def get_widget(self, uri, window):
    	if not uri:
    		return False
    	filename = urllib.unquote(uri[7:])
    	if not filename.startswith(netFolder):
			return False

        self.hbox = InfoPanel('Test')
        self.hbox.show_all()
        if not LocationProviderExample.refreshed:
			self.hbox.refresh(self)
			LocationProviderExample.refreshed = True
        return self.hbox
		
