import numpy as np
from scipy.optimize import leastsq
import pylab as plt
from sin_fit import do_fit
from datetime import datetime

start_time = datetime.now()

N = 100 # number of data points
t = np.linspace(0, 20*np.pi, N)
#f = 1.15247 # Optional!! Advised not to use
#data = 3.0*np.sin(f*t+0.001) + 0.5 + np.random.randn(N) # create artificial data with noise
data = 3.0*np.sin(t+0.001) + 0.1 + np.random.randn(N) # 
#for ind in range(0,len(t),1):
#	print(ind,t[ind],data[ind])

set_up_time =  datetime.now()

debug_flag = True

do_fit(N,t,data,debug_flag)

set_up_time =  datetime.now()

print("done")
