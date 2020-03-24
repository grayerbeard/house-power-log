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
from utility import pr,make_time_text,send_by_ftp
from text_buffer import class_text_buffer
from config import class_config
from get_adc import class_get_adc


scan_size = 100
diff_channel = 3

default_gain = 1
top_limit = 2020
bottom_limit = 980
#input_offset_mv = -6.5  # tested for channel 2
#input_amp_gain = 100 # tested for channel 2
input_offset_mv = 19 # tested for channel 3
input_amp_gain = 10.615 # tested for channel 3
CT_ratio = 1 # mAmps out to Amps in.
CT_resister = 22


config = class_config()
adc = class_get_adc(scan_size,diff_channel,config,default_gain,top_limit,bottom_limit,input_offset_mv,input_amp_gain,CT_resister,CT_ratio)

headings = ["Time","Time Step","gain","Reading","adc Milli Volts","Input mv","I","Irms" ] 
analog_buffer = class_text_buffer(headings,config)

start_time = datetime.now()
do_resets = True
change_limit = 4
debug_flag = True
print("Change Count: ",adc.do_scan(do_resets,change_limit,debug_flag))
read_time = 1000*(datetime.now() - start_time).total_seconds()

adc.reading_time[0] = 0

for rc in range(1,adc.scan_size,1):



#                0        1        2       3          4                5       6    7    8             9            10      11
#headings = ["Time","Time Step","gain","Reading","adc Milli Volts","Input mv","I","Irms"    
	analog_buffer.line_values[0] = str(adc.reading_time[rc])
	analog_buffer.line_values[1] = str(adc.scan_interval[rc])
	analog_buffer.line_values[2] = str(adc.reading_gain[rc])
	analog_buffer.line_values[3] = str(adc.reading[rc])
	analog_buffer.line_values[4] = str(adc.adc_milli_volts[rc])  
	analog_buffer.line_values[5] = str(round(adc.input_milli_volts[rc],3))  
	analog_buffer.line_values[6] = str(round(adc.peak_current[rc],3))
	analog_buffer.line_values[7] = str(round(adc.rms_current[rc],3))
#	analog_buffer.line_values[7] = str(current_rms[rc])
#	analog_buffer.line_values[8] = str(current[rc])
#	analog_buffer.line_values[9] = str(zero_crossing[rc])
#	analog_buffer.line_values[10] = "Spare1 "
#	analog_buffer.line_values[11] = "Spare2 "
	analog_buffer.just_log(True,0,adc.reading_time[rc],1234)

end_file_time = datetime.now()

file_time = 1000*(datetime.now() - start_time).total_seconds() - read_time

print("Read Time",read_time)
print("File Time",file_time)
