import numpy as np
import seaborn as sns
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

SIZE = 1024

df=[]
for line in open("0022.fft"):
    data = []
    tmp  = line.split()
    tmp  = [float(x) for x in tmp] [:1024]
    data = [0] * SIZE
    rate = int(len(tmp) / SIZE)
    for i in range(len(tmp)):
        data[i // rate] = max(data[i // rate], tmp[i])
    df.append(data)

###############################################################

nfilt = 40
low_freq_mel = 0
sample_rate = 4096 # 采样频率？
NFFT = 16384 # N点FFT

mag_frames = df
pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))  # 功率谱

high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))  # 求最高hz频率对应的mel频率
# 我们要做40个滤波器组，为此需要42个点，这意味着在们需要low_freq_mel和high_freq_mel之间线性间隔40个点
mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # 在mel频率上均分成42个点
hz_points = (700 * (10 ** (mel_points / 2595) - 1))  # 将mel频率再转到hz频率
# bin = sample_rate/2 / NFFT/2=sample_rate/NFFT    # 每个频点的频率数
# bins = hz_points/bin=hz_points*NFFT/ sample_rate    # hz_points对应第几个fft频点
bins = np.floor((NFFT + 1) * hz_points / sample_rate)


fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
for m in range(1, nfilt + 1):
    f_m_minus = int(bins[m - 1])  # 左
    f_m = int(bins[m])  # 中
    f_m_plus = int(bins[m + 1])  # 右

    for k in range(f_m_minus, f_m):
        fbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
    for k in range(f_m, f_m_plus):
        fbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])
filter_banks = np.dot(pow_frames, fbank.T)
filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # 数值稳定性
filter_banks = 20 * np.log10(filter_banks)  # dB

###############################################################

print(np.array(df) + 1)
 
df = np.log(np.array(df))

sns.heatmap(df, cmap="YlOrRd" )
plt.show()
