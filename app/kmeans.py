import numpy as np
import random
import sys
class KMeans:
    def __init__(self, k=3, init_method='random', max_iters=100):
        """
        k (int): Number of clusters.
        init_method (str): Method to initialize centroids ('random', 'farthest', 'kmeans++', 'manual').
        """
        self.k = k
        self.init_method = init_method
        self.max_iters = max_iters
        self.centroids = None

    def fit(self, data, initial_centroids=None):
        """
        Parameters:
        data (numpy.ndarray): Data points to cluster.
        initial_centroids (numpy.ndarray): Manually selected initial centroids (if init_method is 'manual').
        """
        self.data = data
        if self.init_method == 'manual' and initial_centroids is not None:
            self.centroids = initial_centroids
        else:
            self.centroids = self.initialize_centroids(data)
        print("centroids",self.centroids)
        for _ in range(self.max_iters):
            clusters = self.assign_clusters(data)
            new_centroids = self.update_centroids(data, clusters)
            
            if np.all(new_centroids == self.centroids):
                break
            
            self.centroids = new_centroids
        
        return self.centroids
    def converge(self, data):
        """
        Parameters:
        data (numpy.ndarray): Data points to cluster.
        initial_centroids (numpy.ndarray): Manually selected initial centroids (if init_method is 'manual').
        """
        self.data = data
        
        print("centroids",self.centroids)
        for _ in range(self.max_iters):
            clusters = self.assign_clusters(data)
            new_centroids = self.update_centroids(data, clusters)
            
            if np.all(new_centroids == self.centroids):
                break
            
            self.centroids = new_centroids
        
        return self.centroids,clusters
    def app_initialize_centroids(self, data,initial_centroids=None):
        self.data = data
        if self.init_method == 'manual' and initial_centroids is not None:
            self.centroids = initial_centroids
        else:
            self.centroids = self.initialize_centroids(data)
        return self.centroids
    def initialize_centroids(self, data):
        """
        Initializes centroids based on the specified method.

        Parameters:
        data (numpy.ndarray): Data points to cluster.

        Returns:
        numpy.ndarray: Initialized centroids.
        """
        if self.init_method == 'random':
            return self.random_initialization(data)
        elif self.init_method == 'farthest':
            return self.farthest_first_initialization(data)
        elif self.init_method == 'kmeans++':
            return self.kmeans_plus_plus_initialization(data)
        
    def random_initialization(self, data):
        """Randomly selects k data points as initial centroids."""
        indices = np.random.choice(data.shape[0], self.k, replace=False)
        return data[indices]

    def farthest_first_initialization(self, data):
        """Selects initial centroids that are farthest apart."""
        centroids = [data[np.random.randint(data.shape[0])]]
        for _ in range(1, self.k):
            distances = np.array([min([np.linalg.norm(x - c) for c in centroids]) for x in data])
            next_centroid = data[np.argmax(distances)]
            centroids.append(next_centroid)
        return np.array(centroids)

    def kmeans_plus_plus_initialization(self, data):
        """Initializes centroids using the KMeans++ algorithm."""
        centroids = [data[np.random.randint(data.shape[0])]]
        for _ in range(1, self.k):
            distances = np.array([min([np.linalg.norm(x - c) for c in centroids]) for x in data])
            probabilities = distances / distances.sum()
            cumulative_probabilities = np.cumsum(probabilities)
            r = random.random()
            for j, p in enumerate(cumulative_probabilities):
                if r < p:
                    centroids.append(data[j])
                    break
        return np.array(centroids)

    def assign_clusters(self, data):
        """
        Assigns each data point to the nearest centroid.

        Parameters:
        data (numpy.ndarray): Data points to cluster.

        Returns:
        list: Cluster assignments for each data point.
        """
        print("assign")
        print(f"Shape of data: {np.shape(data) if isinstance(data, np.ndarray) else 'Not a numpy array'}")
        clusters = []
        for point in data:
            distances = [np.linalg.norm(point - centroid) for centroid in self.centroids]
            cluster = np.argmin(distances)
            clusters.append(cluster)
        return clusters

    def update_centroids(self, data, clusters):
        """
        Updates the centroids as the mean of the assigned data points.

        Parameters:
        data (numpy.ndarray): Data points to cluster.
        clusters (list): Current cluster assignments.

        Returns:
        numpy.ndarray: Updated centroids.
        """
        print("update")
        print(f"Shape of data: {np.shape(data) if isinstance(data, np.ndarray) else 'Not a numpy array'}")
        sys.stdout.flush()
        new_centroids = []
        for i in range(self.k):
            points_in_cluster = [data[j] for j in range(len(data)) if clusters[j] == i]
            if points_in_cluster:
                new_centroids.append(np.mean(points_in_cluster, axis=0))
            else:
                new_centroids.append(self.centroids[i])  # Keep the old centroid if no points in cluster
        return np.array(new_centroids)

    def predict(self, data):
        """
        Predicts the nearest cluster for new data points.

        Parameters:
        data (numpy.ndarray): New data points.

        Returns:
        list: Predicted cluster assignments.
        """
        return self.assign_clusters(data)

    def get_centroids(self):
        """
        Returns the current centroids.

        Returns:
        numpy.ndarray: Current centroids.
        """
        return self.centroids

# Example usage
if __name__ == '__main__':
    # Create some sample data
    np.random.seed(42)
    data = np.vstack((np.random.randn(50, 2) * 0.75 + np.array([1, 0]),
                      np.random.randn(50, 2) * 0.25 + np.array([-1, -1]),
                      np.random.randn(50, 2) * 0.5 + np.array([2, 2])))

    # Initialize and fit the KMeans model
    kmeans = KMeans(k=3, init_method='farthest')
    centroids = kmeans.fit(data)

    # Output the final centroids
    print("Final centroids:\n", centroids)
