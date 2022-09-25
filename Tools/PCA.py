import sys

if len(sys.argv) != 3:
    sys.stderr.write("[PCA] Usage: python3 PCA.py <file.fft> <linewidth>\n")
    exit()

# get argv from sys.argv
MAX_WIDTH = 1024
filename  = sys.argv[1]
linewidth = int(sys.argv[2])

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
Model_PCA = PCA(n_components = 0.9) #X.shape[1])
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

Components = Model_PCA.components_
for i in range(Components.shape[0]):
    for j in range(Components.shape[1]):
        print(Components[i,j], end=" ")
    print("")

