import Adafruit_ADS1x15
import time
from datetime import datetime
from math import sqrt
from text_buffer import class_text_buffer

class class_get_adc(object):
	# Rotating Buffer Class
	# Initiate with just the size required Parameter
	# Get data with just a position in buffer Parameter
	def __init__(self,config):
		#initialization
		self.__adc=Adafruit_ADS1x15.ADS1015()
		self.__cnfg = config

		headings = ["Time","Time Step","gain","Reading","adc Milli Volts","Input mv","I","Irms" ] 
		self.__adc_buffer = class_text_buffer(headings,config)
		self.setup_data()
            
	def setup_data(self):
		self.reading = [0.0]*(self.__cnfg.adc_scan_size + 1)
		self.adc_milli_volts = [0.0]*(self.__cnfg.adc_scan_size + 1)
		self.input_milli_volts = [0.0]*(self.__cnfg.adc_scan_size + 1)
		self.current = [0.0]*(self.__cnfg.adc_scan_size + 1)
		self.rms_current = [0.0]*(self.__cnfg.adc_scan_size + 1)
		self.reading_time = [0.0]*(self.__cnfg.adc_scan_size + 1)
		self.reading_gain = [self.__cnfg.adc_default_gain]*(self.__cnfg.adc_scan_size + 1)
		self.scan_interval =  [0.0001]*(self.__cnfg.adc_scan_size + 1)
		self.__data_size = self.__cnfg.adc_scan_size

	def do_scan(self,config,do_resets=True,change_limit=4,last_gain = 1):
		self.__cnfg = config
		if self.__cnfg.adc_scan_size != self.__data_size:
			self.setup_data()
		self.gain_change_count = 0
		self.scan_count = 0
		time_from_gain_change = 0.0
		reading_ac_max = 0
		start_time = datetime.now()
		last_reading_time = 0
		reset_time = 0
		self.reset_count = 1
		rms_current_total = 0.001
		rms_totaller_count = 0
		self.gain = last_gain # initial gain at start of scan
		#phase_not_started = True
		while (self.scan_count < self.__cnfg.adc_scan_size) and ((last_reading_time - reset_time) < (self.__cnfg.adc_target_scan_msec/1000)):
			self.scan_count += 1
			self.reading_gain[self.scan_count] = self.gain
			# Read the difference between two ADC channels and return the ADC value
			# as a signed integer result.  Differential must be one of:
			#	- 0 = Channel 0 minus channel 1
			#	- 1 = Channel 0 minus channel 3
			#	- 2 = Channel 1 minus channel 3
			#	- 3 = Channel 2 minus channel 3	

			self.reading[self.scan_count] = self.__adc.read_adc_difference(self.__cnfg.adc_channel,gain = self.gain)

			self.reading_time[self.scan_count] = ((datetime.now() - start_time).total_seconds())
			self.scan_interval[self.scan_count] = self.reading_time[self.scan_count] - self.reading_time[self.scan_count-1]
			last_reading_time = self.reading_time[self.scan_count]
			time_from_gain_change = time_from_gain_change + self.scan_interval[self.scan_count]

			#last_time = this_time
			#self.reading_time[self.scan_count] = self.reading_time[self.scan_count-1] + self.scan_interval[self.scan_count-1]

			if abs(self.reading[self.scan_count]) > reading_ac_max:
				reading_ac_max = abs(self.reading[self.scan_count])


			self.adc_milli_volts[self.scan_count] = (self.reading[self.scan_count] * 2/self.reading_gain[self.scan_count]) - self.__cnfg.adc_input_offset_mv
			self.input_milli_volts[self.scan_count] = self.adc_milli_volts[self.scan_count] / self.__cnfg.adc_input_amp_gain
			self.current[self.scan_count] = self.input_milli_volts[self.scan_count]/self.__cnfg.adc_CT_resister/self.__cnfg.adc_CT_ratio
			rms_current_total = rms_current_total + (self.current[self.scan_count] * self.current[self.scan_count])
			self.rms_current[self.scan_count] = sqrt(rms_current_total/(self.scan_count+1))

#			this_time = datetime.now()

			if self.__cnfg.debug_flag_2 : print("Scan:%3d,Time:%6.2f, FromReset:%6.2f,Gain:%2d,adcRdg:%5d,adcIn_mv:%5.2f, \
mvIn:%5.2f,Ipk%5.2f,rms:%5.2f" %
(self.scan_count,1000*self.reading_time[self.scan_count],1000*(self.reading_time[self.scan_count]-reset_time,
self.gain,self.reading[self.scan_count],self.adc_milli_volts[self.scan_count],self.input_milli_volts[self.scan_count],
self.current[self.scan_count],self.rms_current[self.scan_count])))
			#if (self.scan_count > 2) and phase_not_started and ((self.reading[self.scan_count]*self.reading[self.scan_count-1]) < 0 \
			#		and self.reading[self.scan_count] > 0) and rms_current_total > 0.1:
			#	# At start of phase
			#	print("Phase zero restart")
			#	phase_not_started = False
			#	#self.scan_count = -1
			#	rms_current_total = 0
			#	reading_ac_max = 0
			if (abs(self.reading[self.scan_count]) > self.__cnfg.adc_top_limit) and (self.gain > 1) and (self.gain_change_count < change_limit):
				# Gain is too high
				self.gain = int(self.gain/2)
				self.gain_change_count += 1
				#rms_current_total = 0
				reading_ac_max = 0
				time_from_gain_change = 0
				phase_not_started = True
				#self.scan_count = -1
				reset_time = self.reading_time[self.scan_count]
				self.reset_count = self.scan_count
			elif time_from_gain_change > (25/1000) and (reading_ac_max < self.__cnfg.adc_bottom_limit ) \
					and (self.gain_change_count < change_limit) and (self.gain < 16):
				# Gain is too low
				self.gain = int(self.gain*2)
				self.gain_change_count += 1
				rms_current_total = 0
				reading_ac_max = 0
				time_from_gain_change = 0
				phase_not_started = True 
				#self.scan_count = -1
				reset_time = self.reading_time[self.scan_count]
				self.reset_count = self.scan_count
		scan_time_error = self.reading_time[self.scan_count] - self.__cnfg.adc_target_scan_msec
		average_step = self.reading_time[self.scan_count]/(self.scan_count )
		step_error =  scan_time_error/average_step
		excess_steps = self.__cnfg.adc_scan_size - self.scan_count
		self.data_size = self.scan_count
		if self.__cnfg.debug_flag_1:
			scan_time_error = self.reading_time[self.scan_count] - self.__cnfg.adc_target_scan_msec
			print ("scan_time_error: ",scan_time_error)
			average_step = self.reading_time[self.scan_count]/(self.scan_count)
			print ("average_step: ",average_step)
			step_error =  scan_time_error/average_step
			print ("step_error: ",step_error)
			excess_steps = self.__cnfg.adc_scan_size - self.scan_count - 1
			print ("excess_steps: ",excess_steps)
		return self.reading_gain[self.scan_count-1] # returns recomended change in scan sizelast error used

	def do_log(self,debug_flag,start,data_size):
		copy_flag = False
		for rc in range(start,data_size,1):
#			print(self.reading_time[rc],self.current[rc])
#                0        1        2       3          4                5       6    7    8             9            10      11
#headings = ["Time","Time Step","gain","Reading","adc Milli Volts","Input mv","I","Irms"    
			self.__adc_buffer.line_values[0] = str(self.reading_time[rc])
			self.__adc_buffer.line_values[1] = str(self.scan_interval[rc])
			self.__adc_buffer.line_values[2] = str(self.reading_gain[rc])
			self.__adc_buffer.line_values[3] = str(self.reading[rc])
			self.__adc_buffer.line_values[4] = str(self.adc_milli_volts[rc])  
			self.__adc_buffer.line_values[5] = str(round(self.input_milli_volts[rc],3))  
			self.__adc_buffer.line_values[6] = str(round(self.current[rc],3))
			self.__adc_buffer.line_values[7] = str(round(self.rms_current[rc],3))
			#	self.__adc_buffer.line_values[7] = str(current_rms[rc])
			#	self.__adc_buffer.line_values[8] = str(current[rc])
			#	self.__adc_buffer.line_values[9] = str(zero_crossing[rc])
			#	self.__adc_buffer.line_values[10] = "Spare1 "
			#	self.__adc_buffer.line_values[11] = "Spare2 "
			append = True
			if rc == data_size:
				copy_flag = True
				print("Copy this time")
			self.__adc_buffer.just_log(append,debug_flag,copy_flag,0,self.reading_time[rc],1234)
