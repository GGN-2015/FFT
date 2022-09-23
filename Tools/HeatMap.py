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

# music part
parts = [0, 73, 146, 292, 584, 1024]

print(df)
# set picture size
plt.figure(figsize=(1920 / 100, 1080 / 100))

# two graph in a column
fig, ax = plt.subplots(3, 1, constrained_layout=True, \
        figsize=(19.20, 10.80))

# output the HeatMap
sns.heatmap(df.T, cmap="YlOrRd", ax=ax[0])

# output the Average Map
# ave = []
# for i in range(df.shape[0]):
#     ave.append(df[i].mean())
# ave = np.array(ave)
# sns.lineplot(ave, ax=ax[1])

# output the Low Freq ave map
ave = []
for i in range(df.shape[0]):
    ave.append(df[i, 0:73].mean())
ave = np.array(ave)
sns.lineplot(ave, ax=ax[1])

# output the Middle Freq ave map
ave = []
for i in range(df.shape[0]):
    ave.append(df[i, 73:292].mean())
ave = np.array(ave)
sns.lineplot(ave, ax=ax[2])

# dump picture into file
plt.savefig('./Data/TMP/TMP.png')

