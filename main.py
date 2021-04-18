import tools.signalProcessing as process
import tools.IOtools as io
# import pyrtlsdr as sdr

if __name__=='__main__':
    # signal = process.signal('NOAA18', './inputSignals/SDRSharp_20180327_185552Z_137912500Hz_IQ.wav', center_frequency=137912500, bandWidth=80e3, expectedFreq= 137.910e6, timeStep=1., resolution=1800, pass_bandwidth=200)
    # APT2 = process.signal('NOAA18_2', './inputSignals/SDRSharp_20190521_152538Z_137500000Hz_IQ.wav', center_frequency=137500000, bandWidth=80e3, expectedFreq= 137500000, timeStep=1., resolution=1800)
    # signal = process.signal('ISS', './inputSignals/SDRSharp_20170527_003520Z_145900000Hz_IQ.wav', center_frequency=145900000, bandWidth=80e3, expectedFreq= 145825000, timeStep=0.1, resolution=1800, pass_bandwidth=1000)
    signal= process.signal('ISS', './inputSignals/iss_aprs_alotof_signals_SDRSharp_20170816_163505Z_145828040Hz_IQ.wav', center_frequency=145828040, bandWidth=40e3, expectedFreq= 145825000, timeStep=0.2, resolution=1800, pass_bandwidth=1000)
    # io.plotting(ISS2, steps=range(60), simplify=True, outputType = 'mp4')
    # PSK = process.signal('Meteor', './inputSignals/SDRSharp_20180618_195718Z_137900000Hz_IQ.wav', center_frequency=137.9e6, expectedFreq=137.9e6, bandWidth=200e3, timeStep=1., resolution=1800)
    # PIXL1 = process.signal('PIXL1', './inputSignals/SDRSharp_20210326_204124Z_401000000Hz_IQ.wav', center_frequency=401e6, expectedFreq=400575e3, timeStep=0.5, bandWidth=60e3)
    signal.plot(maxStep=300)


