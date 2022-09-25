import sys

if len(sys.argv) != 4:
    sys.stderr.write("[PCA] Usage: python3 PCA.py <file.fft> \
<file.man> <linewidth>\n")
    exit()

# get argv from sys.argv
MAX_WIDTH    = 1024
filename     = sys.argv[1]
manfile      = sys.argv[2]
linewidth    = int(sys.argv[3])
N_COMPONENTS = 0.9 
FRAME_RATE   = 16384
BASE_RATE    = 48000

# necessary import
from sklearn.decomposition import PCA
import numpy as np

# get numpt array from file
def GetNumpyFromFile(filename, lineWidth):
    ans = []
    for line in open(filename):
        sl = line.strip()
        if sl != "":
            tmp = list(map(float, sl.split()))
            assert len(tmp) == lineWidth
            ans.append(tmp[:MAX_WIDTH])
    return np.array(ans)

# X is the data to do PCA
X = GetNumpyFromFile(filename, linewidth)

# Z-score normalizationg
from sklearn import preprocessing
X = preprocessing.scale(X)

# run pca model on X
# calculate variance_ratio for all column
Model_PCA = PCA(n_components = N_COMPONENTS) #X.shape[1])
Model_PCA.fit(X)

# output msg like variance_ratio, singular_value
# print(Model_PCA.n_components_)
# print(Model_PCA.explained_variance_ratio_)
# print(Model_PCA.singular_values_)

# output explained_variance_ratio
# for i in range(len(Model_PCA.explained_variance_ratio_)):
#     print(Model_PCA.explained_variance_ratio_[i], end=" ")
# print("")

# newX = Model_PCA.fit_transform(X)
# print(newX)

sys.stderr.write("[PCA] n_components_ = %d\n" % \
        Model_PCA.n_components_)
sys.stderr.write("[PCA] var_ratio = " + str(Model_PCA.explained_variance_ratio_) + "\n")
sys.stderr.write("[PCA] components_[1] = " + str(Model_PCA.components_[1]) + "\n")

import pandas as pd

# get the data after pca transform
X_pca = Model_PCA.transform(X)
sys.stderr.write("[PCA] X_pca.shape = " + str(X_pca.shape) + "\n")

# get the man file
import GenerateManSeq

manSeq = GenerateManSeq.GenerateManSeq(X.shape[0], \
        manfile, FRAME_RATE, BASE_RATE, 1)

# calculate prefix sum
def GetPrefixSum(manSeq):
    preSeq = [0] * len(manSeq)
    for i in range(1, len(manSeq)):
        preSeq[i] = preSeq[i - 1] + manSeq[i]
    return np.array(preSeq)
manSeq = GetPrefixSum(manSeq)

import seaborn as sns
import matplotlib.pyplot as plt

# construct dataframe (N = 2)
# data_df = pd.DataFrame(data = np.c_[X_pca, manSeq], \
#        columns = ['PcaMain1', 'PcaMain2', 'manSeq'])

from sklearn.svm import LinearSVC
linear_svm = LinearSVC().fit(X_pca, manSeq)
y_Predict  = linear_svm.predict(X_pca)

def GetMode(lis):
    cnt = {}
    for x in lis:
        if cnt.get(x) is None:
            cnt[x] = 1
        else:
            cnt[x] += 1
    tmpcnt = 0
    tmpans = -1
    for x in cnt:
        if cnt[x] > tmpcnt:
            tmpcnt = cnt[x]
            tmpans = x
    assert tmpans != -1
    return tmpans

# get neighborhood Mode
def GetNeighborhoodMode(seq, WIDTH):
    ans = []
    for i in range(len(seq)):
        lis = []
        for j in range(-WIDTH, WIDTH + 1):
            pos = i + j
            if 0 <= pos and pos < len(seq):
                lis.append(seq[pos])
        ans.append(GetMode(lis))
    return np.array(ans)

y_Predict = GetNeighborhoodMode(y_Predict, 5)

from sklearn.metrics import classification_report
print(classification_report(manSeq, y_Predict))

sns.lineplot(
        pd.DataFrame(np.c_[manSeq, y_Predict], 
            columns=['manSeq', 'y_Predict']))

# display scatterplot
# sns.scatterplot(x="PcaMain1", y="PcaMain2", hue="manSeq", data=data_df)

# dump picture into file
plt.savefig('./Data/TMP/PCA_TMP.png')

# output all the Components after PCA
# Components = Model_PCA.components_
# for i in range(Components.shape[0]):
#     for j in range(Components.shape[1]):
#         print(Components[i,j], end=" ")
#     print("")

