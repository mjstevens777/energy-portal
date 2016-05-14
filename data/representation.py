import pandas as pd
import numpy as np
from copy import deepcopy

class HistogramData(object):
    """Represent data as a histogram consisting of many pandas.series."""
    def __init__(self, labels, edges, data, m):
        """Initialize the data.

        Parameters
        ----------
        labels: length k list of string labels
        edges: length k list of
                   length n_i list of pandas.Series or number
        data: n_1 x n_2 x n_3... nested lists of pandas.Series or number
        n: integer, number of d ata points
        """
        self.labels = labels
        self.edges = edges
        self.data = data
        self.m = m
        self.k = len(self.labels)
        if self.k != len(self.edges):
            raise Exception('Number of edge lists does not match number of labels')
        self.dims = [(len(e) - 1) for e in self.edges]
        d = self.data
        for i, dim in enumerate(self.dims):
            if len(d) != dim:
                raise Exception("Bad dimensions at level %d (%d,%d)" % (i, len(d), dim))
            d = d[0]

    def normalizeCountsToPdf(self):
        for idx in self.generateIndices():
            binsize = 1
            for k in range(self.k):
                l, r = self.edges[k][idx[k]:idx[k]+2]
                binsize *= (r - l)
            d = self.data
            for k in range(self.k - 1):
                d = d[idx[k]]
            lastIdx = idx[self.k - 1]
            d[lastIdx] = d[lastIdx] / binsize

    def each(self):
        """A generator for creating a single histogram for each row."""
        for i in range(self.n):
            edges = [
                [e[i] if isinstance(e, pd.Series) else e
                    for e in labelEdges]
                for labelEdges in self.edges]
            data = [
                [d[i] if isinstance(d, pd.Series) else d
                    for d in labelData]
                for labelData in self.data]
            yield HistogramData(self.labels, edges, data, 1)

    def generateIndices(self):
        """A generator for tuples representing indices."""
        size = 1
        for dim in self.dims:
            size *= dim
        for i in range(size):
            idx = ()
            j = i
            for ni in reversed(self.dims):
                idx = (j % ni,) + idx
                j = int(j / ni)
            yield idx

    def flatten(self):
        """A generator for tuples of (edges, data)."""
        for idx in self.generateIndices():
            yield (self.getEdges(idx), self.getData(idx))


    @staticmethod
    def intervalOverlap(e1, e2):
        """Amount of overlap between two bins."""
        l1, r1 = e1
        l2, r2 = e2
        l = np.maximum(l1, l2)
        r = np.minimum(r1, r2)
        overlap = (r - l) * (r > l)
        return overlap

    def getData(self, idx):
        d = self.data
        for k in range(self.k):
            d = d[idx[k]]
        return d

    def getEdges(self, idx):
        e = ()
        for k in range(self.k):
            e = e + (tuple(self.edges[k][idx[k]:idx[k]+2]),)
        return e

    def setData(self, idx, val):
        d = self.data
        for k in range(self.k - 1):
            d = d[idx[k]]
        d[idx[self.k - 1]] = val
        if self.getData(idx) != val:
            raise Exception("Set failed")

    def collapseToLabels(self, newLabels):
        newToOld = [self.labels.index(l) for l in newLabels]
        newDims = [self.dims[old] for old in newToOld]
        newEdges = [self.edges[old] for old in newToOld]
        newK = len(newLabels)

        arr = 0.0
        for dim in reversed(newDims):
            arr = [deepcopy(arr) for i in range(dim)]

        newHist = HistogramData(newLabels, newEdges, arr, self.m)

        for newIdx in newHist.generateIndices():
            oldIndices = []
            for oldIdx in self.generateIndices():
                badIdx = False
                for k in range(newK):
                    oldK = newToOld[k]
                    if oldIdx[oldK] != newIdx[k]:
                        badIdx = True
                        break
                if badIdx:
                    continue
                oldIndices.append(oldIdx)
            data = 0.0
            for oldIdx in oldIndices:
                data += self.getData(oldIdx)
            newHist.setData(newIdx, data)
        return newHist

    def convolution(self, other):
        commonLabels = list(set(self.labels) & set(other.labels))
        nLabels = len(commonLabels)
        if nLabels == 0:
            raise Exception("Data of %r and %r is incomparable" % (self.labels, other.labels))
        selfView = self.collapseToLabels(commonLabels)
        otherView = other.collapseToLabels(commonLabels)
        output = 0.0
        for edgesSelf, dataSelf in selfView.flatten():
            for edgesOther, dataOther in otherView.flatten():
                overlap = 1
                for k in range(nLabels):
                    overlap = overlap * self.intervalOverlap(
                        edgesSelf[k], edgesOther[k])
                if np.all(overlap == 0):
                    continue
                output = output + overlap * dataSelf * dataOther
        return output


class NdHistogram(object):
    """Represent a histogram across multiple dimensions.

    Since this is the most generic
    Let k be the number of dimensions and n_i be the number of
    bins in dimension i.
    """

    def __init__(self, labels, edges, names):
        """Initialize the histogram for a row of data.

        Parameters
        ----------
        labels: length-k list of string
        edges: length-k list of
                 length (n_i + 1) list of bin edges
            bin edges can be either a number or a pandas.Series
        names: length-k list of
                 length n_i list of bin count column names
        """
        self.labels = labels
        self.edges = edges
        self.names = names
        return

    def normalize(self):
        """Return an NdHistogram."""
        return self

class HistogramBase(object):
    """This class is a base class for all other data reprentations."""
    def convolution(self, other, data):
        """The probability that the two distributions are equal.

        Parameters
        ----------
        other: HistogramBase

        data: pandas.Series
        """
        pass

class Histogram(HistogramBase):
    def __init__(self, label, edges, names):
        self.label = label
        self.edges = edges
        self.names = names

class SingleValue(NdHistogram):
    eps = 0.01

    def __init__(self, label, name):
        self.labels = label
        self.name = name
