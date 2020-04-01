#!/usr/bin/env python3
# This file is part of pwm_fanshim.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :test_config.py
# description     :test config.py and config.cfg
# author          :David Torrens
# start date      :2020 04 01
# version         :0.1
# python_version  :3

from time import sleep as time_sleep
from sys import exit as sys_exit
from config import class_config
from utility import fileexists

config = class_config()

if fileexists(config.config_filename):		
	print( "will try to read Config File : " , config.config_filename )
	config.read_file() # overwrites from file
else: 
	config.write_file()
	print("New Config File Made with default values try edit it")

config.print_config()

print("\nEdit Config File, Set reread flag to True then save (Ctrl C to exit)\n")

while True:
	try:
		time_sleep(5) 
		if config.check_reread_flag():
			print("\n ReRead Flag Set, reading new values")
			time_sleep(5)
			config.read_file()
			config.reset_reread_flag()
			config.print_config()
			print("\n")
			time_sleep(5)

	except KeyboardInterrupt:
		print(".........Ctrl+C pressed...")
		sys_exit()
