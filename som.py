#
#	Implementation of a Self-Organizing Map
#
#	First version: Hanna Lilja, 2015-04-16
#

import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt

# * Trains a SOM given some data, the data should be represented by a 2d array where each
# 	row is a data instance and each column represents a feature
# * Currently only a square topology implemented
def trainSOM(data, nrows=20, ncols=20, topology='square', alpha=0.5, iterations=100):
	nsamp = np.shape(data)[0]
	nfeat = np.shape(data)[1]
	if (topology == 'square'):
		units = 0.001*np.random.rand(nrows*ncols, nfeat)
		for i in range(iterations):
			inds = np.arange(0, nsamp)
			inds = np.random.permutation(inds)
			for j in range(nsamp):
				jp = inds[j]
				sample = data[jp,:]
				BMUind = getBMUindex(units, sample)
				#Update BMU
				units[BMUind, :] = units[BMUind, :] + alpha*sample
				#Update neighbours when applicable
				if (i < 0.5*iterations):
					neighboursInd = getNeighbours(BMUind, 1, topology, nrows, ncols)
					for neighbour in neighboursInd:
						units[neighbour, :] = units[neighbour, :] + 0.5*alpha*sample
				if (i < 0.05*iterations):
					neighboursInd = getNeighbours(BMUind, 2, topology, nrows, ncols)
					for neighbour in neighboursInd:
						units[neighbour, :] = units[neighbour, :] + 0.1*alpha*sample
		return units
	else:
		errorSting = 'Error: The topology ' + topology + ' is not implemented'
		print errorSting

# * Plots data on a learned SOM given some data
#   The data should be represented by a 2d array where each row is a data instance and each column represents a feature
# * The number of rows and columns needs to be the same as was used to train the SOM
# * Currently only a square topology implemented
def plotDataOnSOM(data, units, labels, nrows=20, ncols=20):
	nsamp = np.shape(data)[0]
	if (nsamp != len(labels)):
		print 'Error: Labels and data do not match'
	else:
		for i in range(nsamp):
			samp = data[i,:]
			BMUind = getBMUindex(units, samp)
			BMUgridInd = lineToGridInd(BMUind, nrows, ncols)
			plt.plot(BMUgridInd[0], BMUgridInd[1], labels[i]+'o')
		plt.axis([-1, ncols, -1, nrows])
		plt.show()

# Simplified neighbour function
def getNeighbours(BMUInd, radius, topology, nrows, ncols):
	if (topology == 'square'):
		gridBMU = lineToGridInd(BMUInd, nrows, ncols)
		neighbours = []
		if (radius == 1):
			if (gridBMU[0] > 0):
				neighbours.append(gridToLineInd([gridBMU[0]-1, gridBMU[1]], nrows, ncols))
			if (gridBMU[0] < nrows-1):
				neighbours.append(gridToLineInd([gridBMU[0]+1, gridBMU[1]], nrows, ncols))
			if (gridBMU[1] > 0):
				neighbours.append(gridToLineInd([gridBMU[0], gridBMU[1]-1], nrows, ncols))
			if (gridBMU[1] < ncols-1):
				neighbours.append(gridToLineInd([gridBMU[0], gridBMU[1]+1], nrows, ncols))
		elif (radius == 2):
			if (gridBMU[0] > 0 and gridBMU[1] > 0):
				neighbours.append(gridToLineInd([gridBMU[0]-1, gridBMU[1]-1], nrows, ncols))
			if (gridBMU[0] < nrows-1 and gridBMU[1] > 0):
				neighbours.append(gridToLineInd([gridBMU[0]+1, gridBMU[1]-1], nrows, ncols))
			if (gridBMU[0] > 0 and gridBMU[1] < ncols-1):
				neighbours.append(gridToLineInd([gridBMU[0]-1, gridBMU[1]+1], nrows, ncols))
			if (gridBMU[0] < nrows-1 and gridBMU[1] < ncols-1):
				neighbours.append(gridToLineInd([gridBMU[0]+1, gridBMU[1]+1], nrows, ncols))
		return neighbours
	else:
		errorSting = 'Error: The topology ' + topology + ' is not implemented'
		print errorSting

# Finds the best matching unit (BMU) given a data instance
def getBMUindex(unitlist, sample):
	minDist = float('inf')
	BMUind = 0
	for k in range(np.shape(unitlist)[0]):
		unit = unitlist[k,:]
		dist = scipy.spatial.distance.euclidean(sample, unit)
		if (dist < minDist):
			minDist = dist
			BMUind = k
	return BMUind

# Converts unit list index to index on a square grid 
def lineToGridInd(lineInd, nrows, ncols):
	theCol = lineInd%ncols
	theRow = (lineInd-theCol)/ncols
	if (theRow >= nrows):
		print 'Error: Invalid line index'
	else:
		gridInd = [theRow, theCol]
		return gridInd

# Converts a index on a square grid to the unit list index
def gridToLineInd(gridInd, nrows, ncols):
	if (gridInd[0] >= nrows or gridInd[1] >= ncols):
		print 'Error: Invalid grid index'
	else:
		return gridInd[0]*ncols + gridInd[1]

madeUpData = np.array([
	[0.2, 0.2, 0.1, 0.1, 0.2, 0.2], [0.3, 0.2, 0.0, 0.1, 0.2, 0.2], [0.3, 0.2, 0.1, 0.0, 0.2, 0.2], [0.2, 0.3, 0.0, 0.1, 0.1, 0.3], [0.2, 0.3, 0.0, 0.0, 0.3, 0.2],
	[0.1, 0.1, 0.1, 0.1, 0.1, 0.5], [0.1, 0.1, 0.1, 0.1, 0.0, 0.6], [0.1, 0.0, 0.1, 0.0, 0.1, 0.7], [0.1, 0.1, 0.1, 0.0, 0.2, 0.5], [0.0, 0.2, 0.0, 0.1, 0.1, 0.6],
	[0.1, 0.1, 0.3, 0.3, 0.1, 0.1], [0.0, 0.1, 0.4, 0.3, 0.1, 0.1], [0.0, 0.0, 0.5, 0.3, 0.1, 0.1], [0.1, 0.0, 0.6, 0.2, 0.1, 0.0], [0.0, 0.1, 0.3, 0.5, 0.1, 0.0],
	[0.3, 0.1, 0.1, 0.1, 0.3, 0.1], [0.2, 0.2, 0.1, 0.1, 0.4, 0.0], [0.4, 0.1, 0.0, 0.1, 0.3, 0.1], [0.3, 0.0, 0.1, 0.1, 0.4, 0.1], [0.4, 0.1, 0.0, 0.1, 0.4, 0.0]])

madeUpLabels = ['y', 'y', 'y', 'y', 'y', 'b', 'b', 'b', 'b', 'b', 'r', 'r', 'r', 'r', 'r', 'g', 'g', 'g', 'g', 'g']

SOMunits = trainSOM(madeUpData)
plotDataOnSOM(madeUpData, SOMunits, madeUpLabels)
