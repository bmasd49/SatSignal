import numpy as np
import tools.signalTools as tools
import tools.IOtools as IO

class signal:
    def __init__(self, signalName, signalPath, signalOffset = None, expectedFreq = None, bandWidth = None, timeInterval = None, timeStep = None, resolution = None):
        self.name = signalName
        self.path = signalPath
        self.fs, self.rawSignal = IO.readFile(signalPath)
        self.safety = 0.5

        if expectedFreq == None:
            self.expectedFreq = 0
        else:
            self.expectedFreq = expectedFreq

        if resolution  == None:
            self.resolution = 600
        else:
            self.resolution = resolution

        if bandWidth == None:
            self.bandWidth = 30e3
        else:
            self.bandWidth = bandWidth

        self.sensitivity = int(self.bandWidth/self.resolution)

        if signalOffset == None:
            self.signalOffset = 0
        else:
            self.signalOffset = signalOffset

        if timeInterval != None:
            self.rawSignal = self.rawSignal[int(timeInterval[0]*self.fs):int(timeInterval[1]*self.fs)]
        if timeStep == None:
            self.timeStep = 1.
        else:
            self.timeStep = timeStep
        
        self.totalLength = int(self.rawSignal.shape[0]/(self.fs*self.timeStep))

        # if self.name == 'NOAA15':
            # self.defaultFreq = 137.620e6
        # elif self.name == 'NOAA18':
            # self.defaultFreq = 137.9125e6
        # elif self.name == 'NOAA19':
            # self.defaultFreq = 137.100e6
        # else:
            # print('Please type in default frequency of the satellite: ')
            # self.defaultFreq == float(input())

        fullFreq = np.fft.fftfreq(int(self.fs * self.timeStep), 1/(self.fs))
        # self.bandwidthIndex = np.where(np.logical_and(fullFreq > - self.bandWidth/2, fullFreq < self.bandWidth/2))
        # self.bandwidthIndex = np.where(np.logical_and(fullFreq > self.expectedFreq - self.signalOffset - self.bandWidth/2, fullFreq < self.expectedFreq - self.signalOffset + self.bandWidth/2))
        self.bandwidthIndex = np.where(np.logical_and(fullFreq > self.expectedFreq - self.signalOffset - self.bandWidth/2, fullFreq < self.expectedFreq - self.signalOffset + self.bandWidth/2))
        self.fullFreq = fullFreq[self.bandwidthIndex] #+ self.signalOffset
        self.simplifiedFreq = tools.avg_binning(self.fullFreq, self.sensitivity)

    def FFT(self, step=None):
        localSignal = self.rawSignal[int(self.fs * self.timeStep * step): int(self.fs * self.timeStep * (step+1))]/127.
        localSignal *= np.hanning(int(self.fs * self.timeStep))
        magnitude = 20*np.log10(np.abs(np.fft.fft(localSignal)[self.bandwidthIndex]))
        return magnitude
    
    def findSignal(self, magnitude):
        std = np.std(magnitude)
        safety = -std
        mag = tools.avg_binning(magnitude, self.sensitivity)
        mag_avg = np.mean(mag)
        mag -= mag_avg + std + safety
        mag = np.clip(mag, a_min=0., a_max=None)
        return mag, tools.centroid(self.simplifiedFreq, mag)

    def spectrogram(self, step=None, simplify=False):
            mag = self.FFT(step=step)
            mag1, centroid = self.findSignal(mag)
        if simplify:
            return mag1, centroid
        else:
            return mag, centroid
        




