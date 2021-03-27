import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import scipy.signal

def readFile(filename):
    """read wavefile and return sampling rate, as well as recorededSignal as a complex value made of both channels of the wavefile."""
    samplingRate, channels = wavfile.read(filename+'.wav')
    recorededSignal = channels[:,0] + 1j * channels[:,1]
    return recorededSignal, samplingRate

def frequencySpectrum(inputSignal, samplingRate, timeBegin, timeStep):
    """Find the amplitudes in frequency domain of the inputSignal by using FFT, then apply Savitzky-Golay filter to reduce noise of the output"""
    signal = inputSignal[int(timeBegin*samplingRate):int((timeBegin+timeStep)*samplingRate)]
    frequencies = np.fft.fftfreq(signal.shape[0], 1/samplingRate)
    FFT = np.fft.fft(signal)
    filteredAmplitude = scipy.signal.savgol_filter(np.abs(FFT), window_length=int(samplingRate/1000)+1, polyorder=2)
    return frequencies, filteredAmplitude

def spectralCentroid(frequencies, amplitudes, samplingRate, freqBegin, freqEnd):
    """Finding the center, or spectral centroid, of the signal.
    """   
    indexBegin = int(freqBegin * frequencies.shape[0] / samplingRate)
    indexEnd = int(freqEnd * frequencies.shape[0] / samplingRate)
    centroid = np.sum(frequencies[indexBegin:indexEnd] * amplitudes[indexBegin:indexEnd]) / np.sum(amplitudes[indexBegin:indexEnd])
    return centroid

def visualizing(outputFilename, inputSignal, samplingRate, timeBegin, timeStep, centroid):
    """Visualizing inputSignal in frequency domain."""
    frequencies, amplitudes = frequencySpectrum(inputSignal, samplingRate, timeBegin, timeStep)
    plt.figure(figsize=(12,4), dpi=300)
    plt.semilogy(frequencies, amplitudes, '.', markersize=0.01)
    plt.axvline(x=centroid, color='red', markersize=0.05, label=f'Centroid={centroid/1e6:.4f}MHz')
    plt.xlabel('Frequencies (MHz)')
    plt.ylabel('Signal amplitude')
    tickMax = np.max(frequencies)
    plt.xticks(np.arange(-tickMax, tickMax, 0.1e6))
    plt.grid()
    plt.legend()
    plt.savefig(f'./plots/Python_{outputFilename}_{timeBegin}to{timeBegin+timeStep}s.png')
    plt.clf()

if __name__=='__main__':
    NOAA1 = '22-16-38_162600000Hz_2400000s'
    NOAA2 = '14-18-17_162600000Hz_2560000s'
    NOAA = [NOAA1]#, NOAA2]

    #Time interval that we will be working on, from 0 to 5 seconds with step of 1 second.
    timeStep = 1.
    timeEnd = 5.

    #We will find the centroid of signals between 0.4 and 0.5 MHz
    freqBegin = 0.4e6
    freqEnd = 0.5e6

    for inputFile in NOAA:
        NOAASignal, samplingRate = readFile(inputFile)
        for timeBegin in np.arange(0, timeEnd, step=timeStep):
            frequencies, amplitudes = frequencySpectrum(NOAASignal, samplingRate, timeBegin, timeStep)
            centroid = spectralCentroid(frequencies, amplitudes, samplingRate, freqBegin, freqEnd)
            visualizing(inputFile, NOAASignal, samplingRate, timeBegin, timeStep, centroid)   #Take time interval from 0 to 3 seconds
    pass
    

