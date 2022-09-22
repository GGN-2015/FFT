import numpy as np
import scipy.io.wavfile as wf
def dumpWAV(FullMusicRail: np.ndarray, WAVFileName = "a.wav", SamplingRate = 44100):
    wf.write(WAVFileName, SamplingRate, FullMusicRail)

# output error message
import sys
if len(sys.argv) != 3:
    sys.stderr.write("[WavWriter.Error] Usage python3 WavWriter.py <file.txt> <dest.wav>")
    exit()

# input the content of a file.
filename = sys.argv[1]
vals = []
for line in open(filename):
    vals += list(map(int, map(float, line.split())))

sys.stderr.write("[WavCreator] len(vals) = %d\n" % len(vals))
dumpWAV(np.array(vals, dtype=np.int16), sys.argv[2], 44100)
