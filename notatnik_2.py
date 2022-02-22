# nawiąż połączenie
import psycopg2
from DB_connection_functions import *
from DB_connection_parameters import user, password, host, port, database2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database2)
    cursor = connection.cursor()
    #########################################################################
    # pobieram dane do pierwszej iteracji:
    #########################################################################

    # ile punktow
    n = 2
    cursor.execute(
        f'SELECT id, the_geom AS geom, ST_AsText(the_geom) AS geomDD FROM public."drogi_aoi_noded_vertices_pgr_fit" ORDER BY random() limit {n}'
    )
    dane = cursor.fetchall()
    # print('\n surówka z bazy danych \n', dane)

    # rozpakowuje dane
    x = [item[0] for item in dane]  # indeksy punktów
    # print(x)

    coords = [(item[1]) for item in dane]  # współrzedne punktów
    coordsDD = [(item[2]) for item in dane]  # współrzedne punktów
    coordsY = [float(item[11:-1].split()[0]) for item in coordsDD]  # dlugos_geograficzna
    coordsX = [float(item[11:-1].split()[1]) for item in coordsDD]  # szerokosc geograficzna

    df = pd.DataFrame(list(zip(x, coordsY, coordsX, coordsDD, )), columns=['index', 'coordsY', 'coordsX', 'coordsDD', ])

    ############################ Snapowanie ############################

    dane_snapowane = []
    for index, coordX, coordY in zip(df.index, df.coordsX, df.coordsY):
        # pobieram najbliższe werteksy z bazy danych:
        qstring = f'SELECT graf.id, ST_AsText(graf.the_geom) 'f'FROM public."graf_aoi" AS graf  WHERE graf.id = (SELECT id FROM public."graf_aoi_noded" ORDER BY the_geom <-> ST_SetSRID(ST_MakePoint(          20.90936422348022,      52.25404710227145), 4326) LIMIT 1) GROUP BY graf.id, graf.the_geom'
    cursor.execute(qstring)
    print(qstring)
    dane_snapowane.append(cursor.fetchall()[0])
    coords_snapowane = [(item[1]) for item in dane_snapowane]
    print(float(coords_snapowane[0].split(',')[0].split()[0][11:]), '\n',
          float(coords_snapowane[0].split(',')[0].split()[1]))

    # print('Dane 2 \n', dane_snapowane[0])
    # print('Dane 3 \n', dane_snapowane[0][0])

    # x_snapowane = [item[0] for item in dane_snapowane]  # indeksy punktów
    # coords_snapowane = [(item[1]) for item in dane_snapowane]  # współrzedne punktów
    # coordsY_snapowane = [float(item[6:].split()[0]) for item in coords_snapowane]  # dlugos_geograficzna
    # coordsX_snapowane = [float(item[6:-1].split()[1]) for item in coords_snapowane]  # dlugos_geograficzna
    # # print(coordsX_snapowane)
    # df_snapowane = pd.DataFrame(list(zip(x_snapowane, coordsY_snapowane, coordsX_snapowane, coordsDD, )),
    #                             columns=['index', 'coordsY', 'coordsX', 'coordsDD', ])
    #
    # df_sum = pd.concat([df, df_snapowane], axis=1)
    # print(df_sum.to_string())
    #
    # ############################# grupowanie ############################
    # k = 2
    # centroids = np.random.choice(len(x_snapowane), k, replace=False)  # wybieram losowo indeksy centroidów
    # centroidsID = [x_snapowane[item] for item in
    #                centroids]  # na podstawie indeksów wywołuje id z którego będę liczył odległość
    # print('\nIndeksy obiektów wybranych jako centroidy z węzłów grafu: \n', centroidsID)
    #
    #
    # def query_tekst(source, target):
    #     postgreSQL_select_Query = \
    #         f'SELECT * FROM pgr_dijkstra(\'SELECT id, source, target, cost as cost ' \
    #         f'FROM public."graf_aoi"\', {source}, {target}, false)'
    #
    #     print(postgreSQL_select_Query)
    #     return postgreSQL_select_Query
    #
    #
    # def sum_length_from_scratch(tablica):
    #     print(tablica)
    #     dlugosc_drogi = 0
    #     for row in tablica:
    #         dlugosc_drogi = dlugosc_drogi + float(row[4])
    #     return dlugosc_drogi
    #
    #
    # def my_func(centroid, item):
    #     print(centroid, item)
    #     cursor.execute(query_tekst(centroid, item))
    #     print(cursor.fetchall())
    #     return sum_length_from_scratch(cursor.fetchall())
    #
    #
    # distances = ([[my_func(centroid, item) for centroid in centroidsID] for item in x])
    # print('\nOdległości po do każdego z centroidów z każdego z punktów: \n', distances)
    #
    # points = np.array([np.argmin(i) for i in distances])
    # print('\nWynik klasyfikacji: \n', points)
except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia.
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
