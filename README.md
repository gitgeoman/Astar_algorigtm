# Dijkstra, Astar_algorigtm

The project is on the process of designating crisis areas during a Covid-19 pandemic situatiion for rescue units based on grouping the locations of people infected with the virus, taking into account:

- classification based the euclidean distance in euclidean space,
- classification based the euclidean distance in road network,
- classification based the terrain and its passability parameters.

### Description of K-mean clustering for each method

k-means clustering is a method of vector quantization, originally from signal processing, that aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean (cluster centers or cluster centroid), serving as a prototype of the cluster. This results in a partitioning of the data space into Voronoi cells. k-means clustering minimizes within-cluster variances (squared Euclidean distances), but not regular Euclidean distances, which would be the more difficult Weber problem: the mean optimizes squared errors, whereas only the geometric median minimizes Euclidean distances. For instance, better Euclidean solutions can be found using k-medians and k-medoids.[wikipedia]


Visual explanation of k-mean clustering:
<img src="https://upload.wikimedia.org/wikipedia/commons/e/ea/K-means_convergence.gif" alt="My Project GIF" width="300" height="300">

#### General basis of K-mean clustering

#### Classification based the euclidean distance in euclidean space:

The calculation of distance is based the schema in graph below:

![image](https://user-images.githubusercontent.com/45630165/153833054-0c2d4470-9c35-4f3a-99f3-bdb0a999a88a.png)

#### Classification based the euclidean distance in road network

The calculation is based the euclidean distance between the nodes of road network as visible in the graph below:

![image](https://user-images.githubusercontent.com/45630165/153853080-f2992276-493a-465b-9c2c-d298299056ea.png)

#### Classification based the terrain and its passability parameters

### Calculation results for case study

#### Testing datased, area of interest

The area of interest:
![image](https://user-images.githubusercontent.com/45630165/153831898-61d0604e-36f7-42e8-ba6b-a1f8a878ed18.png)

This is part of Warsaw Poland where new cases of Covid-19 were noticed. Severeal hundreds of people neded help but it was not neccessary to hospitalise them. Volunteers and rescue teams were divided in this area to provide help.

On this area data were collected from OSM.

##### Classification based the euclidean distance, euclidean space:

The result of clasification for parameters:
n=4000
k=4
i=5 (iterations)
are visible below:
![image](https://user-images.githubusercontent.com/45630165/153856174-dab4548f-6c28-4746-a386-74ac400897a5.png)

##### Classification based the euclidean distance in road network

The results of classification were visible below. Each figure presents following steps in iterative cicle of k-mean clustering with the distances calculated along the road network.

The result of clasification for parameters
n=4000
k=4
i=5
are visible below
![image](https://user-images.githubusercontent.com/45630165/153856381-9089c253-c601-404b-9594-c8a7744b4a06.png)


##### Classification based the terrain and its passability parameters
