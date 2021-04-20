import tracker
#import rtlsdr
import multiprocessing
from datetime import datetime

if __name__ == '__main__':
    signal = tracker.signal('PIXL1', center_frequency=401e6, expectedFreq=400575e3, step_timelength=0.2, bandWidth=60e3, resolution=600)
    signal.read_info_from_wav('/resources/wav/SDRSharp_20210326_204124Z_401000000Hz_IQ.wav', time_end=60)

    start_time = datetime.now()

    reading_process = multiprocessing.Process(target=signal.read_data_from_wav)
    calculating_process = multiprocessing.Process(target=signal.find_centroids)
    plotting_process1 = multiprocessing.Process(target=signal.plot)
    plotting_process2 = multiprocessing.Process(target=signal.plot)
    plotting_process3 = multiprocessing.Process(target=signal.plot)

    reading_process.start()
    calculating_process.start()
    plotting_process1.start()
    plotting_process2.start()
    plotting_process3.start()

    reading_process.join()
    calculating_process.join()
    plotting_process1.join()
    plotting_process2.join()
    plotting_process3.join()

    print(f"Finished in {datetime.now() - start_time}")


