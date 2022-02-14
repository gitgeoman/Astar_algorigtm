import psycopg2
from funkcje_do_bazy_danych import *
from conn_data import user, password, host, port, database
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()

    # ile punktów
    n = 4000

    # wybieram losowo 100 punktow z bazy danych (węzły) zapisuje ich indeksy jako liste do zmiennej x
    cursor.execute(
        f'SELECT id,the_geom AS geom, ST_AsText(the_geom) AS geomDD FROM public."lineEdges_noded_vertices_pgr" ORDER BY random() limit {n}')
    dane = cursor.fetchall()
    print('\n sórówka z bazy danych \n', dane)

    # rozpakowuje dane
    x = [item[0] for item in dane]  # indeksy punktów
    coords = [(item[1]) for item in dane]  # współrzedne punktów
    coordsDD = [(item[2]) for item in dane]  # współrzedne punktów
    coordsDX = [[float(item[7:-1].split()[0]), float(item[7:-1].split()[1])] for item in coordsDD]
    coordsY = [float(item[6:-1].split()[0]) for item in coordsDD]
    coordsX = [float(item[7:-1].split()[1]) for item in coordsDD]
    print('Lista współrzędnych', coordsX, '\n', coordsY)

    print('\nIndeksy punktów w obliczeniach x: \n', x, 'wspolrzedne punktów w obliczeniach coords:\n', coords, '\n',
          coordsDD)

    # wybieram losowo k punktów na centroidy do pierwszej iteracji (oznacza to że będzie k grup)
    k = 5
    centroids = np.random.choice(len(x), k, replace=False)  # indeksy centroidów
    centroidsID = [x[item] for item in centroids]  # id centroidow
    print('\nIndeksy obiektów wybranych jako centroidy do pierwszej iteracji: \n', centroidsID)


    def my_func(centroid, item):
        cursor.execute(query_tekst(centroid, item))
        return sum_length_from_scratch(cursor.fetchall())


    distances = ([[my_func(centroid, item) for centroid in centroidsID] for item in x])
    print('\nOdległości po do każdego z centroidów z każdego z punktów: \n', distances)

    points = np.array([np.argmin(i) for i in distances])  # wybieram do którego centroidu jest najblizej do punktu

    print('\nWynik klasyfikacji: \n', points)

    # obliczam gdzie jest środek każdej z klas
    # wywołuję indeksy każdej klasy i ich współrzędne

    zipped = list(zip(x, coords, coordsY, coordsX, distances, points, ))
    df = pd.DataFrame(zipped, columns=['db_index', 'coords', 'coordsY', 'coordsX', 'distances', 'klasyfikacja'])
    print('\n', df.to_string())
    # print('\n count of values \n',df.groupby('klasyfikacja').count())

    # obliczam współrzędne dla nowych centroidów
    df1 = pd.DataFrame([df.groupby('klasyfikacja')['coordsX'].mean(), df.groupby('klasyfikacja')['coordsY'].mean()]).T
    print('\n średnie współrzędne nowych centroidów \n\n', df1.to_string())

    plt.plot(figsize=(10, 10))

    no_of_iterations = 4
    list_of_dfs = [df, ]

    for _ in range(no_of_iterations):
        centroidsID = []
        # SNAPOWANIE DO Węzła
        for index, coordX, coordY in zip(df1.index, df1.coordsX, df1.coordsY):
            # print (index, coordX, coordY)

            cursor.execute(
                f'SELECT v.id, v.the_geom FROM public."lineEdges_noded_vertices_pgr" AS v, public."lineEdges_noded" AS e '
                f'WHERE v.id = (SELECT id FROM public."lineEdges_noded_vertices_pgr" '
                f'ORDER BY the_geom <-> ST_SetSRID(ST_MakePoint({coordY}, {coordX}), 4326) LIMIT 1 '
                f') '
                f'AND (e.source=v.id OR e.target=v.id) GROUP BY v.id, v.the_geom')
            nearese = cursor.fetchall()
            centroidsID.append(nearese[0][0])
        print('\n Indeksy obiektów wybranych jako centroidy w iteracji \n ',
              centroidsID)

        distances = ([[my_func(centroid, item) for centroid in centroidsID] for item in x])
        points = np.array([np.argmin(i) for i in distances])  # wybieram do którego centroidu jest najblizej do punktu
        zipped = list(zip(x, coords, coordsY, coordsX, distances, points, ))
        df = pd.DataFrame(zipped, columns=['db_index', 'coords', 'coordsY', 'coordsX', 'distances', 'klasyfikacja'])
        # print('\n df wynikowy dla bierzacej iteracji \n', df.to_string())
        list_of_dfs.append(df)

    # przegląd danych
    print(' TU WYŚWIETLAM KOMPLET WYNIKÓW W POSTACI DF>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>. \n', )

    for one_df in list_of_dfs:
        print('\n df wynikowy \n', one_df.to_string())

    plt.subplots(3, 2, figsize=(10, 14))
    for numer in range(len(list_of_dfs)):
        print('!!!!!!!!!!!!!!!!!!!', numer + 1)
        df_tmp = list_of_dfs[numer]
        groups = df_tmp.groupby('klasyfikacja')
        plt.subplot(3, 2, numer + 1)
        for name, group in groups:
            plt.plot(group.coordsY, group.coordsX, marker='o', linestyle='', markersize=3, label=name)
            # do zrobienia centroidy w każdej iteracji

        plt.title(numer)
    # plt.legend()
    plt.show()


except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia.
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
