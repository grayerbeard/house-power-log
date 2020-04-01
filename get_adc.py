import Adafruit_ADS1x15
import time
from datetime import datetime
from math import sqrt
from text_buffer import class_text_buffer

class class_get_adc(object):
	# Rotating Buffer Class
	# Initiate with just the size required Parameter
	# Get data with just a position in buffer Parameter
#	def __init__(self,scan_size,channel,config,default_gain,top_limit,bottom_limit,input_offset_mv,input_amp_gain,CT_resister,CT_ratio):
	def __init__(self,config):
		#initialization
		#self.__config = config
		
		self.__adc=Adafruit_ADS1x15.ADS1015()
		
		self.gain = config.adc_default_gain

		self.scan_size =  config.adc_scan_size
		self.__channel = config.adc_channel
		self.__top_limit = config.adc_top_limit
		self.__bottom_limit = config.adc_bottom_limit 
		self.__input_offset_mv = config.adc_input_offset_mv
		self.__input_amp_gain = config.adc_input_amp_gain
		self.__CT_resister = config.CT_resister
		self.__CT_ratio = config.CT_ratio

		self.reading = [0.0]*(self.scan_size + 1)
		self.adc_milli_volts = [0.0]*(self.scan_size + 1)
		self.input_milli_volts = [0.0]*(self.scan_size + 1)
		self.peak_current = [0.0]*(self.scan_size + 1)
		self.rms_current = [0.0]*(self.scan_size + 1)
		self.reading_time = [0.0]*(self.scan_size + 1)
		self.reading_gain = [self.gain]*(self.scan_size + 1)
		self.scan_interval =  [0.1]*(self.scan_size + 1)
		self.gain_change_count = 0

		headings = ["Time","Time Step","gain","Reading","adc Milli Volts","Input mv","I","Irms" ] 
		self.__adc_buffer = class_text_buffer(headings,config)
            

	def do_scan(self,do_resets,change_limit,debug_flag):
		self.gain_change_count = 0
		scan_count = 0
		time_from_gain_change = 0.0
		reading_ac_max = 0
		last_time = datetime.now()
		rms_current_total = 0.001
		rms_totaller_count = 0
		rms_totaler_enable = False

		rms_totaller_cycle_count = -1
		while scan_count < self.scan_size:
			#print(rms_totaler_enable)
			self.reading_gain[scan_count] = self.gain
			#self.reading[scan_count] = self.__adc.read_adc_difference(self.__channel,gain = self.gain)
			self.reading[scan_count] = self.__adc.read_adc(self.__channel,gain = self.gain)
			if abs(self.reading[scan_count]) > reading_ac_max:
				reading_ac_max = abs(self.reading[scan_count])
			self.reading_time[scan_count] = self.reading_time[scan_count-1] + self.scan_interval[scan_count]
			self.adc_milli_volts[scan_count] = (self.reading[scan_count] * 2/self.reading_gain[scan_count]) - self.__input_offset_mv
			self.input_milli_volts[scan_count] = self.adc_milli_volts[scan_count] / self.__input_amp_gain
			self.peak_current[scan_count] = self.input_milli_volts[scan_count]/self.__CT_resister/self.__CT_ratio
			#Check for just been a zero crossing negative to positive
			if True: # rms_totaler_enable:
				rms_current_total = rms_current_total + (self.peak_current[scan_count] * self.peak_current[scan_count])
			#print(round((self.peak_current[scan_count] * self.peak_current[scan_count]),2),round(self.peak_current[scan_count],2),rms_current_total)
			if True: #(self.peak_current[scan_count] * self.peak_current[scan_count-1] < 0) and (self.peak_current[scan_count] > 0) : 
				rms_totaler_enable = True
				rms_totaller_cycle_count +=1
				self.rms_current[scan_count] = 2 * sqrt(rms_current_total/(scan_count+1))
			elif scan_count == 0:
				self.rms_current[scan_count] = 0
			else:
				self.rms_current[scan_count] = self.rms_current[scan_count-1]
			this_time = datetime.now()
			self.scan_interval[scan_count] = 1000*((this_time - last_time ).total_seconds())
			time_from_gain_change = time_from_gain_change + self.scan_interval[scan_count]
			last_time = this_time
			if debug_flag : print("#:%3d,Time:%6.2f,Gain:%2d,adcRdg:%5d,adcIn_mv:%5.2f, \
mvIn:%5.2f,Ipk%5.2f,rms:%5.2f" %
(scan_count,self.reading_time[scan_count],self.gain,self.reading[scan_count],self.adc_milli_volts[scan_count],
self.input_milli_volts[scan_count],self.peak_current[scan_count],self.rms_current[scan_count]))
			if abs(self.reading[scan_count]) > self.__top_limit and (self.gain > 1) and self.gain_change_count < change_limit:
				self.gain = int(self.gain/2)
				self.gain_change_count += 1
				rms_current_total = 0
				reading_ac_max = 0
				time_from_gain_change = 0
				if do_resets: 
					scan_count = -1
					# rms_current_total = 0
					rms_totaler_enable = False
					self.rms_current[scan_count] = 0
			elif time_from_gain_change > 60 and (reading_ac_max < self.__bottom_limit) and (self.gain_change_count < change_limit) and (self.gain < 16):
				self.gain = int(self.gain*2)
				self.gain_change_count += 1
				rms_current_total = 0
				reading_ac_max = 0
				time_from_gain_change = 0
				if do_resets: 
					scan_count = -1
					# rms_current_total = 0
					rms_totaler_enable = False
					self.rms_current[scan_count] = 0
			scan_count += 1
		return self.gain_change_count

	def do_log(self,debug_flag):
		for rc in range(1,self.scan_size,1):
#                0        1        2       3          4                5       6    7    8             9            10      11
#headings = ["Time","Time Step","gain","Reading","adc Milli Volts","Input mv","I","Irms"    
			self.__adc_buffer.line_values[0] = str(self.reading_time[rc])
			self.__adc_buffer.line_values[1] = str(self.scan_interval[rc])
			self.__adc_buffer.line_values[2] = str(self.reading_gain[rc])
			self.__adc_buffer.line_values[3] = str(self.reading[rc])
			self.__adc_buffer.line_values[4] = str(self.adc_milli_volts[rc])  
			self.__adc_buffer.line_values[5] = str(round(self.input_milli_volts[rc],3))  
			self.__adc_buffer.line_values[6] = str(round(self.peak_current[rc],3))
			self.__adc_buffer.line_values[7] = str(round(self.rms_current[rc],3))
			#	self.__adc_buffer.line_values[7] = str(current_rms[rc])
			#	self.__adc_buffer.line_values[8] = str(current[rc])
			#	self.__adc_buffer.line_values[9] = str(zero_crossing[rc])
			#	self.__adc_buffer.line_values[10] = "Spare1 "
			#	self.__adc_buffer.line_values[11] = "Spare2 "

		self.__adc_buffer.just_log(True,0,self.reading_time[rc],1234)
