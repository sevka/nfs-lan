#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#		nfs-share.py
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

"""NFS share class for /etc/exports manipulation"""
import sys
import shutil
from commands import *
import os

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
