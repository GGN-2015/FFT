#!/bin/python3

import sys

# python3 WavReader.py <wavfilename>
if len(sys.argv) != 3:
    sys.stderr.write("[WavReader] Usage: python3 %s <input.wav> <LineWidth>" % sys.argv[0])
    exit()

import wave
import numpy as np

from scipy import *
from pylab import *

def OpenWavFile(filename: str):
    wavefile     = wave.open(filename, 'r')
    
    nchannels    = wavefile.getnchannels()
    sample_width = wavefile.getsampwidth()
    frame_rate   = wavefile.getframerate()
    nframes      = wavefile.getnframes()

    # output the basic message onto screen(stderr)
    sys.stderr.write("[WavReader] nchannels   : %10d.\n" % nchannels)
    sys.stderr.write("[WavReader] sample_width: %10d.\n" % sample_width)
    sys.stderr.write("[WavReader] frame_rate  : %10d.\n" % frame_rate)
    sys.stderr.write("[WavReader] nframes     : %10d.\n" % nframes)

    # sometimes ffmpeg output wav with sample_width = 1
    assert sample_width == 2
    assert nchannels in [1, 2]
    data = wavefile.readframes(nframes)

    # <i2: small-endian integer in 2 bytes
    tmp = np.frombuffer(data, dtype='<i2')
    sig = tmp.reshape(-1, nchannels)

    # display the curve on the screen
    # plt.plot(sig)
    # plt.show()

    # return the np array
    return nchannels, sig

# output wav signal into chars
def DumpSignal(wavefile, lineWidth):
    nchannels, sig = OpenWavFile(wavefile)

    # leave a single channel
    if nchannels == 2:
        # ans = np.around((sig[:,0] + sig[:,1]) / 2, )
        ans = sig[:,0]
    else:
        ans = sig[:,0]
    
    sys.stderr.write("[WavReader] len(ans)    : %10d.\n" % len(ans))
    
    # output the merged signal
    for i in range(len(ans)):
        print(ans[i], end = " ")

        # output a new line after lineWidth reached
        if lineWidth > 0 and i % lineWidth == lineWidth - 1:
            print("")

# input a wavfile, output a txt
DumpSignal(sys.argv[1], int(sys.argv[2]))
sys.stderr.write("[WavReader] Done.\n")
