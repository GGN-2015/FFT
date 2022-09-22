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
    tmp  = [float(x) for x in line.split()] [:lineWidth]
    df.append(tmp)

# take a log is reasonable because its value is really high
# +1 to avoid number 0
df = np.log(np.array(df) + 1)

print(df)

sns.heatmap(df.T, cmap="YlOrRd")
plt.xlabel("Time")
plt.ylabel("Freqency (log) Amplitude")
plt.show()

plt.savefig('./Data/TMP/TMP.png')
