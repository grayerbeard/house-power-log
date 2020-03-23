import Adafruit_ADS1x15
import time

class class_get_ads(object):
	# Rotating Buffer Class
	# Initiate with just the size required Parameter
	# Get data with just a position in buffer Parameter
	def __init__(self,scan_size,diff_channel,config,default_gain,top_limit,bottom_limit):
		#initialization
		self.__config = config
		self.gain = default_gain
		self.__adc=Adafruit_ADS1x15.ADS1015()
		self.last_scan_size =  max_scan_size
		self.__diff_channel = diff_channel
		self.reading = [0.0]*(max_scan_size + 1)
		self.scan_interval =  [datetime.now()]*(scan_size + 1)
		self.gain_change_count = 0
		self__top_limit = top_limit
		self__bottom_limit = bottom_limit              

	def do_scan(self):
		self.gain_change_count = 0
		scan_count = 0
		reading_ac_max = 0
		last_time = datetime.now()
		while scan_count < scan_size:
			self.reading[scan_count] = self.__adc.read_adc_difference(self.__diff_channel,gain = self.gain)
			this_time = datetime.now()
			scan_interval = 1000*(this_time - last_time ).total_seconds()
			last_time = this_time
			if abs(reading[scan_count]) > self__top_limit:
				if (self.gain > 1) and gain_change_count < 4:
					self.gain = int(self.gain/2)
					reading_ac_max = 0
					scan_count = 0
			else:
				if abs(reading[scan_count] > reading_ac_max:
					reading_ac_max = abs(reading[scan_count]
			if scan_count > int(scan_size/4):
				if (reading_ac_max < self__bottom_limit) and gain_change_count < 4:
					if self.gain < 16:
						self.gain = int(self.gain*2)
						scan_count = 0
			else:
				scan_count += 1
		return self.gain_change_count
