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

	def do_scan(self,config,resetting_limit,last_gain):
		self.__cnfg = config

		# If change in scan size set in config.cfg that requires data arrays to be set up again
		if self.__cnfg.adc_scan_size != self.__data_size:
			self.setup_data()

		# Zero the count used for storing data
		self.scan_count = 0


		# Do a reset to zero counts etc.
		self.reset_count = -1
		self.reset(True)

		# Set Time reference point
		start_time = datetime.now()
		self.reading_time[0] = 0

		# Make sure first time set to Zero
		self.reading_time[0] = 0

		# Set the Gain to the Last Gain used
		self.gain = last_gain # initial gain at start of scan

		while (self.scan_count < self.__cnfg.adc_scan_size) and ((self.reading_time[self.scan_count-1] - self.last_reset_time) < (self.__cnfg.adc_target_scan_msec/1000)):
			#print(self.scan_count,self.last_reset_time,self.reading_time[self.scan_count-1])
			# Information on differencial input channels
			# 	Read the difference between two ADC channels and return the ADC value
			# 	as a signed integer result.  Differential must be one of:
			#		- 0 = Channel 0 minus channel 1
			#		- 1 = Channel 0 minus channel 3
			#		- 2 = Channel 1 minus channel 3
			#		- 3 = Channel 2 minus channel 3	

			# Increment the Count used for storing data
			# so at start first place used is at [1]
			self.scan_count += 1 

			# Take reading and record the Gain Used
			self.reading[self.scan_count] = self.__adc.read_adc_difference(self.__cnfg.adc_channel,gain = self.gain)
			self.reading_gain[self.scan_count] = self.gain

			# Record the time the reading was taken
			self.reading_time[self.scan_count] = ((datetime.now() - start_time).total_seconds())

			# Check if reading is max seen so far so later can reduce gain if gain too high.
			if abs(self.reading[self.scan_count]) > self.reading_ac_max:
				self.reading_ac_max = abs(self.reading[self.scan_count])

			# Calculat the Current flow based on input voltage, offsets, CT Ratio and CT Load Resister
			self.adc_milli_volts[self.scan_count] = (self.reading[self.scan_count] * 2/self.reading_gain[self.scan_count]) - self.__cnfg.adc_input_offset_mv
			self.input_milli_volts[self.scan_count] = self.adc_milli_volts[self.scan_count] / self.__cnfg.adc_input_amp_gain
			self.current[self.scan_count] = self.input_milli_volts[self.scan_count]/self.__cnfg.adc_CT_resister/self.__cnfg.adc_CT_ratio

			# Add to the RMS current totaliser and estimate RMS current
			self.rms_current_total = self.rms_current_total + (self.current[self.scan_count] * self.current[self.scan_count])
			self.rms_current[self.scan_count] = sqrt(self.rms_current_total/(self.scan_count+1))

			# If in Debug Mode Print out the input and calculated values
			if self.__cnfg.debug_flag_2 : print("Scan:%3d,Time:%6.2f, FromReset:%6.2f,Gain:%2d,adcRdg:%5d,adcIn_mv:%5.2f, \
mvIn:%5.2f,Ipk%5.2f,rms:%5.2f" %
(self.scan_count,1000*self.reading_time[self.scan_count],1000*(self.reading_time[self.scan_count]-self.last_reset_time),
self.gain,self.reading[self.scan_count],self.adc_milli_volts[self.scan_count],self.input_milli_volts[self.scan_count],
self.current[self.scan_count],self.rms_current[self.scan_count]))

			# Detect if just after a zero crossing going positive and do a reset
			print("do checking")
			if (self.scan_count > 2) and self.phase_not_started and ((self.reading[self.scan_count]*self.reading[self.scan_count-1]) < 0 \
					and self.reading[self.scan_count] > 0) : # and self.rms_current_total > 0.1:
				# At start of phase
				self.reset(False)
				print("phase reset")

			# Check if gain too high and if so reduce the gain and do reset (if gain not already lowest)
			if (abs(self.reading[self.scan_count]) > self.__cnfg.adc_top_limit) and (self.gain > 1) and (self.reset_count < resetting_limit):
				# Gain is too high
				self.gain = int(self.gain/2)
				self.reset(True)
				print("Gain High Reset")

			# Check if gain too low and if so increase the gain and do reset (if gain not already highest)
			elif (self.reading_time[self.scan_count] - self.last_reset_time) > (30/1000) and (self.reading_ac_max < self.__cnfg.adc_bottom_limit ) \
					and (self.reset_count < resetting_limit) and (self.gain < 16):
				# Gain is too low
				self.gain = int(self.gain*2)
				self.reset(True)
				print("Gain Low Reset")

		# Now finished so record the position of last data value
		# The data to use is recorder between self.start_count  and self.data_size
		self.end_count = self.scan_count

		# If in debug mode print out some fascinating information
		if self.__cnfg.debug_flag_1:
			scan_time_error = self.reading_time[self.scan_count] - self.__cnfg.adc_target_scan_msec
			average_step = self.reading_time[self.scan_count]/(self.scan_count )
			step_error =  scan_time_error/average_step
			excess_steps = self.__cnfg.adc_scan_size - self.scan_count
			scan_time_error = self.reading_time[self.scan_count] - self.__cnfg.adc_target_scan_msec
			print ("scan_time_error: ",scan_time_error)
			average_step = self.reading_time[self.scan_count]/(self.scan_count)
			print ("average_step: ",average_step)
			step_error =  scan_time_error/average_step
			print ("step_error: ",step_error)
			excess_steps = self.__cnfg.adc_scan_size - self.scan_count - 1
			print ("excess_steps: ",excess_steps)
		
		# Return with the value of gain being used so that can be used at start next time
		return self.gain # returns recomended change in scan sizelast error used

	def reset(self,was_gain_change):
		# used by self.do_scan for resets
		print("doing reset",was_gain_change)
		# value to register where to start using data after scan done
		self.start_count = self.scan_count

		# value to allow checking of time since last reset in secounds
		self.last_reset_time = self.reading_time[self.scan_count]

		# Totaller for calculating rms current
		self.rms_current_total = 0

		# value to note nmax input used for reducing gain id gain too high
		self.reading_ac_max = 0

		# count so we can make sure dont keep doing too many resets
		self.reset_count += 1

		# if reset because of a phase change reset then need to record that so we dont reset at the next zero crossing
		if was_gain_change:

			# Flag to enable starting after zero crossing
			self.phase_not_started = True 

		else:
			self.phase_not_started = False



	def do_log(self,debug_flag,start_count,end_count):
		copy_flag = False
		for rc in range(start_count,end_count,1):
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
			if rc == end_count:
				copy_flag = True
				print("Copy this time")
			self.__adc_buffer.just_log(append,debug_flag,copy_flag,0,self.reading_time[rc],1234)
