#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   for use with Python 3

#	cpu_monitor_config.py module for the config class
#   testing in shed version OK in sauna
#  
#	This program is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; either version 2 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNimport sys, getoptESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#  
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software
#	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	MA 02110-1301, USA.

# Standard library imports
from configparser import RawConfigParser
from csv import DictReader as csv_DictReader
from csv import DictWriter as csv_DictWriter
#from datetime import datetime
#from shutil import copyfile
#from ftplib import FTP
#from sys import argv as sys_argv
from sys import exit as sys_exit
#import socket
from os import path
from sys import argv as sys_argv
# Local application imports
from utility import pr,make_time_text,send_by_ftp,str2bool

class class_config:
	def __init__(self):
# Start of items set in config.cfg
	# Debug
		self.debug_reread_config = False   
		self.debug_flag_1 = False
		self.debug_flag_2 = False
		self.debug_flag_ftp = False
	# Scan
		self.scan_delay = 10		# delay in seconds between each scan (not incl sensor responce times)
		self.max_scans = 0			# number of scans to do, set to zero to scan for ever (until type "ctrl C")
	# Log
		self.log_directory = "log/"	# where to store log files
		self.local_dir_www = "/var/www/html/" # default value for local web folder
		self.log_buffer_flag = True	 # whether to generate the csv log file as well as the html text file	
		self.text_buffer_length = 15	# number of lines in the text buffer in the html file	
	# Ftp
		self.ftp_creds_filename = "/home/pi/ftp_creds/ftp_creds.csv"
		self.ftp_log_max_count  = 5
		self.ftp_timeout = 0.5
		self.ftplog = 0		# Number of Value Changes before Log File is Saved to remote website, 0 means every change
	# Heating Fan
		self.heat_max_temp =  16
		self.heat_min_temp =  15
		self.heat_min_speed =  20
		self.heat_max_speed =  100
		self.heat_min_freq =  6
		self.heat_max_freq =  6
	# Sauna
		self.sauna_max_temp =  69.0
		self.sauna_min_temp = 61.0 
		self.sauna_min_speed = 75
		self.sauna_max_speed = 90
		self.sauna_min_freq = 2.0
		self.sauna_max_freq = 5.0
		self.sauna_GPIO_port = 18
		self.sauna_brightness = 80
	# Power Log
		self.adc_scan_size = 100
		self.adc_target_scan_msec = 80
		self.adc_channel = 3
		self.adc_default_gain = 1
		self.adc_top_limit = 2000
		self.adc_bottom_limit = 950
		self.adc_input_offset_mv = 0 # 27.6518 #23.2184 # 26.62 # tested for channel 3
		self.adc_input_amp_gain = 9.48 # tested for channel 3
		self.adc_CT_ratio = 1 # mAmps out to Amps in.
		self.adc_CT_resister = 22
# End of items set in config.cfg	

		# Based on the program name work out names for other files
		# First three use the program pathname	
		self.prog_path = path.dirname(path.realpath(__file__)) + "/"
		self.prog_name = str(sys_argv[0][:-3])
		self.config_filename = "config.cfg"
		print("Program Name is : ",self.prog_name)
		print("config file is : ",self.config_filename)

	def read_file(self):
		here = "config.read_file"
		config_read = RawConfigParser()
		config_read.read(self.config_filename)
		section = "Debug"
		self.debug_reread_config = str2bool(config_read.get(section, 'debug_reread_config'))
		self.debug_flag_1 = str2bool(config_read.get(section, 'debug_flag_1'))
		self.debug_flag_2 = str2bool(config_read.get(section, 'debug_flag_2'))
		self.debug_flag_ftp = str2bool(config_read.get(section, 'debug_flag_ftp'))
		section = "Scan"
		self.scan_delay = float(config_read.get(section, 'scan_delay')) 
		self.max_scans = float(config_read.get(section, 'max_scans'))
		section = "Log"
		self.log_directory = config_read.get(section, 'log_directory')
		self.local_dir_www = config_read.get(section, 'local_dir_www')
		self.log_buffer_flag = config_read.getboolean(section, 'log_buffer_flag')
		self.text_buffer_length  = int(config_read.get(section, 'text_buffer_length'))		
		section = "Ftp"
		self.ftp_creds_filename = config_read.get(section, 'ftp_creds_filename') 
		self.ftp_log_max_count = float(config_read.get(section, 'ftp_log_max_count'))
		section = "Heating_Fan"
		self.heat_max_temp =  float(config_read.get(section, 'heat_max_temp'))
		self.heat_min_temp =  float(config_read.get(section, 'heat_min_temp'))
		self.heat_max_speed =  float(config_read.get(section, 'heat_max_speed'))
		self.heat_min_speed =  float(config_read.get(section, 'heat_min_speed'))
		self.heat_max_freq =  float(config_read.get(section, 'heat_max_freq'))
		self.heat_min_freq =  float(config_read.get(section, 'heat_min_freq'))
		section = "Sauna"
		self.sauna_max_temp = float(config_read.get(section, 'sauna_max_temp'))
		self.sauna_min_temp = float(config_read.get(section, 'sauna_min_temp'))
		self.sauna_max_speed =  float(config_read.get(section, 'sauna_max_speed'))
		self.sauna_min_speed =  float(config_read.get(section, 'sauna_min_speed'))
		self.sauna_max_freq = float(config_read.get(section, 'sauna_max_freq'))
		self.sauna_min_freq = float(config_read.get(section, 'sauna_min_freq'))
		self.sauna_GPIO_port  =  float(config_read.get(section, 'sauna_GPIO_port'))
		self.sauna_brightness = float(config_read.get(section, 'sauna_brightness'))
		section = "Power_Log"
		self.adc_scan_size  =  int(config_read.get(section, 'adc_scan_size'))
		self.adc_target_scan_msec  =  int(config_read.get(section, 'adc_target_scan_msec'))
		self.adc_channel  =  int(config_read.get(section, 'adc_channel'))
		self.adc_default_gain  =  int(config_read.get(section, 'adc_default_gain'))
		self.adc_top_limit  =  int(config_read.get(section, 'adc_top_limit'))
		self.adc_bottom_limit  =  int(config_read.get(section, 'adc_bottom_limit'))
		self.adc_input_offset_mv  =  float(config_read.get(section, 'adc_input_offset_mv'))
		self.adc_input_amp_gain  =  float(config_read.get(section, 'adc_input_amp_gain'))
		self.adc_CT_ratio  =  float(config_read.get(section, 'adc_CT_ratio')) 
		self.adc_CT_resister  =  float(config_read.get(section, 'adc_CT_resister'))
		return

	def write_file(self):
		here = "config.write_file"
		config_write = RawConfigParser()
		section = "Debug"
		config_write.add_section(section)
		config_write.set(section, 'debug_reread_config',self.debug_reread_config)
		config_write.set(section, 'debug_flag_1',self.debug_flag_1)
		config_write.set(section, 'debug_flag_2',self.debug_flag_2)
		config_write.set(section, 'debug_flag_ftp',self.debug_flag_ftp)
		section = "Scan"
		config_write.add_section(section)
		config_write.set(section, 'scan_delay',self.scan_delay)
		config_write.set(section, 'max_scans',self.max_scans)
		section = "Log"
		config_write.add_section(section)
		config_write.set(section, 'log_directory',self.log_directory)
		config_write.set(section, 'local_dir_www',self.local_dir_www)
		config_write.set(section, 'log_buffer_flag',self.log_buffer_flag)
		config_write.set(section, 'text_buffer_length',self.text_buffer_length)	
		section = "Ftp"
		config_write.add_section(section)
		config_write.set(section, 'ftp_creds_filename',self.ftp_creds_filename)
		config_write.set(section, 'ftp_log_max_count',self.ftp_log_max_count)
		section = "Heating_Fan"
		config_write.add_section(section)
		config_write.set(section, 'heat_max_temp',self.heat_max_temp)
		config_write.set(section, 'heat_min_temp',self.heat_min_temp)
		config_write.set(section, 'heat_max_speed',self.heat_max_speed)
		config_write.set(section, 'heat_min_speed',self.heat_min_speed)
		config_write.set(section, 'heat_max_freq',self.heat_max_freq)
		config_write.set(section, 'heat_min_freq',self.heat_min_freq)
		section = "Sauna"
		config_write.add_section(section)
		config_write.set(section, 'sauna_max_temp',self.sauna_max_temp)
		config_write.set(section, 'sauna_min_temp',self.sauna_min_temp)
		config_write.set(section, 'sauna_max_speed',self.sauna_max_speed)
		config_write.set(section, 'sauna_min_speed',self.sauna_min_speed)
		config_write.set(section, 'sauna_max_freq',self.sauna_max_freq)
		config_write.set(section, 'sauna_min_freq',self.sauna_min_freq)
		config_write.set(section, 'sauna_GPIO_port',self.sauna_GPIO_port)
		config_write.set(section, 'sauna_brightness',self.sauna_brightness)
		section = "Power_Log"
		config_write.add_section(section)
		config_write.set(section, 'adc_scan_size',self.adc_scan_size)
		config_write.set(section, 'adc_target_scan_msec',self.adc_target_scan_msec)
		config_write.set(section, 'adc_channel',self.adc_channel)
		config_write.set(section, 'adc_default_gain ',self.adc_default_gain )
		config_write.set(section, 'adc_top_limit',self.adc_top_limit)
		config_write.set(section, 'adc_bottom_limit',self.adc_bottom_limit)
		config_write.set(section, 'adc_input_offset_mv',self.adc_input_offset_mv)
		config_write.set(section, 'adc_input_amp_gain',self.adc_input_amp_gain)
		config_write.set(section, 'adc_CT_ratio',self.adc_CT_ratio)
		config_write.set(section, 'adc_CT_resister',self.adc_CT_resister)
		
		# Writing our configuration file to 'self.config_filename'
		pr(self.debug_flag_1, here, "ready to write new config file with default values: " , self.config_filename)
		with open(self.config_filename, 'w+') as configfile:
			config_write.write(configfile)
		return 0

	def print_config(self):
		here = "config.print_config"
		print("\n                   Section Debug")
		print("  config.debug_reread_config is: ",self.debug_reread_config)   
		print("         config.debug_flag_1 is: ",self.debug_flag_1)
		print("         config.debug_flag_2 is: ",self.debug_flag_2)
		print("       config.debug_flag_ftp is: ",self.debug_flag_ftp)
		print("\n                    Section Scan")
		print("           config.scan_delay is: ",self.scan_delay)
		print("           config.max_scans  is: ",self.max_scans)
		print("\n                     Section Log")
		print("       config.log_directory  is: ",self.log_directory)
		print("       config.local_dir_www  is: ",self.local_dir_www)
		print("     config.log_buffer_flag  is: ",self.log_buffer_flag)
		print("  config.text_buffer_length  is: ",self.text_buffer_length)
		print("\n                     Section Ftp")
		print("  config.ftp_creds_filename  is: ",self.ftp_creds_filename)
		print("    config.ftp_log_max_count is: ",self.ftp_log_max_count)
		print("         config.ftp_timeout  is: ",self.ftp_timeout)
		print("              config.ftplog  is: ",self.ftplog)
		print("\n             Section Heating Fan")
		print("       config.heat_max_temp  is: ",self.heat_max_temp)
		print("       config.heat_min_temp  is: ",self.heat_min_temp)
		print("      config.heat_min_speed  is: ",self.heat_min_speed)
		print("      config.heat_max_speed  is: ",self.heat_max_speed)
		print("       config.heat_min_freq  is: ",self.heat_min_freq)
		print("       config.heat_max_freq  is: ",self.heat_max_freq)
		print("\n                   Section Sauna")
		print("      config.sauna_max_temp  is: ",self.sauna_max_temp)
		print("      config.sauna_min_temp  is: ",self.sauna_min_temp) 
		print("     config.sauna_min_speed  is: ",self.sauna_min_speed)
		print("     config.sauna_max_speed  is: ",self.sauna_max_speed)
		print("      config.sauna_min_freq  is: ",self.sauna_min_freq)
		print("      config.sauna_max_freq  is: ",self.sauna_max_freq)
		print("    config.sauna_brightness  is: ",self.sauna_brightness)
		print("\n               Section Power Log")
		print("       config.adc_scan_size  is: ",self.adc_scan_size)
		print("config.adc_target_scan_msec  is: ",self.adc_target_scan_msec)
		print("         config.adc_channel  is: ",self.adc_channel)
		print("   config.adc_default_gain)  is: ",self.adc_default_gain)
		print("       config.adc_top_limit  is: ",self.adc_top_limit)
		print("    config.adc_bottom_limit  is: ",self.adc_bottom_limit)
		print(" config.adc_input_offset_mv  is: ",self.adc_input_offset_mv)
		print("  config.adc_input_amp_gain  is: ",self.adc_input_amp_gain)
		print("        config.adc_CT_ratio  is: ",self.adc_CT_ratio)
		print("     config.adc_CT_resister  is: ",self.adc_CT_resister)

	def check_reread_flag(self):
		here = "config.read_file"
		config_read = RawConfigParser()
		config_read.read(self.config_filename)
		section = "Debug"
		return str2bool(config_read.get(section, 'debug_reread_config'))

	def reset_reread_flag(self):
		here = "reset_reread_flag"
		self.debug_reread_config = False
		self.write_file()
		#config_write = RawConfigParser()
		#section = "Debug"
		#config_write.set(section, 'debug_reread_config',False)
		#self.debug_reread_config = False
