from scipy.signal import stft, savgol_filter
from scipy.fftpack import fft
from scipy.ndimage import uniform_filter1d
import numpy as np

def local(signal, timeInterval=None, freqInterval=None):
    if timeInterval==None:
        timeInterval = (0, signal.shape[0])
    if freqInterval==None:
        freqInterval = (signal.defaultFreq - signal.shifingRange, signal.defaultFreq + signal.shifingRange)

    
    pass
def windowing():
    pass













def centroid(freq, mag):
    """Finding the center, or spectral centroid, of the signal.
    """   
    return  np.sum(freq * mag) / np.sum(mag)

def STFT(signal, fs, timeStep):
    """Short timed fourier transform
    """
    return stft(signal, fs=fs, nperseg=timeStep * fs, return_onesided=False)

def FFT(signal):
    """FFT
    """
    return fft(signal)


def Hz_to_kHz(x):
    return x/1000

def amp_to_dB(x):
    return 20*np.log10(x)

def filtering(fs, signal): 
    return savgol_filter(signal, window_length=1001, polyorder=2)

def avg_binning(inputArray, sensitivity):
    numberOfBins = int(len(inputArray)/sensitivity)
    return [np.mean(value) for value in np.array_split(inputArray, numberOfBins)]

def moving_avg_filter(f, mag, sensitivity):
    fBins = binning(f, sensitivity)
    magBins = binning(mag, sensitivity)
    avg_f = np.average(fBins, axis=1)
    avg_mag = np.average(magBins, axis=1)
    return avg_f, avg_mag


def detectSignal():

    pass

