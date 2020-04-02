import numpy as np
from scipy.optimize import leastsq
import pylab as plt

class class_sin-fit(object):
	def __init__(self,config):
		#initialization
#		self.__cnfg = config
#		self.setup_data()
            
#	def setup_data(self):
#		self.reading = [0.0]*(self.__cnfg.adc_scan_size + 1)
#		self.adc_milli_volts = [0.0]*(self.__cnfg.adc_scan_size + 1)
#		self.input_milli_volts = [0.0]*(self.__cnfg.adc_scan_size + 1)
#		self.peak_current = [0.0]*(self.__cnfg.adc_scan_size + 1)
#		self.rms_current = [0.0]*(self.__cnfg.adc_scan_size + 1)
#		self.reading_time = [0.0]*(self.__cnfg.adc_scan_size + 1)
#		self.reading_gain = [self.__cnfg.adc_default_gain]*(self.__cnfg.adc_scan_size + 1)
#		self.scan_interval =  [0.1]*(self.__cnfg.adc_scan_size + 1)
#		self.__data_size = self.__cnfg.adc_scan_size

	def do_fit(self,N,t,f,data):
#		self.__cnfg = config
#		if self.__cnfg.adimport numpy as npc_scan_size != self.__data_size:
#			self.setup_data()


#N = 1000 # number of data points
#t = np.linspace(0, 4*np.pi, N)
#f = 1.15247 # Optional!! Advised not to use
#data = 3.0*np.sin(f*t+0.001) + 0.5 + np.random.randn(N) # create artificial data with noise



		guess_mean = np.mean(data)
		guess_std = 3*np.std(data)/(2**0.5)/(2**0.5)
		guess_phase = 0
		guess_freq = 1
		guess_amp = 1

		# we'll use this to plot our first estimate. This might already be good enough for you
		data_first_guess = guess_std*np.sin(t+guess_phase) + guess_mean

		# Define the function to optimize, in this case, we want to minimize the difference
		# between the actual data and our "guessed" parameters
		optimize_func = lambda x: x[0]*np.sin(x[1]*t+x[2]) + x[3] - data
		est_amp, est_freq, est_phase, est_mean = leastsq(optimize_func, [guess_amp, guess_freq, guess_phase, guess_mean])[0]

		# recreate the fitted curve using the optimized parameters
		data_fit = est_amp*np.sin(est_freq*t+est_phase) + est_mean

		# recreate the fitted curve using the optimized parameters

		fine_t = np.arange(0,max(t),0.1)
		data_fit=est_amp*np.sin(est_freq*fine_t+est_phase)+est_mean

		plt.plot(t, data, '.')
		plt.plot(t, data_first_guess, label='first guess')
		plt.plot(fine_t, data_fit, label='after fitting')
		plt.legend()
		plt.show()
