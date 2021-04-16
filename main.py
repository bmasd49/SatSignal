import tools.signalProcessing as signal
import tools.IOtools as io

if __name__=='__main__':
    # APT = signal.signal('NOAA15', './inputSignals/station1_yagi_SDRSharp_20170312_060959Z_137650kHz_IQ.wav', signalOffset=137.65e6, bandWidth=60e3, expectedFreq= 137.680e6, timeStep=1., resolution=1800)
    # io.plotting(APT, steps=range(60), simplify=True)
    # APT = signal.signal('NOAA18', './inputSignals/SDRSharp_20180327_185552Z_137912500Hz_IQ.wav', signalOffset=137912500, bandWidth=80e3, expectedFreq= 137.910e6, timeStep=1., resolution=1800)
    # APT2 = signal.signal('NOAA18_2', './inputSignals/SDRSharp_20190521_152538Z_137500000Hz_IQ.wav', signalOffset=137500000, bandWidth=80e3, expectedFreq= 137500000, timeStep=1., resolution=1800)
    # io.plotting(APT2, steps=range(60), simplify=True)
    # ISS = signal.signal('ISS', './inputSignals/SDRSharp_20170527_003520Z_145900000Hz_IQ.wav', signalOffset=145900000, bandWidth=80e3, expectedFreq= 145825000, timeStep=0.1, resolution=1800)
    # io.plotting(ISS, steps=range(60*4), simplify=True)
    ISS2 = signal.signal('ISS', './inputSignals/iss_aprs_alotof_signals_SDRSharp_20170816_163505Z_145828040Hz_IQ.wav', signalOffset=145828040, bandWidth=40e3, expectedFreq= 145825000, timeStep=0.1, resolution=1800)
    io.plotting(ISS2, steps=range(60*10), simplify=True, outputType = 'mp4')
    # PSK = signal.signal('Meteor', './inputSignals/SDRSharp_20180618_195718Z_137900000Hz_IQ.wav', signalOffset=137.9e6, expectedFreq=137.9e6, bandWidth=80e3, timeStep=1., resolution=1800)
    # io.plotting(PSK, steps=range(60), simplify=True)
    # PIXL1 = signal.signal('PIXL1', './inputSignals/SDRSharp_20210326_204124Z_401000000Hz_IQ.wav'\
            # , signalOffset=401e6, expectedFreq=400575e3, timeStep=0.5, bandWidth=60e3)
    # io.plotting(PIXL1, steps=range(120), simplify=True)


