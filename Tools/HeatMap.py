import sys

# check argv
if len(sys.argv) != 3:
    sys.stderr.write("[HeatMap] Usage: python3 HeatMap.py <file.fft> <LineWidth>")
    exit()

# import process is very slow
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# load argv arguments
fileName  = sys.argv[1]
lineWidth = int(sys.argv[2])

# read in every line from the file
df=[]
for line in open(fileName):
    data = []
    tmp  = line.split()
    tmp  = [float(x) for x in tmp] [:lineWidth]
    df.append(data)

# take a log is reasonable because its value is really high
df = np.log(np.array(df))

sns.heatmap(df.T, cmap="YlOrRd")
plt.xlabel("Time")
plt.ylabel("Freqency (log) Amplitude")
plt.show()
