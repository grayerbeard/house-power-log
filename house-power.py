#!/usr/bin/env python

# File: my-analogs.py based on the pimorini sensor.py
# david Torrens March 10th 2020
# original Author; James Carlson, https://github.com/jxxcarlson
# Date: Feb 21, 2016
# Derived from code by Gisky

#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V

#Read the difference between two ADC channels and return the ADC value
#as a signed integer result.  Differential must be one of:
#   - 0 = Channel 0 minus channel 1    not used this project 
#   - 1 = Channel 0 minus channel 3    original buffered   
#   - 2 = Channel 1 minus channel 3    amp 1 gain xx   
#   - 3 = Channel 2 minus channel 3    amp /2 gain xx

import time
#from math import sqrt


#from ads_lib import ADS1015
#GAIN = 1
##import ADS1115
#import Adafruit_ADS1x15


from datetime import datetime

# Local application imports
from utility import pr,make_time_text,send_by_ftp,fileexists
#from utility_037 import fileexists,pr,make_time_text
#from text_buffer import class_text_buffer
from config import class_config
from get_adc import class_get_adc
from time import sleep as time_sleep
from sys import exit as sys_exit

config = class_config()

if fileexists(config.config_filename):		
	print( "will try to read Config File : " , config.config_filename )
	config.read_file() # overwrites from file
else : 
	config.write_file()
	print("New Config File Made with default values, you probably need to edit it")

adc = class_get_adc(config)
config.print_config()
print("\nEdit Config File, Set reread flag to True then save (Ctrl C to exit)\n")

scan_count = 0

while (scan_count < config.max_scans) or (config.max_scans == 0):
	scan_count += 1
	print("Scan: ",scan_count)
	try:
		time_sleep(config.scan_delay) 
		if config.check_reread_flag():
			print("\n ReRead Flag Set, reading new values")
			config.read_file()
			config.reset_reread_flag()
			config.print_config()
			print("\n")

		start_time = datetime.now()
		print("Change Count: ",adc.do_scan(config,do_resets=config.debug_flag_1,change_limit=4))
		read_time = 1000*(datetime.now() - start_time).total_seconds()

		adc.reading_time[0] = 0

		adc.do_log(config.debug_flag_2)

		end_file_time = datetime.now()

		file_time = 1000*(datetime.now() - start_time).total_seconds() - read_time

		print("Read Time",read_time)
		print("File Time",file_time,"\n")

	except KeyboardInterrupt:
		print(".........Ctrl+C pressed...")
		sys_exit()
