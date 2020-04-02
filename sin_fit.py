import numpy as np
from scipy.optimize import leastsq
import pylab as plt

class class_get_adc(object):
	def do_fit(N,t,data,debug_flag):
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
		self.est_amp, self.est_freq, self.est_phase, self.est_mean = leastsq(optimize_func, [guess_amp, guess_freq, guess_phase, guess_mean])[0]

		print("amp: ",self.est_amp,"  est_freq: ",self.est_freq,"  est_phase: ",self.est_phase,"  est_mean: ",self.est_mean)

						Time:%6.2f

		print("Amp:%5.2f,Freq:%6.2f,Phase:%6.2f,Mean:%6.2" % (self.est_amp,self.est_freq,self.est_phase,self.est_mean))

		if debug_flag:
			# recreate the fitted curve using the optimized parameters
			data_fit = self.est_amp*np.sin(self.est_freq*t+self.est_phase) + self.est_mean
			# recreate the fitted curve using the optimized parameters
			fine_t = np.arange(0,max(t),0.1)
			data_fit=self.est_amp*np.sin(self.est_freq*fine_t+self.est_phase)+self.est_mean
			plt.plot(t, data, '.')
			plt.plot(t, data_first_guess, label='first guess')
			plt.plot(fine_t, data_fit, label='after fitting')
			plt.legend()
			plt.show()
