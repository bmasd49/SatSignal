from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import numpy as np
import datetime

def readFile(filename):
    """read wavefile and return sampling rate, as well as recorededSignal as a complex value made of both channels of the wavefile."""
    fs, channels = wavfile.read(filename)
    complexSignal = channels[:,0] + 1j * channels[:,1]
    return fs, complexSignal


def plotting(signal, steps = None, simplify = False, outputType = None):
    plt.figure(figsize=(12,6), dpi=300)
    scale = 1e-3 #convert Hz to kHz
    if simplify:
        f = signal.simplifiedFreq * scale
    else:
        f = signal.fullFreq * scale
    centroids = np.zeros_like(steps, dtype=float)
    os.system("rm ./gif/*.png")

    for step in range(len(steps)):
        print(f"Step {step}/{len(steps)}")
        mag, centroid = signal.spectrogram(step=step, simplify=simplify)
        centroid = (centroid + signal.signalOffset)*scale
        centroids[step] = centroid
        plt.plot(f+signal.signalOffset*scale, mag, '.', markersize=1.)
        plt.axvline(x=centroid, color='red', markersize=0.1, label=f'Centroid={centroid:.1f}kHz')
        plt.ticklabel_format(useOffset=False)
        plt.ylim([-40,50])
        plt.yticks(np.arange(50,-50,-10))
        plt.xticks(np.arange(signal.expectedFreq-signal.bandWidth/2, signal.expectedFreq+signal.bandWidth/2+10e3, 10e3)*scale)
        plt.title(f'{signal.name}: Frequency domain at step {step:03d} ({datetime.timedelta(seconds=int(step*signal.timeStep))}) with each step = {signal.timeStep}s')
        plt.xlabel(f'Frequency (kHz)')
        plt.ylabel('Amplitude (dB)')
        plt.legend()
        plt.grid()
        plt.savefig(f'./gif/{step:03d}.png')
        plt.clf()

    plt.plot(centroids, range(len(centroids)), '.')
    plt.ticklabel_format(useOffset=False)
    plt.xlabel("Centroid position [kHz]")
    plt.ylabel("Time step")
    plt.title(f"{signal.name}: The shift of centroid by time")
    plt.savefig(f"CentroidGraph-{signal.name}.png")
    if outputType == None:
        outputType = 'gif'
    os.system(f"ffmpeg -y -framerate {int(1/signal.timeStep)} -i ./gif/%03d.png -i ./palette.png -lavfi paletteuse {signal.name}.{outputType}")
