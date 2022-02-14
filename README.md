# Astar_algorigtm
 
The project is on the process of designating crisis areas during a Covid-19 pandemic situatiion for rescue units based on grouping the locations of people infected with the virus, taking into account the terrain and its passability.

The area of interest:
![image](https://user-images.githubusercontent.com/45630165/153831898-61d0604e-36f7-42e8-ba6b-a1f8a878ed18.png)

This is part of Warsaw Poland where new cases of Covid-19 were noticed. Severeal hundreds of people neded help but it was not neccessary to  hospitalise them. Volunteers and rescue teams were divided in this area to provide help.

On this area data were collected from OSM. 

To show the application of algorithm the number or new cases were set as 200, number or rescue teams available in the area of interst is four.
n=200 - new cases in area,
k= 4, number of categories  (corresponding to the number of rescue teams). 



The results of classification were visible below. Each figure presents following steps in iterative cicle of k-mean clustering with the distances calculated along the road network.  
The concept of dijkstra algorithm based on euclidean distance. https://upload.wikimedia.org/wikipedia/commons/e/e4/DijkstraDemo.gif

The result of clasification for parameters:
n=200
k=4
i=5 (iterations)
are visible below:
![image](https://user-images.githubusercontent.com/45630165/153832230-63cdd1a9-7b07-45a2-8965-99dee3aceebb.png)


To comparis the results above classification were calculated with the euclidean distances calculated in euclidean space. (
![image](https://user-images.githubusercontent.com/45630165/153833054-0c2d4470-9c35-4f3a-99f3-bdb0a999a88a.png)
The result of clasification for parameters
n=200
k=4
i=5
are visible below
#tutaj link
