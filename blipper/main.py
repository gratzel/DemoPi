#!/usr/bin/env python

from settings import Settings
from logger import Logger
from blipper import *
from display import *

ch_offsets = [0, 0, 0]

rssi_slowcount = 1

def my_callback(addr,value,rssi):
  global ch_offsets, rssi_slowcount
  #print "Ch" + str(addr) + " = " + str(value)
  obj = [myApp.root.bar_red, myApp.root.bar_green, myApp.root.bar_yellow][addr]
  # check flag value for returning from sleep
  if value==34661:
    ch_offsets[addr] = obj.bar_value
    value = 0
  # convert to signed
  if value >= 32728:
    value = value-65536
  new_value = value + ch_offsets[addr]
  new_value = max(0,new_value)
  #new_value = min(100,new_value)
  if new_value != obj.bar_value:
    obj.bar_value = new_value
    obj.bar_text = str(new_value)
  # display rssi
  if rssi_slowcount <= 0:
    myApp.root.bar_blue.bar_text = str(rssi) + " dBm"
    myApp.root.bar_blue.bar_value = 1.5*(92+rssi)
    rssi_slowcount = 8
  else:
    rssi_slowcount -= 1


ENABLE_SCANNER = True

def main():
  global myApp, ENABLE_SCANNER
  try:
    #Read config file
    settings=Settings()
    #pdb.set_trace()
  
    #Set up logger
    logger=Logger(settings)

    #Create scanner
    if ENABLE_SCANNER:
      scanner=Scanner(settings,logger,my_callback)
      #Begin scanning
      scanner.StartScan()

    myApp = BlipperApp()
    myApp.run()
    logger.log("app completed")
    
  except KeyboardInterrupt:
    pass
    #scanner.StopScanning()

  if ENABLE_SCANNER:
    scanner.StopScan()

if __name__ == "__main__":
  main()
    
    
