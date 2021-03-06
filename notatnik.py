# nawiąż połączenie
import psycopg2
from DB_connection_functions import *
from DB_connection_parameters import user, password, host, port, database

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()
    #########################################################################
    # pobieram dane do pierwszej iteracji:
    #########################################################################

    # ile punktow
    n = 5
    cursor.execute(
        f'SELECT id,the_geom AS geom, ST_AsText(the_geom) AS geomDD FROM public."drogi_aoi_noded_vertices_pgr_fit" ORDER BY random() limit {n}'
    )
    dane = cursor.fetchall()
    print('\n surówka z bazy danych \n', dane)

    # rozpakowuje dane
    x = [item[0] for item in dane]  # indeksy punktów
    coords = [(item[1]) for item in dane]  # współrzedne punktów
    coordsDD = [(item[2]) for item in dane]  # współrzedne punktów
    coordsDX = [[float(item[11:-1].split()[0]), float(item[7:-1].split()[1])] for item in coordsDD]
    coordsY = [float(item[11:-1].split()[0]) for item in coordsDD]  # dlugos_geograficzna
    coordsX = [float(item[11:-1].split()[1]) for item in coordsDD]  # szerokosc geograficzna
    print('Lista współrzędnych \n !!!!!!!!!!!!!!! \n', coordsX, '\n', coordsY)
    print('\nIndeksy punktów w obliczeniach x: \n', x, 'wspolrzedne punktów w obliczeniach coords:\n', coords, '\n',
          coordsDD)
    X_zipped = list(zip(x, coords, coordsY, coordsX, coordsDD, ))
    df = pd.DataFrame(X_zipped, columns=['indeks', 'coords', 'coordsY', 'coordsX', 'coordsDD', ])
    print('>>>>>>>>>>>>>to są dane \n ', df.to_string())

    # #########################################################################
    # # SNAPOWANIE wszystkich punktow do najblizszego punktu z warstwy grafu
    # #######################################################################

    dane_snapowane = []
    for index, coordX, coordY in zip(df.index, df.coordsX, df.coordsY):
        cursor.execute(
            f'SELECT v.id, ST_AsText(v.the_geom) FROM public."graf_aoi_noded_vertices_pgr" AS v, public."graf_aoi_noded" AS e '
            f'WHERE v.id = (SELECT id FROM public."graf_aoi_noded_vertices_pgr" '
            f'ORDER BY the_geom <-> ST_SetSRID(ST_MakePoint({coordY}, {coordX}), 4326) LIMIT 1) '
            f'AND(e.source = v.id OR e.target = v.id) GROUP BY v.id, v.the_geom'
        )
        dane_snapowane.append(cursor.fetchall()[0])

    x_snapowane = [item[0] for item in dane_snapowane]  # indeksy punktów
    coords_snapowane = [(item[1]) for item in dane_snapowane]  # współrzedne punktów wyjmuje tekst
    coords_snapowane = [[float(item[6:-1].split()[0]), float(item[7:-1].split()[1])] for item in coords_snapowane]
    # print('to są dane snapowane \n', coords_snapowane)
    coordsY_snapowane = [item[0] for item in coords_snapowane]  # dlugos_geograficzna
    coordsX_snapowane = [item[1] for item in coords_snapowane]  # szerokosc geograficzna

    X_zipped_snapowane = list(zip(x_snapowane, coords_snapowane, coordsY_snapowane, coordsX_snapowane))
    df = pd.DataFrame(X_zipped_snapowane, columns=['indeks', 'coords', 'coordsY', 'coordsX', ])
    print('>>>>>>>>>>>>>to są dane _snapowane \n ', df.to_string())

    #########################################################################
    # PRZECHODZĘ DO PIERWSZEGO KLASTROWANIA
    #########################################################################

    # wybieram losowo k punktów na centroidy do pierwszej iteracji (oznacza to że będzie k grup)
    k = 2
    centroids = np.random.choice(len(x), k, replace=False)  # wybieram losowo indeksy centroidów
    centroidsID = [x[item] for item in centroids]  # na podstawie indeksów wywołuje id z którego będę liczył odległość
    
    print('\nIndeksy obiektów wybranych jako centroidy z węzłów drogowych: \n', centroidsID)


    def query_tekst(source, target):
        postgreSQL_select_Query = \
            f'SELECT * FROM pgr_dijkstra(\'SELECT id, source, target, cost as cost ' \
            f'FROM public."graf_aoi"\', {source}, {target}, false)'

        # print(postgreSQL_select_Query)
        return postgreSQL_select_Query


    def sum_length_from_scratch(tablica):
        print(tablica)
        dlugosc_drogi = 0
        for row in tablica:
            dlugosc_drogi = dlugosc_drogi + float(row[4])
        return dlugosc_drogi


    def my_func(centroid, item):
        print(centroid, item)
        cursor.execute(query_tekst(centroid, item))
        print(cursor.fetchall())
        return sum_length_from_scratch(cursor.fetchall())


    distances = ([[my_func(centroid, item) for centroid in centroidsID] for item in x])
    print('\nOdległości po do każdego z centroidów z każdego z punktów: \n', distances)

    points = np.array([np.argmin(i) for i in distances])
    print('\nWynik klasyfikacji: \n', points)


except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia.
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
