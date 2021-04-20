import numpy as np
import tools
import signal_io as io
import multiprocessing

class signal:
    def __init__(self, signalName, center_frequency = None, expectedFreq = None, bandWidth = None, timeInterval = None, step_timelength = None, resolution = None, pass_bandwidth = None):
        self.name = signalName
        #self.fs, self.rawSignal = io.readFile(signalPath)
        self.safety = 0.5

        if expectedFreq == None:
            self.expectedFreq = 0
        else:
            self.expectedFreq = expectedFreq

        if resolution  == None:
            self.resolution = 1000
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

        if step_timelength == None:
            self.step_timelength = 1.
        else:
            self.step_timelength = step_timelength

        if pass_bandwidth == None:
            self.pass_bandwidth = 1000
        else:
            self.pass_bandwidth = pass_bandwidth

        self.time_data = multiprocessing.Queue()
        self.freq_data = multiprocessing.Queue()


    def read_info_from_wav(self, wav_path, time_begin=0, time_end=None):
        self.path = wav_path
        self.fs, self.step_framelength, self.max_step, self.time_begin, self.time_end = io.read_info_from_wav(wav_path, self.step_timelength, time_begin, time_end)
        fullFreq = np.fft.fftfreq(int(self.fs * self.step_timelength), 1/(self.fs))
        self.bandwidthIndex = np.where(np.logical_and(fullFreq > self.expectedFreq - self.center_frequency - self.bandWidth/2, fullFreq < self.expectedFreq - self.center_frequency + self.bandWidth/2))
        self.fullFreq = fullFreq[self.bandwidthIndex]
        self.simplifiedFreq = tools.avg_binning(self.fullFreq, self.resolution)
        self.total_step = int((self.time_end-self.time_begin)/self.step_timelength)

    def read_data_from_wav(self):
        io.read_data_from_wav(self.path, self.fs, self.step_timelength, self.step_framelength, self.time_begin, self.time_end, self.time_data)

    def find_centroids(self):
        while True:
            queue_output = self.time_data.get()
            if queue_output == None:
                self.time_data.put(None)
                break
            step, localSignal = queue_output
            localSignal *= np.hanning(self.step_framelength)
            raw_mag = 20*np.log10(np.abs(np.fft.fft(localSignal)[self.bandwidthIndex]))
            safety_factor = 0
            avg_mag = tools.avg_binning(raw_mag, self.resolution)   
            noise_offset = tools.calculate_offset(avg_mag)   
            avg_mag += noise_offset + safety_factor
            filtered_mag = np.clip(avg_mag, a_min=0., a_max=None)
            tools.channel_filter(filtered_mag, self.resolution, pass_step_width = int(self.pass_bandwidth / self.bandWidth * self.resolution))
            centroid = tools.centroid(self.simplifiedFreq, filtered_mag)
            self.freq_data.put((step, centroid, avg_mag))
        self.freq_data.put('END')

    def find_channels(self):
        pass

    def plot(self,  outputType='mp4'):
        io.plot(self, outputType = outputType)



