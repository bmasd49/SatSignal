import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import scipy.signal

def readFile(filename):
    """read wavefile and return sampling rate, as well as recorededSignal as a complex value made of both channels of the wavefile."""
    samplingRate, channels = wavfile.read(filename+'.wav')
    recorededSignal = channels[:,0] + 1j * channels[:,1]
    return recorededSignal, samplingRate

def spectralCentroid(frequencies, amplitudes, samplingRate, freqBegin, freqEnd):
    """Finding the center, or spectral centroid, of the signal.
    """   
    indexBegin = int(freqBegin * frequencies.shape[0] / samplingRate)
    indexEnd = int(freqEnd * frequencies.shape[0] / samplingRate)
    centroid = np.sum(frequencies[indexBegin:indexEnd] * amplitudes[indexBegin:indexEnd]) / np.sum(amplitudes[indexBegin:indexEnd])
    return centroid

def STFT(signal, fs, timeStep):
    return scipy.signal.stft(signal, fs=fs, nperseg=timeStep * fs, return_onesided=False)

def Hz_to_kHz(x):
    return x/1000

def amp_to_dB(x):
    return 20*np.log10(x)

def dB_to_amp(x):
    return librosa.core.db_to_amplitude(x)

def removingNoise(fs, signal): 
    return scipy.signal.savgol_filter(signal, window_length=int(fs/1000)+1, polyorder=2)

if __name__=='__main__':
    NOAA = 'station1_yagi_SDRSharp_20170312_060959Z_137650kHz_IQ'
    inputFiles = [NOAA]

    timeStep = 1.
    timeMax = 20.

    f_min = -30e3 #Hz
    f_max = 70e3  #Hz
    
    for inputFile in inputFiles:
        signal, fs = readFile(inputFile)
        signal = signal[:int(timeMax*fs)]
        f, t, spectrum = STFT(signal, fs, timeStep)
        if (f_min<0) and (f_max>=0):
            f = np.concatenate((f[:int(f_max)],f[int(f_min):]))
            spectrum = np.concatenate((spectrum[:int(f_max),:],spectrum[int(f_min):,:]))
        else:
            f = f[int(f_min):int(f_max)]
            spectrum = spectrum[int(f_min):int(f_max),:]

        f = Hz_to_kHz(f)
        spectrum = amp_to_dB(np.abs(spectrum))
        avg = np.mean(spectrum, axis=1)
        # avg = removingNoise(fs, avg)
        plt.plot(f,avg,'.', markersize=0.1)
        plt.ylim([-120,0])
        plt.yticks(np.arange(0,-130,-10))
        plt.xticks(np.arange(Hz_to_kHz(f_min), Hz_to_kHz(f_max)*1.1, 10))
        plt.grid()
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.title(f'{timeMax}-second-average of signal')
        plt.savefig('avg.png')
        plt.clf()
        plt.figure(figsize=(8,6), dpi=300)
        for i, time in enumerate(t[1:-1]):
            plt.plot(f, spectrum[:,i+1], '.', markersize=0.1)
            plt.ylim([-120,0])
            plt.yticks(np.arange(0,-130,-10))
            plt.xticks(np.arange(Hz_to_kHz(f_min), Hz_to_kHz(f_max)*1.1, Hz_to_kHz(f_max-f_min)/10))
            plt.grid()
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude (dB)')
            plt.title(f'STFT Magnitude at {time} s')
            plt.savefig(f'./gif/{i:03d}.png')
            plt.clf()











