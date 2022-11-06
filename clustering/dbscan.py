import numpy as np
import pandas as pd
from queue import Queue
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import seaborn as sns

#source: https://www.mikioharman.com/2020-08-24-dbscan/
#made some refactoring

class dbscan():
    def __init__(self, ar, epsilon=1, min_points=5):
        self.ar = np.array(ar)
        # needed to get label col index
        self.n_features = self.ar.shape[1]
        self.epsilon = epsilon
        self.min_points = min_points
        self.cluster_label = 0
        self.noise = -1
        self.init_value = -100

    def fit(self):
        # Create labels column initialized to -1 (unclassified)
        self.ar = np.append(self.ar, np.array([[self.init_value] * self.ar.shape[0]]).reshape(-1, 1), axis=1)
        for x in range(len(self.ar)):
            # if the point is not labelled already then search for neighbors
            if self.ar[x, self.n_features] != self.init_value:
                continue
            # find neighbors
            neighbors = self.get_neigbours(x)
            # If less neighbors than min_points then label as noise and continue
            if len(neighbors) < self.min_points:
                self.ar[x, self.n_features] = self.noise
                continue
                # increment cluster label
            self.cluster_label += 1
            # set current row to new cluster label
            self.ar[x, self.n_features] = self.cluster_label
            # create seed set to hold all neighbors of cluster including the neighbors already found
            found_neighbors = neighbors
            # create Queue to fold all neighbors of cluster
            q = Queue()
            # add original neighbors
            for x in neighbors:
                q.put(x)
                # While isnt empty label new neighbors to cluster
            while not q.empty():
                current = q.get()
                # if cur_row labled noise then change to cluster label (border point)
                if self.ar[current, self.n_features] == self.noise:
                    self.ar[current, self.n_features] = self.cluster_label
                # If label is not -1(unclassified) then continue
                if self.ar[current, self.n_features] != self.init_value:
                    continue
                    # label the neighbor
                self.ar[current, self.n_features] = self.cluster_label
                # look for neightbors of cur_row
                neighbors2 = self.get_neigbours(current)
                # if neighbors2 >= min_points then add those neighbors to seed_set
                if len(neighbors2) >= self.min_points:
                    for x in neighbors2:
                        if x not in found_neighbors:
                            q.put(x)
                            found_neighbors.append(x)

    def predict(self, x):
        "Return the predicted labels of array of features"
        preds = []
        for point in x:
            neighbors = self.get_neigbours(point, input_ar=True)
            label = self.ar[neighbors[0], self.n_features]
            preds.append(label)
        return preds

    def get_neigbours(self, x, input_ar=False):
        vec = x if input_ar else self.ar[x, :self.n_features]
        dist = np.sqrt(((vec - self.ar[:, :self.n_features]) ** 2).sum(1))
        neighbors = np.argwhere(dist <= self.epsilon).reshape(-1)
        return neighbors.tolist()


# generate data
centers = [(0, 4), (5, 5), (8, 2)]
cluster_std = [1.2, 1, 1.1]

X, y = make_blobs(n_samples=200, cluster_std=cluster_std, centers=centers, n_features=2, random_state=1)

# fit model
scanner = dbscan(ar=X, epsilon=0.7, min_points=3)

scanner.fit()

sns.scatterplot(data=pd.DataFrame(scanner.ar), x=0, y=1, hue=2, palette="deep")
plt.show()
