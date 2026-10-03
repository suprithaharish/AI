import numpy as np


def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))


class KMeans:

    def __init__(self, k=2, max_iters=100):
        self.k = k
        self.max_iters = max_iters

    def fit(self, X):

        # Pick random initial centroids
        idx = np.random.choice(
            X.shape[0],
            self.k,
            replace=False
        )

        self.centroids = X[idx]

        for _ in range(self.max_iters):

            # Assign clusters
            self.labels = np.array([
                np.argmin([
                    euclidean_distance(x, c)
                    for c in self.centroids
                ])
                for x in X
            ])

            # Recompute centroids
            new_centroids = np.array([
                X[self.labels == i].mean(axis=0)
                if len(X[self.labels == i]) > 0
                else self.centroids[i]
                for i in range(self.k)
            ])

            # Check convergence
            if np.all(self.centroids == new_centroids):
                break

            self.centroids = new_centroids

        return self.labels


def silhouette_score_simple(X, labels):

    scores = []

    for i, x in enumerate(X):

        c_idx = labels[i]

        same_cluster = X[labels == c_idx]
        other_cluster = X[labels != c_idx]

        # Calculate average distance within same cluster
        if len(same_cluster) > 1:

            distances = [
                euclidean_distance(x, original)
                for original in same_cluster
                if not np.array_equal(x, original)
            ]

            a = np.mean(distances)

        else:
            a = 0

        # Calculate distance to other cluster
        if len(other_cluster) > 0:

            cluster_distances = []

            for c in set(labels):

                if c != c_idx:

                    cluster_points = X[labels == c]

                    mean_distance = np.mean([
                        euclidean_distance(x, o)
                        for o in cluster_points
                    ])

                    cluster_distances.append(mean_distance)

            b = np.min(cluster_distances)

        else:
            b = 0

        # Calculate silhouette value
        if max(a, b) == 0:
            scores.append(0)
        else:
            scores.append((b - a) / max(a, b))

    return np.mean(scores)


# Example Usage
if __name__ == "__main__":

    X = np.array([
        [1, 2],
        [1, 4],
        [1, 0],
        [10, 2],
        [10, 4],
        [10, 0]
    ])

    # Create K-Means model
    km = KMeans(k=2)

    # Train the model
    labels = km.fit(X)

    # Calculate silhouette score
    score = silhouette_score_simple(X, labels)

    print("Assigned Labels:", labels)

    print(
        "Calculated Silhouette Validation Score:",
        score
    )