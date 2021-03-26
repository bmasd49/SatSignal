import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import scipy.signal

def readFile(filename):
    """read wavefile and return sampling rate, as well as recorededSignal as a complex value made of both channels of the wavefile."""
    samplingRate, channels = wavfile.read(filename)
    recorededSignal = channels[:,0] + 1j * channels[:,1]
    return recorededSignal, samplingRate

def frequencySpectrum(inputSignal, samplingRate, t_begin, t_end):
    """Find the amplitudes in frequency domain of the inputSignal by using FFT, then apply Savitzky-Golay filter to reduce noise of the output"""
    signal = inputSignal[t_begin*samplingRate:t_end*samplingRate]
    frequencies = np.fft.fftfreq(signal.shape[0], 1/samplingRate)
    FFT = np.fft.fft(signal)
    filteredAmplitude = scipy.signal.savgol_filter(np.abs(FFT), window_length=int(samplingRate/100)+1, polyorder=2)
    return frequencies, filteredAmplitude

def visualizing(outputFilename, inputSignal, samplingRate, t_begin, t_end):
    """Visualizing inputSignal in frequency domain."""
    frequencies, amplitudes = frequencySpectrum(inputSignal, samplingRate, t_begin, t_end)
    plt.semilogy(frequencies, amplitudes, '.', markersize=0.01)
    plt.xlabel('Frequencies')
    plt.ylabel('Signal amplitude')
    plt.savefig(f'Python_{outputFilename}.png')
    plt.clf()

def spectralCentroid():
    """Finding the center, or spectral centroid, of the signal.
       To be finished..."""
    pass

if __name__=='__main__':
    NOAA1 = '22-16-38_162600000Hz_2400000s.wav'
    NOAA2 = '14-18-17_162600000Hz_2560000s.wav'

    NOAASignal1, samplingRate1 = readFile(NOAA1)
    NOAASignal2, samplingRate2 = readFile(NOAA2)

    visualizing(NOAA1, NOAASignal1, samplingRate1, 0, 3)   #Take time interval from 0 to 3 seconds
    visualizing(NOAA2, NOAASignal2, samplingRate2, 0, 3)   #Take time interval from 0 to 3 seconds
    pass
    

