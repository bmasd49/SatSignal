from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import numpy as np
import datetime
import soundfile as sf
PATH=os.path.dirname(os.path.dirname(__file__))


def read_info_from_wav(wav_path, step_timelength, time_begin, time_end):
    with sf.SoundFile(PATH+wav_path, 'r') as f:
        fs= f.samplerate
        step_framelength = int(step_timelength * fs)
        max_step = int(f.frames / step_framelength) 
        f.subtype
        if time_begin < 0:
            time_begin = 0
        if (time_end == None) or (time_end * fs > f.frames):
            time_end = f.frames/fs
    return fs, step_framelength, max_step, time_begin, time_end

def read_data_from_wav(filename, fs, step_timelength, step_framelength, time_begin, time_end, time_data):
    with sf.SoundFile(PATH+filename, 'r') as f:
        # bitrate_dictionary = {'PCM_U8':255, 'PCM_S8':127, 'PCM_16': 32767}
        # normalize_factor = bitrate_dictionary[f.subtype]
        frame_begin = int(time_begin*fs)
        frame_end = frame_begin + int( int((time_end - time_begin) / step_timelength) * step_timelength * fs)
        f.seek(frame_begin)
        step = -1
        while f.tell() < frame_end:
            step += 1
            raw_time_data = f.read(frames=step_framelength)
            time_data.put((step, raw_time_data[:,0] + 1j * raw_time_data[:,1]))
        time_data.put(None)

def plot(signal, outputType = None):
    plt.figure(figsize=(10,5))
    scale = 1e-3 #convert Hz to kHz
    f = signal.simplifiedFreq * scale
    centroids = np.empty(signal.total_step)

    while True:
        queue_output = signal.freq_data.get()
        if queue_output == 'END':
            signal.freq_data.put('END')
            break
        
        # mag, centroid = signal.spectrogram(step=step, simplify=simplify)
        step, centroid, mag = queue_output
        print(f"\t{step/signal.total_step*100:.2f} %", end="\r")
        plt.plot(f+signal.center_frequency*scale, mag, '.', markersize=1.)
        
        if centroid != None:
            centroid = (centroid + signal.center_frequency)*scale
            plt.axvline(x=centroid, color='red', markersize=0.1, label=f'Centroid={centroid:.1f}kHz')
        centroids[step] = centroid
        plt.ticklabel_format(useOffset=False)
        plt.ylim([-20,40])
        plt.yticks(np.arange(40,-30,-10))
        plt.xticks(np.arange(signal.expectedFreq-signal.bandWidth/2, signal.expectedFreq+signal.bandWidth/2+signal.bandWidth/10, signal.bandWidth/10)*scale)

        # plt.xticks(np.arange(signal.expectedFreq-signal.bandWidth/2, signal.expectedFreq+signal.bandWidth/2+10e3, 10e3)*scale)
        plt.title(f'{signal.name}: Frequency domain at step {step:03d} ({datetime.timedelta(seconds=int(step*signal.step_timelength))}) with each step = {signal.step_timelength}s')
        plt.xlabel(f'Frequency (kHz)')
        plt.ylabel('Amplitude (dB)')
        #plt.legend()
        plt.grid()
        plt.savefig(f'{PATH}/outputs/timeseries/{step:04d}.png', dpi=100)
        plt.clf()


# def waterfall(signal):
#     for i in range(signal.total_step):
#         if centroids[i] != None:
#             plt.plot(centroids[i], i, 'r.')

#     #plt.plot(centroids, range(len(centroids)), '.')
#     plt.grid()
#     plt.ylim([0,signal.total_step+1])
#     plt.xlim([(signal.expectedFreq-5e3-1e3)*scale, (signal.expectedFreq+5e3+1e3)*scale])
#     plt.xticks(np.arange(signal.expectedFreq-5e3, signal.expectedFreq+5e3+1e3, 1e3)*scale)
#     plt.ticklabel_format(useOffset=False)
#     plt.xlabel("Centroid position [kHz]")
#     plt.ylabel("Time step")
#     plt.title(f"{signal.name}: The shift of centroid by time")
#     plt.savefig(f'{PATH}/outputs/images/Center_position_{signal.name}.png', dpi=300)

#     if outputType == None:
#         outputType = 'gif'
#     os.system(f"ffmpeg -y -framerate {int(1/signal.step_timelength)} -i {PATH}/outputs/timeseries/%04d.png -i {PATH}/resources/palette.png -lavfi paletteuse {PATH}/outputs/animations/{signal.name}.{outputType}")
#     if os.name == 'nt':
#         os.system(f"del {os.path.normpath(PATH+'/outputs/timeseries/*.png')}")
#     else:
#         os.system(f"rm {PATH}/outputs/timeseries/*.png")



def double_plot(signal, outputType = None):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(8,8))
    fig.tight_layout(pad=2.)
    scale = 1e-3 #convert Hz to kHz
    f = signal.simplifiedFreq * scale

    centroids = np.empty(signal.total_step)

    ax2.ticklabel_format(useOffset=False)
    ax2.grid()
    ax2.set_ylim([0,signal.total_step+1])
    ax2.set_xlim([(signal.expectedFreq-5e3-1e3)*scale, (signal.expectedFreq+5e3+1e3)*scale])
    ax2.set_xlabel("Frequency (kHz)")
    ax2.set_ylabel("Time step")
    ax2.set_title(f"{signal.name}: Centroid position")
    ax2.set_xticks(np.arange(signal.expectedFreq-5e3, signal.expectedFreq+5e3+1e3, 1e3)*scale)

    for i in range(signal.total_step):
        print(f"{int(i/signal.total_step*100)}%")
        # mag, centroid = signal.spectrogram(step=step, simplify=simplify)
        step, centroid, mag = signal.freq_data.get()
        ax1.plot(f+signal.center_frequency*scale, mag, '.', markersize=3.)        
        if centroid != None:
            centroid = (centroid + signal.center_frequency)*scale
            ax1.axvline(x=centroid, color='red', markersize=0.1)
            ax2.plot(centroid, step, 'r.', markersize=3.)
        ax1.ticklabel_format(useOffset=False)
        ax1.grid()
        ax1.set_ylim([-20,40])
        ax1.set_yticks(np.arange(40,-30,-10))
        ax1.set_xticks(np.arange(signal.expectedFreq-signal.bandWidth/2, signal.expectedFreq+signal.bandWidth/2+signal.bandWidth/10, signal.bandWidth/10)*scale)
        ax1.set_title(f'{signal.name}: Power spectral density at step {step:04d} ({datetime.timedelta(seconds=int(step*signal.step_timelength))}) with each step = {signal.step_timelength}s')
        ax1.set_ylabel('Amplitude (dB)')
        fig.savefig(f'{PATH}/outputs/timeseries/{step:04d}.png', dpi=300)
        ax1.clear()
    print("Finished plotting")
    if outputType == None:
        outputType = 'gif'
    os.system(f"ffmpeg -y -framerate {int(1/signal.step_timelength)} -i {PATH}/outputs/timeseries/%04d.png -i {PATH}/resources/palette.png -lavfi paletteuse {PATH}/outputs/animations/{signal.name}.{outputType}")

    if os.name == 'nt':
        os.system(f"del {os.path.normpath(PATH+'/outputs/timeseries/*.png')}")
    else:
        os.system(f"rm {PATH}/outputs/timeseries/*.png")
