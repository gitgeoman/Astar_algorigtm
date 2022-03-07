# Dijkstra, Astar_algorigtm

The project is on the process of designating crisis areas during a Covid-19 pandemic situatiion for rescue units based
on grouping the locations of people infected with the virus, taking into account:

- classification based the euclidean distance in euclidean space,
- classification based the euclidean distance in road network,
- classification based the terrain and its passability parameters.

### Description of K-mean clustering for each method

k-means clustering is a method of vector quantization, originally from signal processing, that aims to partition n
observations into k clusters in which each observation belongs to the cluster with the nearest mean (cluster centers or
cluster centroid), serving as a prototype of the cluster. This results in a partitioning of the data space into Voronoi
cells. k-means clustering minimizes within-cluster variances (squared Euclidean distances), but not regular Euclidean
distances, which would be the more difficult Weber problem: the mean optimizes squared errors, whereas only the
geometric median minimizes Euclidean distances. For instance, better Euclidean solutions can be found using k-medians
and k-medoids.[wikipedia]

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
![image](https://user-images.githubusercontent.com/45630165/156719155-5f2b781a-da41-4540-a57d-9edf7fdd9bf6.png)
satelite preview
![image](https://user-images.githubusercontent.com/45630165/153831898-61d0604e-36f7-42e8-ba6b-a1f8a878ed18.png)

This is Warsaw - the capital of Poland where new cases of Covid-19 were noticed. Severeal hundreds of people neded help but it
was not neccessary to hospitalise them. Volunteers and rescue teams were divided in this area to provide help.

The pandemic point location (random 500 buildings from AOI):
![image](https://user-images.githubusercontent.com/45630165/156719346-f636e02d-0505-4821-9953-c69927382728.png)

##### Classification based the euclidean distance, euclidean space:

The result of clasification for parameters:
n=500 k=4 i=5 (iterations)
are visible below:

![image](https://user-images.githubusercontent.com/45630165/157050382-aa2448ec-3d0e-4743-aeab-42e447880dea.png)


##### Classification based the euclidean distance in road network

The results of classification were visible below. Each figure presents following steps in iterative cicle of k-mean
clustering with the distances calculated along the road network.


fig road network
![image](https://user-images.githubusercontent.com/45630165/156719617-b4618255-298c-4412-a8f4-75a93ab70e2c.png)

The result of clasification for parameters n=500 k=4 i=5 road network are visible below
<<<<<<< Updated upstream

![image](https://user-images.githubusercontent.com/45630165/153856174-dab4548f-6c28-4746-a386-74ac400897a5.png)
=======
>>>>>>> Stashed changes

![image](https://user-images.githubusercontent.com/45630165/153856174-dab4548f-6c28-4746-a386-74ac400897a5.png)

##### Classification based the terrain and its passability parameters

The results of classification were visible below. Each figure presents following steps in iterative cicle of k-mean
clustering with the distances calculated including selected terrain parameters.

graph network
![image](https://user-images.githubusercontent.com/45630165/156719766-175eeadd-0657-4972-850b-c375a4dda6de.png)

cost of graph lines were estimated based the terrain coverage elements inside square network.


classification result:</br>

iter 1: </br>
![image](https://user-images.githubusercontent.com/45630165/156719832-90d41393-cdf8-437e-9ddf-e033478bc669.png)</br>
iter 2:</br>
![image](https://user-images.githubusercontent.com/45630165/156719850-f61795f7-6bc9-41db-b86d-313dec53f2b3.png)</br>
iter 3:</br>
![image](https://user-images.githubusercontent.com/45630165/156720185-b1cbe98d-999f-4b8d-bbea-3ab491366a08.png)</br>


	class value counter			
![image](https://user-images.githubusercontent.com/45630165/156720370-faba5bfc-80e1-4ad7-aea2-08d69eed8448.png)

