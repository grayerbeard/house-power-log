import numpy as np
from scipy.optimize import leastsq
import pylab as plt
from sin_fit import class_sin_fit
from datetime import datetime

estimate_sin = class_sin_fit()

start_time = datetime.now()

total_time_sec = 0.040
data_size = 40
data_amp = 10
sin_freq = 50
phase_error = 0.0005
zero_error = 0
random_error = 0.05

#gave 47 cycles I want 300/20 is 15
#

N = data_size # number of data points
#t = np.linspace(0, 20*np.pi, N)
t = np.linspace(0, total_time_sec, N)
data = data_amp*np.sin(2*np.pi*sin_freq*(t+phase_error)) + zero_error + random_error*data_amp*np.random.randn(N) # 
#data = data_amp*np.sin(2*np.pi*sin_freq*t)
cycle_count = 0
for ind in range(0,data_size):
	if (ind > 1) and (data[ind-1]*data[ind]<0) and (data[ind]>0):
		cycle_count += 1
#	print(ind,round(t[ind],4),round(data[ind],2),cycle_count)

#print(20*np.pi)

set_up_time =  datetime.now()

guess_mean =  0
guess_std = 0
guess_phase = - phase_error
guess_freq = 50
guess_amp = 1.05*data_amp
debug_flag = True

estimate_sin.do_fit(t,data,guess_mean,guess_std,guess_phase,guess_freq,guess_amp,debug_flag)

fit_time =  datetime.now()

set_up = 1000*(set_up_time - start_time).total_seconds()
fit = 1000*(fit_time - start_time).total_seconds() - set_up

print("Set up in: " + str(set_up) + "msec")
print("Amp:%6.2f,  Freq:%6.2f,  Phase:%6.2f,  Mean:%6.2f   Fit Done In (msec):%6.2f" % 
(estimate_sin.est_amp, estimate_sin.est_freq, estimate_sin.est_phase,estimate_sin.est_mean,estimate_sin.fit_time))
       
