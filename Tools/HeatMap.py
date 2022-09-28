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
FRAME_RATE_FILE = "./Data/JSON/frameRate.json"
FRAME_RATE = 16384
# BASE_RATE  = 48000 

# import process is very slow
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def GetWavFileName(filename: str):
    lis = filename.split('.')[:-1]
    lis.append('wav')
    return ('.'.join(lis)).replace('FFT', 'WAV')

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

# Get BASE_RATE
wavFile = GetWavFileName(fileName)
import json
frameRate = json.load(open(FRAME_RATE_FILE))
sys.stderr.write("[HeatMap] wavFile = %s\n" % wavFile)

assert frameRate.get(wavFile) is not None
BASE_RATE = int(frameRate[wavFile])
sys.stderr.write("[HeatMap] BASE_RATE = %d\n" % BASE_RATE)

# read in every line from the file
df=[]
for line in open(fileName):
    tmp  = [float(x) for x in line.split()] [:lineWidth]
    df.append(tmp)

# Read in MAN FILE
if HAS_MANFILE:
    import GenerateManSeq
    manSeq = GenerateManSeq.GenerateManSeq(len(df), manFile, FRAME_RATE, \
            BASE_RATE, (WIDTH + 1) * MAX_HEIGHT)

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

# Calculate Neighborhood Max
def CalculateNeighborhoodMax(arr, width):
    assert width > 0
    ave = []
    for i in range(arr.shape[0]):
        L = max(0, i - width)
        R = min(arr.shape[0] - 1, i + width)

        ave.append(arr[L : R+1].max())
    assert len(ave) == len(arr)
    return np.array(ave)

# Calculate Neighborhood Min 
def CalculateNeighborhoodMin(arr, width):
    assert width > 0
    ave = []
    for i in range(arr.shape[0]):
        L = max(0, i - width)
        R = min(arr.shape[0] - 1, i + width)

        ave.append(arr[L : R+1].min())
    assert len(ave) == len(arr)
    return np.array(ave)


# Calculate Neighborhood Min 
def CalculateNeighborhoodDelta(arr, width):
    return (
            CalculateNeighborhoodMax(arr, width) -
            CalculateNeighborhoodMin(arr, width))

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

# calculate total mean
def CalculateNeighborhoodTotalMean(arr, width):
    assert width > 0
    ave = []
    for i in range(arr.shape[0]):
        cnt = 0
        ans = 0
        for j in range(-width, width + 1):
            pos = i + j
            if 0 <= pos and pos < arr.shape[0]:
                ans += arr[pos].mean()
                cnt += 1
        ave.append(ans / cnt)
    assert len(ave) == len(arr)
    return np.array(ave)

# calculate std var
def CalculateNeighborhoodVar(arr, width):
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
        std.append((var/cnt - (ave/cnt)**2))
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
    data_np = np.c_[aveNP, CalculateNeighborhoodMax(aveNP, WIDTH), \
            CalculateNeighborhoodDelta(aveNP, WIDTH)] 
    tags = ["ave", "NbMax", "NbDelta"]

    if HAS_MANFILE:
        data_np = np.c_[data_np, CalculateNeighborhoodMean(manSeq, WIDTH)]
        tags.append("ManCut")
    data_df = pd.DataFrame(data_np, None, tags) 
    sns.lineplot(data_df, ax=ax[axID])

ShowDataInSubPlot(aveL, 1)

# calculate the Middle Freq ave map
aveH = []
for i in range(df.shape[0]):
    aveH.append(np.median(df[i, 732:1024]))
aveH = np.array(aveH)

ShowDataInSubPlot(aveH, 2)

# dump picture into file
plt.savefig('./Data/TMP/TMP.png')

