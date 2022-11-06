import torch
import numpy as np
import pandas as pd
from queue import Queue
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import seaborn as sns


class dbscan_t():
    def __init__(self, t, epsilon=1, min_points=5):
        self.t = t
        # needed to get label col index
        self.n_features = self.t.shape[1]
        self.epsilon = epsilon
        self.min_points = min_points
        self.cluster_label = 0
        self.noise = -1
        self.init_value = -100
        self.t_clusters = torch.full((self.t.size()[0],), self.init_value)

    def fit(self):
        # Create labels column initialized to -1 (unclassified)
        for x in range(self.t.size()[0]):
            # if the point is not labelled already then search for neighbors
            if self.t_clusters[x] != self.init_value:
                continue
            # find neighbors
            neighbors = self.get_neigbours(x)
            # If less neighbors than min_points then label as noise and continue
            if len(neighbors) < self.min_points:
                self.t_clusters[x] = self.noise
                continue
                # increment cluster label
            self.cluster_label += 1
            # set current row to new cluster label
            self.t_clusters[x] = self.cluster_label
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
                if self.t_clusters[current] == self.noise:
                    self.t_clusters[current] = self.cluster_label
                # If label is not -1(unclassified) then continue
                if self.t_clusters[current] != self.init_value:
                    continue
                    # label the neighbor
                self.t_clusters[current] = self.cluster_label
                # look for neighbours of cur_row
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
            neighbors = self.get_neigbours(point, input_t=True)
            label = self.t_clusters[neighbors[0]]
            preds.append(label)
        return preds

    def get_neigbours(self, x, input_t=False):
        vec = x if input_t else self.t[x]
        dist = ((vec - self.t) ** 2).sum(1).sqrt()
        neighbors = torch.where(dist < self.epsilon)[0].tolist()
        return neighbors


# generate data
centers = [(0, 4), (5, 5), (8, 2)]
cluster_std = [1.2, 1, 1.1]
X, y = make_blobs(n_samples=200, cluster_std=cluster_std, centers=centers, n_features=2, random_state=1)

# fit model
scanner = dbscan_t(t=torch.tensor(X), epsilon=0.7, min_points=3)

scanner.fit()

df=pd.DataFrame(X)
df['cluster']=scanner.t_clusters
sns.scatterplot(data=df, x=0, y=1, hue='cluster', palette="deep")
plt.show()
