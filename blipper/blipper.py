#!/usr/bin/env python
import pexpect
import subprocess
import thread
from multiprocessing.pool import ThreadPool
import time
from settings import Settings
import requests
import json
from logger import Logger
import pdb
import threading

class Scanner():
  HCI_TIMEOUT = 1

  def __init__(self,settings,logger,callback):
    self._logger=logger
    self._bleScanProc = None
    self._scanProc=None
    self._addrToRssi={}
    self._keepScanning=True
    self._settings=settings
    self._lastFetch=None
    self._addresses=None
    self._readTimeout=5
    self._callback = callback
    try:
      self.log("Loading addresses")
      json_data=open("addresses.cfg").read()
      resp = json.loads(json_data)
      self._addresses = resp
    except Exception,error:
      self.log("Error loading addresses: "+str(error)+".")
  
  def log(self,data):
    self._logger.log(data)
      
  def getAddresses(self,type=None):
    
    if self._addresses:
      if(type is None):  
        return self._addresses
      elif(type is "all"):
        return dict(self._addresses["ble"].items() + self._addresses["disc"].items()+self._addresses["nonDisc"].items())
      else:
        return self._addresses[type]
    else:
      return []

  def report_blipper(self,addr,value,rssi):
    #if(addr in self.getAddresses("ble")):
      #self._addrToRssi[addr]=rssi;
      #self.log("Ch" + str(addr) + " = " + str(value))
      #print "Ch" + str(addr) + " = " + str(value)
      self._callback(addr,value,rssi)
    
    
  def scanProcessSpawner(self):
    while self._keepScanning:
      self._scanProc = subprocess.Popen(['hcitool', 'scan'],cwd='/usr/bin',stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
      self._scanProc.wait()
      if(self._readTimeout>0):
        time.sleep(self._readTimeout)
   
    
      
  def bleScanProcessSpawnerAsync(self):
    self._bleScanProc = subprocess.Popen(['hcitool', 'lescan', '--duplicates'],cwd='/usr/bin',stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    
  def parseHcidump(self):
    self.log("Starting parse of hcidump stdout")
    child=pexpect.spawn("hcidump -R",timeout=self.HCI_TIMEOUT)
    #child=pexpect.spawn("./test.sh",timeout=None)    
    while self._keepScanning:
      try:
        # wait for a MAC address match
        #child.expect("(([0-9A-F]{2}[:-]){5}([0-9A-F]{2}))",timeout=None)
        # wait for a pattern match
        #child.expect("35 65 78 74 ([0-9A-F]{2})",timeout=None)
        
        #wait for mfg id match
        child.expect("70 08 FF D6 01 ",timeout=self.HCI_TIMEOUT)
        #After a match is found the instance attributes 'before', 'after' and
        #'match' will be set. You can see all the data read before the match in
        #'before'. You can see the data that was matched in 'after'.  
        #match=child.after
        #print "match=",match,

        #skip first three bytes of payload
        child.expect("([0-9A-F]{2}[ ]){3}",timeout=self.HCI_TIMEOUT)
        dont_care=child.after
        channel = int(dont_care[1:2],16)
        #print " channel=",channel,

        #capture last two bytes of payload
        child.expect("([0-9A-F]{2}[ ]){2}",timeout=self.HCI_TIMEOUT)
        raw_data=child.after
        dehex_data = int(raw_data[3:5]+raw_data[0:2],16)
        #print " data=",hex

        #wait for precursor to rssi match
        child.expect("70 65 72 ",timeout=self.HCI_TIMEOUT)
        child.expect("([0-9A-F]{2})",timeout=self.HCI_TIMEOUT)
        raw_data=child.after
        rssi = int(raw_data,16)-256

        # wait for an RSSI value match
        #child.expect("(-\d{2})",timeout=None)
        #rssi=child.after
        #print " RSSI= ",rssi
    
        #if(addr in self._addrToRssi):
        #  if (rssi!=self._addrToRssi[addr]):
        #    self.report_blipper(addr,rssi)
        #else:
        self.report_blipper(channel, dehex_data, rssi)
      except:
        pass
        
  def StartHciMonitor(self):
    self.log(json.dumps(self.getAddresses(), indent=4))
    self.log("Spawning BLE scan child proccess")
    self.bleScanProcessSpawnerAsync()
    self.parseHcidump()
        
  def StopScan(self):
    self._keepScanning=False
    self.log("Killing low energy scan child process")
    self.log(self._bleScanProc.pid)
    try: self._bleScanProc.terminate()
    except(OSError): pass
    self.log("Killed.")

  def StartScan(self):
    # starts or restarts the thread machinery
    self.thread = threading.Thread(target=self.StartHciMonitor)  
    self.stop = False
    self.thread.start()

def my_callback(addr,value,rssi):
    print "Ch" + str(addr) + " = " + str(value) + " RSSI=" + str(rssi)

def main():
  try:
    #Read config file
    settings=Settings()
    #pdb.set_trace()
  
    #Set up logger
    logger=Logger(settings)

    #Create scanner
    scanner=Scanner(settings,logger,my_callback)

    #Begin scanning
    #scanner.StartScanning()
    scanner.StartScan()
    while True:
      pass
    
  except KeyboardInterrupt:
    scanner.StopScan()
  
if __name__ == "__main__":
  main()
    
  	
