#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from sys import exit
import datetime

dat = pd.read_csv("tdata_03.06.2021.csv")
logstart = pd.to_datetime('03/06/2021 14:22:00')
logend = pd.to_datetime('03/06/2021 15:22:00')

all_dates = pd.to_datetime(dat.date + " " + dat.time)
fig, ax = plt.subplots(figsize = [12,9])
ax.plot_date(all_dates, dat.T1, '-', label="U201")
ax.plot_date(all_dates, dat.T2, '-', label="U301")
ax.plot_date(all_dates, dat.T3, '-', label="Temperature sensor")
ax.plot_date(all_dates, dat.T4, '-', label="Wifi module")
ax.plot_date(all_dates, dat.T5, '-', label="Bluetooth module")
ax.plot_date(all_dates, dat.T6, '-', label="Ambient temperature")
plt.axvline(logstart,linestyle='-.')
plt.text(logstart,26.5,'Valid bulk test start',rotation=90, fontsize=16)
plt.axvline(logend,linestyle='-.')
plt.text(logend,26.5,'Valid bulk test end',rotation=90, fontsize=16)
ax.legend(loc=4)
ax.grid(True)
ax.xaxis.set_major_formatter( DateFormatter('%H:%M:%S') )
ax.set_ylabel("Temperature [°C]")
ax.set_xlabel("Time")
#plt.show()
plt.savefig('sensor_data.png', bbox_inches='tight', dpi=300)
