#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	nfs-share.py
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

"""NFS share dialog window"""
import sys
import shutil
from commands import *
import os
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)
import gio

class ExportsSharing:
	"""Class for /etc/exports manipulation"""
	def __init__(self, folder):
		self.exportsFile = "/etc/exports"
		#self.exportsFile = "/home/sevka/projects/nfs-share/exports"
		self.lineNo = -1;
		self.folder = folder
		self.shared = False
		self.writable = False
		file = open(self.exportsFile, "r")
		lines = file.readlines()
		file.close()
		l = 0;
		for line in lines:
			if (not line.startswith("#")):
				if (line.startswith(self.folder) and (line[len(self.folder)] == " " or line[len(self.folder)] == "\t")):
					self.lineNo = l
					self.shared = True
					if ("*(rw," in line):
						self.writable = True
			l = l + 1
	
	def isShared(self):
		return self.shared
		
	def isWritable(self):
		return self.writable
	
	def restartNFS(self):
		getoutput('exportfs -arv')
		#getoutput('touch /home/sevka/projects/nfs-share/a.txt')
	
	def share(self, writable):
		if not self.backupExports():
			return False
		if writable:
			configString = "*(rw,async,subtree_check)"
		else:
			configString = "*(ro,async,subtree_check)"
			
		if (not self.isShared()):
			try:
				file = open(self.exportsFile, "a")
				print >> file, self.folder + "\t" + configString
				return True
			except:
				return False
		else:
			file = open(self.exportsFile, "r")
			lines = file.readlines()
			file.close()
			lines[self.lineNo] = self.folder + "\t" + configString + "\n"
			try:
				file = open(self.exportsFile, "w")
				file.truncate()
				file.writelines(lines)
				file.close
				return True
			except:
				return False
	
	def unshare(self):
		if not self.backupExports():
			return False
		file = open(self.exportsFile, "r")
		lines = file.readlines()
		file.close()
		del lines[self.lineNo]
		try:
			file = open(self.exportsFile, "w")
			file.truncate()
			file.writelines(lines)
			file.close
			return True
		except:
			return False
	
	def backupExports(self):
		try:
			shutil.copyfile(self.exportsFile, self.exportsFile + "~")
			return True
		except:
			return False
#-------------------------------------------------------------------------------
class NfsShareWindow(gtk.Window):
	'''
	"Share" window 
	'''
	def __init__(self, folder):
		'''
		Constructor. GUI
		'''
		self.folder = folder
		
		gtk.Window.__init__(self)
		self.set_modal(True)
		self.set_default_size(500,200)
		self.set_title('Share folder through NFS')
		mainVBox = gtk.VBox(False, 10)
		mainHBox = gtk.HBox(False, 10)
		
		self.fileLabel = gtk.Label('file')
		infoVBox = gtk.VBox(False, 10)
		infoVBox.pack_start(gtk.Label('Share this folder through NFS'), False, False, 10)
		infoVBox.pack_start(self.fileLabel, True, True, 10)
		
		image = gtk.image_new_from_gicon(gio.ThemedIcon('folder-remote'),gtk.ICON_SIZE_DIALOG)
		mainHBox.pack_start(image, False, False, 30)
		mainHBox.pack_start(infoVBox, True, True, 10)
		
		self.shareCheckBtn = gtk.CheckButton('Share this folder')
		self.writeCheckBtn = gtk.CheckButton('Allow other users to create, update and delete files')
		mainVBox.set_border_width(10)
		self.okBtn = gtk.Button('', gtk.STOCK_OK)
		self.cancelBtn = gtk.Button('', gtk.STOCK_CANCEL)
		btnBox = gtk.HButtonBox()
		btnBox.add(self.okBtn)
		btnBox.add(self.cancelBtn)
		btnBox.set_layout(gtk.BUTTONBOX_END)
		btnBox.set_spacing(10)
		
		mainVBox.pack_start(mainHBox, True, True)
		mainVBox.pack_start(self.shareCheckBtn, False, False)
		mainVBox.pack_start(self.writeCheckBtn, False, False)
		mainVBox.pack_start(gtk.HSeparator(), False, False)
		mainVBox.pack_start(btnBox, False, False)		
		
		self.shareCheckBtn.connect('toggled', self.on_shareCheckBtn_toggled)
		self.writeCheckBtn.connect('toggled', self.on_writeCheckBtn_toggled)
		self.okBtn.connect('clicked', self.on_okBtn_clicked)
		self.cancelBtn.connect('clicked', self.on_cancelBtn_clicked)		
		self.connect('destroy', self.on_cancelBtn_clicked)
		
		self.add(mainVBox)
		
		self.es = ExportsSharing(self.folder)
		self.shareCheckBtn.set_active(self.es.isShared())
		self.writeCheckBtn.set_active(self.es.isWritable())
		self.fileLabel.set_label(self.folder)
		self.on_cb_toggled()

	def _errorMessage(self, message):
		'''
		Error message dialog
		'''
		self.dialogError = gtk.MessageDialog(self, gtk.DIALOG_MODAL |  gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
		self.dialogError.set_default_response(gtk.RESPONSE_OK)
		self.dialogError.connect('response', self._dialogError_closed)
		self.dialogError.show_all()
		
	def _dialogError_closed(self, *args):
		'''
		Error dialog closing
		'''
		self.dialogError.destroy()
		gtk.main_quit()

	def on_okBtn_clicked(self, widget):
		'''
		Ok button callback
		'''
		if (self.shareCheckBtn.get_active()):
			if not self.es.share(self.writeCheckBtn.get_active()):
				self._errorMessage("Error occured while sharing")
			else:
				self.es.restartNFS()
				gtk.main_quit()
		else:
			if not self.es.unshare():
				self._errorMessage("Error occured while unsharing")
			else:
				self.es.restartNFS()
				gtk.main_quit()

	def on_cancelBtn_clicked(self, widget):
		'''
		Cancel button callback
		'''
		gtk.main_quit()

	def on_shareCheckBtn_toggled(self, widget):
		'''
		Share checkbox toggle
		'''
		if self.shareCheckBtn.get_active() == True:
			self.writeCheckBtn.set_sensitive(1)
		else:
			self.writeCheckBtn.set_sensitive(0)
		self.on_cb_toggled()

	def on_writeCheckBtn_toggled(self, widget):
		'''
		"Allow write" checkbox toggle
		'''
		self.on_cb_toggled()
	
	def on_cb_toggled(self):
		'''
		Enable/disable Ok button on toggle checkboxes
		'''
		if (self.shareCheckBtn.get_active() != self.es.isShared() or self.writeCheckBtn.get_active() != self.es.isWritable()):
			self.okBtn.set_sensitive(1)
		else:
			self.okBtn.set_sensitive(0)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Folder doesn't specified"
	else:
		folder = sys.argv[1]
		a = NfsShareWindow(folder)
		a.show_all()
		gtk.gdk.threads_init()
		gtk.main()
	

