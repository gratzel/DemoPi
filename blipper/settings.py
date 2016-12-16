#!/usr/bin/env python

import os.path
import ConfigParser

class Settings():
	def __init__(self):
		#Set defaults
		self.readTimeout_BLE=5
	
		self.logging_File="blipper.log"
		self.logging_MaxSize=1024*1024 # 1MB
		self.logging_FileCount=5
		self.logging_UseLog=False
		self.logging_STDOUT=True
		
		
		if not os.path.isfile("blipper.ini"):
			raise "Error reading configuration file"
		
		Config = ConfigParser.ConfigParser()
		Config.read("blipper.ini")

		try: self.readTimeout_BLE=Config.get("Read Timeout","ble") 
		except: pass

		try: self.logging_File=Config.get("Logging","file") 
		except: pass
		try: self.logging_MaxSize=Config.get("Logging","maxsize") 
		except: pass
		try: self.logging_FileCount=Config.get("Logging","filecount") 
		except: pass
		try: self.logging_UseLog=Config.getboolean("Logging","uselog") 
		except: pass
		try: self.logging_STDOUT=Config.getboolean("Logging","stdout") 
		except: pass
