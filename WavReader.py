import wave
import numpy as np

from scipy import *
from pylab import *

import sys

def OpenWavFile(filename: str):
    wavefile     = wave.open(filename, 'r')
    
    nchannels    = wavefile.getnchannels()
    sample_width = wavefile.getsampwidth()
    frame_rate   = wavefile.getframerate()
    nframes      = wavefile.getnframes()

    print("nchannels   : %6d" % nchannels)
    print("sample_width: %6d" % sample_width)
    print("frame_rate  : %6d" % frame_rate)
    print("nframes     : %6d" % nchannels)

    data = wavefile.readframes(nframes)

    # <i2: small-endian integer in 2 bytes
    sig = np.frombuffer(data, dtype='<i2').reshape(-1, nchannels)

    # display the curve on the screen
    # plt.plot(sig)
    # plt.show()

    # return the np array
    return nchannels, sig

# output wav signal into chars
def DumpSignal(wavefile):
    nchannels, sig = OpenWavFile(wavefile)

    # output an average channel
    for i in range(len(sig)):
        ans = 0
        for j in range(nchannels):
            ans += sig[i][j]
        print(ans / nchannels, end = " ")


# python3 WavReader.py <wavfilename>
if len(sys.argv) != 2:
    print("[WavReader] Usage: python3 %s <wavfilename>" % sys.argv[0])
    exit()

# input a wavfile, output a txt
DumpSignal(sys.argv[1])
