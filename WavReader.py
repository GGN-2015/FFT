# !/bin/python3

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

    
    sys.stderr.write("nchannels   : %6d\n" % nchannels)
    sys.stderr.write("sample_width: %6d\n" % sample_width)
    sys.stderr.write("frame_rate  : %6d\n" % frame_rate)
    sys.stderr.write("nframes     : %6d\n" % nchannels)

    data = wavefile.readframes(nframes)

    # <i2: small-endian integer in 2 bytes
    tmp = np.frombuffer(data, dtype='<i2')
    # sig = tmp.reshape(-1, nchannels)
    sig = tmp.reshape(-1, 1)

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
        for j in range(1): # nchannels is 1
            ans += sig[i][j]
        print(ans / nchannels, end = " ")


# python3 WavReader.py <wavfilename>
if len(sys.argv) != 2:
    print("[WavReader] Usage: python3 %s <wavfilename>" % sys.argv[0])
    exit()

# input a wavfile, output a txt
DumpSignal(sys.argv[1])
