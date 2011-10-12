# -*- coding: utf-8 -*-
#
#		nfs-share-nautilus.py
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
import sys
from nfs_lan.nfs_share import ExportsSharing
import gtk
import nautilus
import gconf
import urllib
#from ConfigParser import ConfigParser

class NfsShareExtension(nautilus.MenuProvider, nautilus.InfoProvider):
	def __init__(self):
		self.client = gconf.client_get_default()
		#config = ConfigParser({'net_folder':'/net'})
		#config.read(os.path.expanduser('~/.nfs-lan'))
		self.net_folder = '/net'	#config.get('main', 'net_folder')
		
	def update_file_info(self, file):
		if not file:
			return
		filename = urllib.unquote(file.get_uri()[7:])
		if not file.is_directory() or file.get_uri_scheme() != 'file' or filename.startswith(self.net_folder):
			return
		
		try:
			es = ExportsSharing(filename)
			if es.isShared():
				file.add_emblem("shared")
		except:
			pass
	
	def _share(self, file):
		filename = urllib.unquote(file.get_uri()[7:])
		result = os.system("gksudo python /usr/share/pyshared/nfs_lan/nfs_share.py  \"" + filename  + "\"")
		self.update_file_info(file)

	
	def menu_activate_cb(self, menu, file):
		self._share(file)

	def menu_background_activate_cb(self, menu, file): 
		self._share(file)
		
	def get_file_items(self, window, files):
		if len(files) != 1:
			return
        
		file = files[0]
		filename = urllib.unquote(file.get_uri()[7:])
		if not file.is_directory() or file.get_uri_scheme() != 'file' or filename.startswith(self.net_folder):
			return

		item = nautilus.MenuItem('nfs-share::file-share',
								 'Share this folder through NFS...',
								 'Share folder %s through NFS' % file.get_name())
		item.set_property('icon', 'folder-remote')
		item.connect('activate', self.menu_activate_cb, file)
		return item,

	def get_background_items(self, window, file):
		if not file:
			return
		filename = urllib.unquote(file.get_uri()[7:])
		if filename.startswith(self.net_folder):
			return

		item = nautilus.MenuItem('nfs-share::background-share',
								 'Share this folder through NFS...',
								 'Share folder %s through NFS' % file.get_name())
		item.set_property('icon', 'folder-remote')
		item.connect('activate', self.menu_background_activate_cb, file)
		return item,
		
	def get_toolbar_items(self, window, file):
		if not file:
			return
		filename = urllib.unquote(file.get_uri()[7:])
		if filename.startswith(self.net_folder):
			return
	
		item = nautilus.MenuItem('nfs-share::toolbar-share',
								 'Share this folder through NFS...',
								 'Share folder %s through NFS' % file.get_name())
		item.set_property('icon', 'folder-remote')
		item.connect('activate', self.menu_background_activate_cb, file)
		return item,		
