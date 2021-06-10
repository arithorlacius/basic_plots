import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob as gb
from sys import exit
from scipy import signal

# TP1 = Analog supply voltage
# TP2 = Bias voltage
# TP3 = Output of amplifier
# TP4 = Load cell main power voltage

# Load cell A represented by a shade of red
reds = ['darkorange','red','maroon']
# Load cell B represented by a shade of blue
blues = ['darkblue','royalblue','skyblue']

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='white', alpha=0.5)
cols = reds + blues
fig, ax = plt.subplots(4, 2, figsize = [8,12], sharey='row')
for n_ind, num in enumerate(['1','2','3','4']):
    for s_ind, status in enumerate(['startup', 'shutdown']):
        for index,fil in enumerate(gb('scope_waveforms/LCI_2?/TP'+num+'_'+status+'_?.CSV')):
            print(fil)
            loadcell = fil.split('\\')[1]
            split = fil.split('\\')[-1].split('.')[0]
            test_info = split.split("_")
            name = loadcell +" "+ split
            print(loadcell, name)
            df = pd.read_csv(fil)
            # Generate the sampling frequency from the data points
            delta_t = df.iloc[0,-1] - df.iloc[0,0]
            fs = df.size/delta_t
            # Generate the Butterworth lowpass data
            sos = signal.butter(3, fs/100, 'lowpass', fs = fs, output='sos')
            filt_sig = signal.sosfilt(sos, df.iloc[:,1])
            # Plotting
            ax[n_ind,s_ind].plot(df.iloc[:,0], df.iloc[:,1], color = cols[index], label =  loadcell+' run '+test_info[-1])
            #ax[n_ind,s_ind].plot(df.iloc[:,0], filt_sig, color = cols[index], linestyle = 'dashed', label = loadcell+' run '+test_info[-1])

        if status == 'shutdown':
            if  num == '1':
                textstr = r'$\Delta t\approx%.1f \mathrm{ms}$' % (44.224, )
                ax[n_ind,s_ind].set_xlim(-0.01,0.05)
                ax[n_ind,s_ind].set_title('Analog supply (TP1)', loc='right')
                ax[n_ind,s_ind].set_xticks(ax[n_ind,s_ind].get_xticks()[1:])
            elif num == '2':
                textstr = r'$\Delta t\approx%.2f \mathrm{s}$' % (1.7052, )
                ax[n_ind,s_ind].set_xlim(-0.2,2.2)
                ax[n_ind,s_ind].set_title('Bias (TP2)', loc='right')
            elif num == '3':
                textstr = '\n'.join((
                r'$\Delta t\approx%.2f \mathrm{s}$' % (1.5618, ),
                r'$\Delta V_{OS}\approx %.1f \mathrm{mV}$' % (179.68, )))
                ax[n_ind,s_ind].set_xlim(-0.2,1.6)
                ax[n_ind,s_ind].set_title('Amplifier output (TP3)', loc='right')
            else:
                textstr = '\n'.join((
                r'$\Delta t_{2A}\approx%.2f \mathrm{s}$' % (1.1605, ),
                r'$\Delta t_{2B}\approx%.1f \mathrm{ms}$' % (580.25, )))
                ax[n_ind,s_ind].set_xlim(-0.05,1.1)
                ax[n_ind,s_ind].set_xlabel('Time [s]')
                ax[n_ind,s_ind].set_title('Main power rail (TP4)', loc='right')
            # place a text box in upper left in axes coords
            ax[n_ind,s_ind].text(0.65, 0.95, textstr, transform=ax[n_ind,s_ind].transAxes, fontsize=8, verticalalignment='top', bbox=props)
        else:
            ax[n_ind,s_ind].set_ylabel('Voltage [V]')
            if  num == '1':
                textstr = r'$\Delta t\approx%.1f \mathrm{ms}$' % (8.448, )
                ax[n_ind,s_ind].set_xlim(-0.002,0.01)
                ax[n_ind,s_ind].ticklabel_format(axis='x',scilimits=(-3,-3),useMathText=True)
            elif num == '2':
                textstr = '\n'.join((
                r'$\Delta t\approx%.1f \mu \mathrm{s}$' % (796.8, ),
                r'$\Delta V_{OS}\approx %.1f \mathrm{mV}$' % (187.49, )))
                ax[n_ind,s_ind].set_xlim(-0.0005,0.0015)
                ax[n_ind,s_ind].ticklabel_format(axis='x',scilimits=(-3,-3),useMathText=True)
            elif num == '3':
                textstr = '\n'.join((
                r'$\Delta t\approx%.1f \mathrm{ms}$' % (4.6, ),
                r'$\Delta V_{OS}\approx %.1f \mathrm{mV}$' % (287.09, )))
                ax[n_ind,s_ind].set_xlim(-0.002,0.006)
                ax[n_ind,s_ind].ticklabel_format(axis='x',scilimits=(-3,-3),useMathText=True)
            else:
                textstr = r'$\Delta t\approx%.1f \mathrm{ms}$' % (22.167, )
                ax[n_ind,s_ind].set_xlim(-0.015,0.02)
                ax[n_ind,s_ind].ticklabel_format(axis='x',scilimits=(-3,-3),useMathText=True)
                ax[n_ind,s_ind].set_xlabel('Time [s]')
                ax[n_ind,s_ind].legend(fontsize=7)
            # place a text box in upper left in axes coords
            ax[n_ind,s_ind].text(0.65, 0.08, textstr, transform=ax[n_ind,s_ind].transAxes, fontsize=8, verticalalignment='bottom', bbox=props)
        ax[n_ind,s_ind].grid(True)
#plt.savefig('all_measurements_no_filt.pdf',bbox_inches='tight')
plt.subplots_adjust(wspace = 0.05, hspace=0.3)
#plt.savefig('all_measurements_butter_lowpass.pdf',bbox_inches='tight')
plt.savefig('all_measurements_raw.png',dpi = 300,bbox_inches='tight')
#plt.savefig('all_measurements_butter_lowpass.png',dpi = 300,bbox_inches='tight')