import numpy as np
import tools.signalTools as tools
import tools.IOtools as IO

class signal:
    def __init__(self, signalName, signalPath, center_frequency = None, expectedFreq = None, bandWidth = None, timeInterval = None, timeStep = None, resolution = None, pass_bandwidth = None):
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

        if center_frequency == None:
            self.center_frequency = 0
        else:
            self.center_frequency = center_frequency

        if timeInterval != None:
            self.rawSignal = self.rawSignal[int(timeInterval[0]*self.fs):int(timeInterval[1]*self.fs)]
        if timeStep == None:
            self.timeStep = 1.
        else:
            self.timeStep = timeStep

        if pass_bandwidth == None:
            self.pass_bandwidth = 1000
        else:
            self.pass_bandwidth = pass_bandwidth
   
        self.totalLength = int(self.rawSignal.shape[0]/(self.fs*self.timeStep))
        self.noise_offset = 0

        fullFreq = np.fft.fftfreq(int(self.fs * self.timeStep), 1/(self.fs))
        self.bandwidthIndex = np.where(np.logical_and(fullFreq > self.expectedFreq - self.center_frequency - self.bandWidth/2, fullFreq < self.expectedFreq - self.center_frequency + self.bandWidth/2))
        self.fullFreq = fullFreq[self.bandwidthIndex] #+ self.center_frequency
        self.simplifiedFreq = tools.avg_binning(self.fullFreq, self.resolution)

    def spectral(self, step=None, simplify=True):
        localSignal = self.rawSignal[int(self.fs * self.timeStep * step): int(self.fs * self.timeStep * (step+1))]/127.
        localSignal *= np.hanning(int(self.fs * self.timeStep))
        raw_mag = 20*np.log10(np.abs(np.fft.fft(localSignal)[self.bandwidthIndex]))
        safety_factor = 0
        avg_mag = tools.avg_binning(raw_mag, self.resolution)   
        if (int(self.timeStep*step)%1 == 0):
            self.noise_offset = tools.calculate_offset(avg_mag, self.bandWidth, 1e3)   
        avg_mag += self.noise_offset + safety_factor
        filtered_mag = np.clip(avg_mag, a_min=0., a_max=None)
        tools.channel_filter(filtered_mag, self.resolution, self.bandWidth, self.pass_bandwidth)
        centroid = tools.centroid(self.simplifiedFreq, filtered_mag)

        if simplify:
            return avg_mag, centroid
        else:
            return raw_mag, centroid

    def find_channels(self):
        pass

    def plot(self, maxStep=0, outputType='gif'):
        steps = range(maxStep)
        IO.double_plot(self, steps = steps, simplify = True, outputType = outputType)




