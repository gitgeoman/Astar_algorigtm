# Loading the required modules

import numpy as np
from scipy.spatial.distance import cdist


# Defining our function
def kmeans(x, k, no_of_iterations):
    idx = np.random.choice(len(x), k, replace=False)
    # Randomly choosing Centroids
    centroids = x[idx, :]  # Step 1 #to jest tablica z centroidami [[x,y],[x,y]]
    print(x)
    # finding the distance between centroids and all the data points
    distances = cdist(x, centroids, 'euclidean')  # Step 2 tu jest generator
    # print(distances)
    # który oblicza odległości od wszystkich centroidów do wszystkich punktów
    # print(distances[0])

    # Centroid with the minimum Distance
    points = np.array([np.argmin(i) for i in distances])  # Step 3

    # Repeating the above steps for a defined number of iterations
    # Step 4
    for _ in range(no_of_iterations):
        centroids = []
        for idx in range(k):
            temp_cent = x[points == idx].mean(axis=0)
            centroids.append(temp_cent)

        centroids = np.vstack(centroids)  # Updated Centroids

        distances = cdist(x, centroids, 'euclidean')
        points = np.array([np.argmin(i) for i in distances])

    return points
