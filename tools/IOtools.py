from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import numpy as np

def readFile(filename):
    """read wavefile and return sampling rate, as well as recorededSignal as a complex value made of both channels of the wavefile."""
    fs, channels = wavfile.read(filename)
    complexSignal = channels[:,0] + 1j * channels[:,1]
    return fs, complexSignal


def plotting(signal, steps = None):
    plt.figure(figsize=(8,6), dpi=300)
    scale = 1e-3 #convert Hz to kHz
    f = signal.fullFreq * scale
    for i, step in enumerate(steps):
        print(f"Step {step}/{len(steps)}")
        _, mag, centroid = signal.spectrogram(step=step)
        # f *= scale
        centroid *= scale
        plt.plot(f, mag, '.', markersize=1.)
        plt.axvline(x=centroid, color='red', markersize=0.1, label=f'Centroid={centroid:.1f}kHz')
        plt.ylim([-50,100])
        plt.yticks(np.arange(100,-50,-10))
        plt.xticks(np.arange(-signal.bandWidth/2, signal.bandWidth/2+10e3, 10e3)*scale)
        plt.title(f'Frequency domain at step {step:02d} with each step = {signal.timeStep}s')
        plt.xlabel(f'Frequency (kHz), offset={int(signal.signalOffset/1000)}kHz')
        plt.ylabel('Amplitude (dB)')
        plt.legend()
        plt.grid()
        plt.savefig(f'./gif/{i:03d}.png')
        plt.clf()
    os.system("ffmpeg -y -framerate 5 -i ./gif/%03d.png -i ./gif/palette.png -lavfi paletteuse -r 5 output.gif")
    # for i, time in enumerate(t[1:-1]):
        # plt.plot(f, spectrum[:,i+1], '.', markersize=1)
        # plt.axvline(x=maxFreq[i+1])
        # plt.ylim([-120,100])
        # plt.yticks(np.arange(0,-130,-10))
        # plt.xticks(np.arange(Hz_to_kHz(f_min), Hz_to_kHz(f_max)*1.1, Hz_to_kHz(f_max-f_min)/10))
        # plt.grid()
        # # plt.xlabel('Frequency (Hz)')
        # # plt.ylabel('Amplitude (dB)')
        # plt.title(f'STFT Magnitude at {time} s')
        # plt.savefig(f'./gif/{i:03d}.png')
        # plt.clf()
    # os.system("ffmpeg -y -i ./gif/%03d.png -i ./gif/palette.png -lavfi paletteuse -r 5 output.gif")
