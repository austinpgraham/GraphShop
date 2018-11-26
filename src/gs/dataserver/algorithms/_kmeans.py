#!/usr/bin/env python3
import math
import random


class KMeans():
    """
    Implementation of the KMeans algorithm
    """
    
    def __init__(self, data, k):
        # Save attributes
        self._k = k
        self._data = data
        self._ncols = len(list(data.columns))
        # Generate list of centers and randomly assign clusters
        self._centers = [[0 for _ in range(self._ncols)] for _ in range(self._k)]
        self._clabels = [random.randint(0, k) for i in range(len(data))]
        # Intialize error metrics
        self._cluster_sse = []
        self._total_sse = 0
        # Calculate initial centers
        self._calc_centers()
        # Begin clustering
        self._cluster()
    
    def _euclid(self, point1, point2):
        """
        Euclidean distance
        """
        dim = len(point1)
        # Be sure points have the same dimensions
        if dim != len(point2):
            raise ValueError("Lengths must match.")
        inter = sum([(point1[i] - point2[i])**2 for i in range(dim)])
        return math.sqrt(inter)

    def _calc_centers(self):
        """
        Calculate centers for each cluster
        """
        for i in range(self._k):
            # Get points in cluster
            rel_data = self._data.iloc[[idx for idx, j in enumerate(self._clabels) if j == i]]
            rel_data = rel_data.values
            # Initalize aggregate new center
            new_center = [0 for _ in range(self._ncols)]
            # Add all dimensions of each point to new center
            for v in rel_data:
                for idx, e in enumerate(v):
                    new_center[idx] += e
            # Divide for average
            new_center = [v / len(rel_data) for v in new_center]
            # Re-assign new center
            self._centers[i] = new_center

    def _cluster(self):
        """
        Perform KMeans clustering
        """
        has_changed = True
        while has_changed:
            # Assume nothing will change
            has_changed = False
            #  Iterate through all points
            for i in self._data.index:
                # Find the closest center
                curr_label = self._clabels[i]
                distances = [self._euclid(self._data.iloc[i].tolist(), self._centers[j]) for j in range(self._k)]
                new_cluster = distances.index(min(distances))
                # If not the same, re-assign the cluster
                if new_cluster != curr_label:
                    # SAFEGAURD - A CLUSTER MUST CONTAIN AT LEAST ONE POINT
                    if len([x for x in self._clabels if x == self._clabels[i]]) > 1:
                        self._clabels[i] = new_cluster
                        # Mark that a change has been made
                        has_changed = True
            # Re-calculate centers
            self._calc_centers()
        
        # Calculate SSE for each cluster
        for i in range(self._k):
            rel_data = self._data.iloc[[idx for idx, j in enumerate(self._clabels) if j == i]]
            rel_data = rel_data.values
            sse = sum([self._euclid(v, self._centers[i])**2 for v in rel_data])
            self._cluster_sse.append(sse)
        
        # Calculate total SSE
        self._total_sse = sum(self._cluster_sse)
    
    def __str__(self):
        """
        Print designated metrics
        """
        _out = ""
        _out += "Total SSE: {}\n".format(round(self._total_sse, 3))
        for i in range(self._k):
            _out += "Cluster {}:\n".format(i)
            _out += "\tMembers: {}\n".format(str([idx for idx, j in enumerate(self._clabels) if j == i]))
            _out += "\tMean: {}\n".format(str([round(j, 3) for j in self._centers[i]]))
            _out += "\tSSE: {}\n".format(round(self._cluster_sse[i], 3))
        return _out
