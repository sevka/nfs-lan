#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#		nfs-browse.py
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

"""Browse NFS shares"""
import shutil
import os

class AvahiNFSBrowse:
	
	COMPS_ALL = 0
	COMPS_SHARES = 1
	
	def __init__(self, folder = '/net'):
		self.netFolder = folder
	
	def get_comps(self, type = 1):
		"""
		Get all workstation computer names
		:return: list 
		"""
		result = os.popen("avahi-browse -at").read()
		lines = result.splitlines()
		comps = []
		
		for line in lines:
			lineArray = line.split()
			if lineArray[-2] == 'Workstation':
				compName = lineArray[3] + ".local"
				result2 = os.popen("showmount -e " + compName).read()
				lines2 = result2.splitlines()
				if (type == self.COMPS_ALL) or (len(lines2) > 1 and lines2[0].startswith("Export list for " + compName + ":")):
					comps.append(compName)
		return comps
	
	def walk_comps(self):
		"""
		Walk through all computers with NFS shares.
		After 'cd' command, computer appears in Nautilus
		"""
		for comp in self.get_comps():
			os.system("cd " + self.netFolder + "/" + comp)

if __name__ == "__main__":
	a = AvahiNFSBrowse()
	#print a.get_comps(0)
	a.walk_comps()
	
