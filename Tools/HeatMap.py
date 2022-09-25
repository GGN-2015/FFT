import sys

# check argv
if len(sys.argv) not in [3, 4]:
    sys.stderr.write("[HeatMap] Usage: python3 HeatMap.py <file.fft> <LineWidth>\n")
    sys.stderr.write("[HeatMap]    OR: python3 HeatMap.py <file.fft> <file.man> <LineWidth>\n")
    exit()

# music parts
PARTS = [0, 73, 146, 292, 584, 1024]
WIDTH = 4 
MAX_HEIGHT = 16
FRAME_RATE = 16384
BASE_RATE  = 48000 

# import process is very slow
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load argv arguments
if len(sys.argv) == 3:
    HAS_MANFILE = False
    fileName    = sys.argv[1]
    lineWidth   = int(sys.argv[2])
else:
    HAS_MANFILE = True
    fileName    = sys.argv[1]
    manFile     = sys.argv[2]
    lineWidth   = int(sys.argv[3])

# read in every line from the file
df=[]
for line in open(fileName):
    tmp  = [float(x) for x in line.split()] [:lineWidth]
    df.append(tmp)

# Read in MAN FILE
if HAS_MANFILE:
    # every line in the file is a time slot
    slotCnt = len(df)
    manSeq  = [0] * slotCnt
    stotal  = (FRAME_RATE / BASE_RATE) * slotCnt 

    sys.stderr.write("[HeatMap] stotal = %d\n" % stotal)

    for line in open(manFile):
        sl = line.strip()
        if sl == "" or sl[0] == "#": # empty line or comment
            continue
        minute, second = map(int, sl.split(':'))
        stime = minute * 60 + second
        
        # round to an even number
        pos = round(stime / stotal * slotCnt)
        sys.stderr.write("[HeatMap] set pos = %d\n" % pos)

        if 0 <= pos and pos < slotCnt:
            manSeq[pos] = (WIDTH + 1) * MAX_HEIGHT
    manSeq = np.array(manSeq)

# take a log is reasonable because its value is really high
# +1 to avoid number 0
df = np.log(np.array(df) + 1)

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

# calculate the mean value of a neighborhood
def CalculateNeighborhoodMean(arr, width):
    assert width > 0
    ave = []
    for i in range(arr.shape[0]):
        cnt = 0
        ans = 0 # sum value of the neighborhood
        for j in range(-width, width + 1):
            pos = i + j
            if 0 <= pos and pos < arr.shape[0]:
                ans += arr[pos]
                cnt += 1
        ave.append(ans / cnt)
    assert len(ave) == len(arr)
    return np.array(ave)

# calculate std var
def CalculateNeighborhoodStd(arr, width):
    assert width > 0
    std = []
    for i in range(arr.shape[0]):
        cnt = 0
        ave = 0 # sum 
        var = 0 # sqr sum
        for j in range(-width, width + 1):
            pos = i + j
            if 0 <= pos and pos < arr.shape[0]:
                ave += arr[pos]
                var += arr[pos] ** 2
                cnt += 1
        std.append((var/cnt - (ave/cnt)**2) ** 0.5)
    assert len(std) == len(arr)
    return np.array(std)

# calculate the Low Freq ave map
aveL = []
for i in range(df.shape[0]):
    aveL.append(df[i, 0:73].mean())
aveL = np.array(aveL)

# sns.lineplot(np.r_[aveL, CalculateNeighborhoodStd(aveL, WIDTH), CalculateNeighborhoodStd(aveL, WIDTH)],
#        ax = ax[1])

# show subplot in axID
def ShowDataInSubPlot(aveNP, axID):
    data_np = np.c_[aveNP, CalculateNeighborhoodMean(aveNP, WIDTH), CalculateNeighborhoodStd(aveNP, WIDTH)] 
    tags = ["ave", "NbMean", "NbStd"]

    if HAS_MANFILE:
        data_np = np.c_[data_np, CalculateNeighborhoodMean(manSeq, WIDTH)]
        tags.append("ManCut")
    data_df = pd.DataFrame(data_np, None, tags) 
    sns.lineplot(data_df, ax=ax[axID])

ShowDataInSubPlot(aveL, 1)

# calculate the Middle Freq ave map
aveH = []
for i in range(df.shape[0]):
    aveH.append(df[i, 73:292].mean())
aveH = np.array(aveH)

ShowDataInSubPlot(aveH, 2)

# dump picture into file
plt.savefig('./Data/TMP/TMP.png')

