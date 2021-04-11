import tools.signalProcessing as signal
import tools.IOtools as io

if __name__=='__main__':
    # APT = signal.signal('NOAA15', './inputSignals/station1_yagi_SDRSharp_20170312_060959Z_137650kHz_IQ.wav', signalOffset=137.65e6, timeStep=1.)
    # PSK = signal.signal('NOAA15', './inputSignals/SDRSharp_20180618_195718Z_137900000Hz_IQ.wav', signalOffset=137.9e6, timeStep=1.)
    PIXL1 = signal.signal('CubeSat', './inputSignals/SDRSharp_20210326_204124Z_401000000Hz_IQ.wav'\
            , signalOffset=401e6, expectedFreq=400575e3, timeStep=0.3, bandWidth=50e3)
    io.plotting(PIXL1, steps=range(PIXL1.totalLength), simplify=True)


