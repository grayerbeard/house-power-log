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
from math import sqrt


#from ads_lib import ADS1015
#GAIN = 1
##import ADS1115
#import Adafruit_ADS1x15


from datetime import datetime

# Local application imports
from utility import pr,make_time_text,send_by_ftp
from text_buffer import class_text_buffer
from config import class_config
from get_adc import class_get_ads

scan_size = 200
diff_channel = 3
top_limit = 2020
bottom_limit = 980
config = class_config()
adc = class_get_ads(scan_size,diff_channel,config,top_limit,bottom_limit)

headings = ["Time","Time Step","Gain","Reading"] #"Rdg13","Rdg23","ac03","ac13","AC23"] # "currents RMS","Current","ZeroCrosses","Spare1","Spare2"]
analog_buffer = class_text_buffer(headings,config)

#reading_0_3 = [0.0]*(scan_size + 1)
#reading_1_3 = [0.0]*(scan_size + 1)
#reading_2_3 = [0.0]*(scan_size + 1)
#gain = [0.0]*(scan_size + 1)
#reading_ac_0_3 = [0.0]*(scan_size + 1)
#reading_ac_1_3 = [0.0]*(scan_size + 1)

#reading_ac_2_3 = [0.0]*(scan_size + 1)
#reading_square_total = [0.0]*(scan_size + 1)
#reading_ac_max = [0.0]*(scan_size + 1)
#current_rms = [0.0]*(scan_size + 1)
#current = [0.0]*(scan_size + 1)
#reading_time = [0.0]*(scan_size + 1)
#time_step = [0.0]*(scan_size + 1)
#GAIN = 1
#last_cycle_max = [0.0]*(scan_size + 1)
#zero_crossing = [0]*(scan_size + 1)


#reference = explorerhat.analog.one.read()
#reference = adc.read_adc(0, gain=GAIN)

#rc = 1
#print(reference)

not_finished = True

start_time = datetime.now()
#reading_0_3[0] = adc.read_adc_difference(1,gain = GAIN)
#reading_1_3[0] = adc.read_adc_difference(2,gain = GAIN)
#reading_2_3[0] = adc.read_adc_difference(3,gain = GAIN)#Read the difference between two ADC channels and return the ADC value
#as a signed integer result.  Differential must be one of:
#   - 0 = Channel 0 minus channel 1    not used this project 
#   - 1 = Channel 0 minus channel 3    original buffered   
#   - 2 = Channel 1 minus channel 3    amp 1 gain xx   
#   - 3 = Channel 2 minus channel 3    amp /2 gain xx
reading_time[0] = 1000*(datetime.now() - start_time).total_seconds()

GAIN = int(1)

gain_scan = 0
gain_scan_limit = int(scan_size/5)

cal0 = 1 # 2
cal1 = 1 #-0.593
cal2 = 1 # 0.172
offset0 = 0 #-0.625
offset1 = 0 # 3.375
offset2 = 0 # -12 



#print( reference)
adc.read_adc_difference

read_time = (end_time - start_time).total_seconds()

for rc in range(0,scan_size+1,1):
	#if rc >=1:
		#reading_ac[rc] = abs(reading[rc])
		#if reading_ac[rc]>reading_ac_max["Date_time","Time Step","gain","Rdg01","Rdg23","ac01","ac23,"currents RMS","Current","ZeroCrosses","Spare1","Spare2"rc-1]:
		#	reading_ac_max[rc] = abs(reading[rc])
		#else:
		#	reading_ac_max[rc] = reading_ac_max[rc-1]
		#if reading_ac[rc]>reading_ac_0_1_max[rc-1]:
		#	reading_ac_max[rc] = abs(reading[rc])
		#else:
		#	reading_ac_max[rc] = reading_ac_max[rc-1]
		#time_step[rc] = 1000*(reading_time[rc]- reading_time[rc-1]).total_seconds()
		#reading_square_total[rc] = reading_square_total[rc-1] + (reading_ac[rc] * reading_ac[rc])
		#current_rms[rc] =  20.826*sqrt(reading_square_total[rc]/rc)
		#current[rc] = 14.598 * reading_ac_max[rc]

#                0           1          2       3       4       5       6     7      8             9            10      11
#headings = ["Date_time","Time Step","gain","Rdg003","Rdg13","Rdg23","ac03","ac13","AC23"]       currents RMS","Current"       ,"ZeroCrosses","Spare1","Spare2"]
	analog_buffer.line_values[0] = str(reading_time[rc])
	analog_buffer.line_values[1] = str(reading_time[rc] - reading_time[rc-1])
	analog_buffer.line_values[2] = str(gain[rc])
	analog_buffer.line_values[3] = str(reading_0_3[rc])
	analog_buffer.line_values[4] = str(reading_1_3[rc])  
	analog_buffer.line_values[5] = str(reading_2_3[rc])  
	analog_buffer.line_values[6] = str(reading_ac_0_3[rc])
	analog_buffer.line_values[7] = str(reading_ac_1_3[rc])
	analog_buffer.line_values[8] = str(reading_ac_2_3[rc])
#	analog_buffer.line_values[7] = str(current_rms[rc])
#	analog_buffer.line_values[8] = str(current[rc])
#	analog_buffer.line_values[9] = str(zero_crossing[rc])
#	analog_buffer.line_values[10] = "Spare1 "
#	analog_buffer.line_values[11] = "Spare2 "
	analog_buffer.just_log(True,0,reading_time[rc],1234)

end_file_time = datetime.now()

file_time = (end_file_time - end_time).total_seconds()

print("Read Time",read_time)
print("File Time",file_time)
