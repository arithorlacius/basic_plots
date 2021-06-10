import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob as gb
from sys import exit
from scipy import signal

fig, ax = plt.subplots(2, 1, figsize = [12,8],sharex = True)
fil = "TP1_startup_2.CSV"
name = "Test point 1, startup"
df = pd.read_csv(fil)
# Generate the sampling frequency from the data points
delta_t = df.iloc[0,-1] - df.iloc[0,0]
fs = df.size/delta_t
# Generate the Butterworth lowpass data
sos = signal.butter(3, fs/100, 'lowpass', fs = fs, output='sos')
filt_sig = signal.sosfilt(sos, df.iloc[:,1])
# Plotting
ax[0].plot(df.iloc[:,0], df.iloc[:,1], label = name)
ax[1].plot(df.iloc[:,0], filt_sig, linestyle = 'dashed', label = 'Butterworth lowpass')
ax[1].set_xlabel('Time [s]')
ax[0].legend()
ax[0].grid(True)
ax[1].grid(True)
#plt.show()
plt.savefig('Tstartup.png',dpi=300,bbox_inches='tight')
