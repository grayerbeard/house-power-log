import numpy as np
from scipy.optimize import leastsq
import pylab as plt
from datetime import datetime

class class_sin_fit(object):
	def do_fit(self,t,data,guess_mean,guess_std,guess_phase,guess_freq,guess_amp,debug_flag):
		self.start_time = datetime.now()
		data_first_guess = guess_amp*np.sin(2*np.pi*guess_freq*(t+guess_phase)) + guess_mean

		optimize_func = lambda x: x[0]*np.sin(2*np.pi*x[1]*(t+x[2])) + x[3] - data
		self.est_amp, self.est_freq, self.est_phase, self.est_mean = leastsq(optimize_func, [guess_amp, guess_freq, guess_phase, guess_mean])[0]
		self.fit_done_time =  datetime.now()
		self.fit_time = 1000*(self.fit_done_time - self.start_time).total_seconds()
		if debug_flag:
			data_fit = self.est_amp*np.sin(2*np.pi*self.est_freq*(t+self.est_phase)) + self.est_mean
			fine_t = np.linspace(0,max(t),10*len(t))
			data_fit=self.est_amp*np.sin(2*np.pi*self.est_freq*(fine_t+self.est_phase))+self.est_mean
			print("Amp:%6.2f,  Freq:%6.2f,  Phase:%6.2f,  Mean:%6.2f,  Fit Done In (msec):%6.2f" % 
				(self.est_amp, self.est_freq, self.est_phase,self.est_mean,self.fit_time))
			plt.plot(t, data, '.')
			plt.plot(t, data_first_guess, label='first guess')
			plt.plot(fine_t, data_fit, label='after fitting')
			plt.legend()
			plt.show()
