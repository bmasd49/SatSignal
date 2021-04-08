import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import scipy.signal
import os
import tools.signalProcessing as signal
import tools.IOtools as io
import tools.signalTools as tools

if __name__=='__main__':
    APT = signal.signal('NOAA15', './inputSignals/station1_yagi_SDRSharp_20170312_060959Z_137650kHz_IQ.wav', signalOffset=137.65e6, timeStep=1.)
    io.plotting(APT, steps=range(60))


