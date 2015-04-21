#
#	Implementation of principal component analysis plots on dummy example
#
#	First version: Hanna Lilja, 2015-04-21
#

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# The data should be represented by a 2d array where each row is a data instance and each column represents a feature
# n_dim is the number of dimensions the data is reduced to, 2 and 3 dimensions are suported by the plot function
def doPCA(data, n_dim = 2):
	thePCA = PCA(n_components = n_dim)
	dimRed = thePCA.fit_transform(data)
	return dimRed

# Plots the result of PCA, supports 2d and 3d plots
def plotPCA(pcadata, labels):
	nsamp = np.shape(pcadata)[0]
	dims = np.shape(pcadata)[1]
	if (np.shape(labels)[0] != nsamp):
		print 'Error: labels do not match data'
	elif (dims == 2):
		for i in range(nsamp):
			samp = pcadata[i,:]
			plt.plot(samp[0], samp[1], labels[i]+'o')
		plt.show()
	elif (dims == 3):
		fig = plt.figure()
		axeObj = fig.add_subplot(111, projection='3d')
		for i in range(nsamp):
			samp = pcadata[i,:]
			axeObj.scatter(samp[0], samp[1], samp[2], c = labels[i])
		plt.show()
	else:
		print 'Error: can not plot in that dimension'

madeUpData = np.array([
	[0.2, 0.2, 0.1, 0.1, 0.2, 0.2], [0.3, 0.2, 0.0, 0.1, 0.2, 0.2], [0.3, 0.2, 0.1, 0.0, 0.2, 0.2], [0.2, 0.3, 0.0, 0.1, 0.1, 0.3], [0.2, 0.3, 0.0, 0.0, 0.3, 0.2],
	[0.1, 0.1, 0.1, 0.1, 0.1, 0.5], [0.1, 0.1, 0.1, 0.1, 0.0, 0.6], [0.1, 0.0, 0.1, 0.0, 0.1, 0.7], [0.1, 0.1, 0.1, 0.0, 0.2, 0.5], [0.0, 0.2, 0.0, 0.1, 0.1, 0.6],
	[0.1, 0.1, 0.3, 0.3, 0.1, 0.1], [0.0, 0.1, 0.4, 0.3, 0.1, 0.1], [0.0, 0.0, 0.5, 0.3, 0.1, 0.1], [0.1, 0.0, 0.6, 0.2, 0.1, 0.0], [0.0, 0.1, 0.3, 0.5, 0.1, 0.0],
	[0.3, 0.1, 0.1, 0.1, 0.3, 0.1], [0.2, 0.2, 0.1, 0.1, 0.4, 0.0], [0.4, 0.1, 0.0, 0.1, 0.3, 0.1], [0.3, 0.0, 0.1, 0.1, 0.4, 0.1], [0.4, 0.1, 0.0, 0.1, 0.4, 0.0]])

madeUpLabels = ['y', 'y', 'y', 'y', 'y', 'b', 'b', 'b', 'b', 'b', 'r', 'r', 'r', 'r', 'r', 'g', 'g', 'g', 'g', 'g']

PCAresult = doPCA(madeUpData, n_dim = 3)
plotPCA(PCAresult, madeUpLabels)
