import Adafruit_ADS1x15
adc=Adafruit_ADS1x15.ADS1015()

class class_get_ads(object):
	# Rotating Buffer Class
	# Initiate with just the size required Parameter
	# Get data with just a position in buffer Parameter
	def __init__(self,scan_size,diff_channel,config,default_gain):
		#initialization
		self.__config = config
		self.gain = default_gain
		self.__adc=Adafruit_ADS1x15.ADS1015()
		self.last_scan_size =  max_scan_size
		self.__diff_channel = diff_channel
		reading = [0.0]*(max_scan_size + 1)
		reading_time =  [datetime.now()]*(max_scan_size + 1)
		self.gain_change_count = 0              

	def do_scan(self):
		self.gain_change_count = 0
		scan_count = 0
		reading_ac_max = 0
		while rc < scan_size:
			reading[scan_count] = self.__adc.read_adc_difference(self.__diff_channel,gain = self.gain)
			if abs(reading[scan_count]) > 2000:
				if (self.gain > 1) and gain_change_count < 4:
					self.gain = int(self.gain/2)
					reading_ac_max = 0
					rc = 0
			else:
				if abs(reading[scan_count] > reading_ac_max:
					reading_ac_max = abs(reading[rc]
			if scan_count > int(scan_size/4):
				if (reading_ac_max < 1000) and gain_change_count < 4:
					if self.gain < 16:
						self.gain = int(self.gain*2)
						scan_count = 0
			else:
				rc += 1
		return self.gain_change_count
