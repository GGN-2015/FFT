import sys

# output error message
if len(sys.argv) != 3:
    sys.stderr.write("[ShowWave] Usage: python3 ShowWave.py <input.txt> <CutWidth>")
    exit()

#! you need to install matplotlib
from pylab import *

# preparing arguments from argv
file     = open(sys.argv[1])
cutWidth = int(sys.argv[2])

# read in every line from the file
vals = []
for line in file:
    tmp   = list(map(float, line.split()))
    vals += tmp

    # reading the whole file in is of great-time consume.
    if cutWidth > 0 and len(vals) >= cutWidth:
        break

# curWidth < 0 means do not cut.
if cutWidth > 0:
    vals = vals[:cutWidth]

# output a wave graph
plt.plot(vals)
plt.show()
