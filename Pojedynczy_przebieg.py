import psycopg2
from DB_connection_functions import *
from DB_connection_parameters import user, password, host, port, database
import numpy as np

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()

    n = 5

    cursor.execute(f'SELECT * FROM public."lineEdges_noded_vertices_pgr" ORDER BY random() limit {n}')
    dane = cursor.fetchall()

    x = [item[0] for item in dane]
    coords = [(item[5]) for item in dane]
    print('indeksy punktów w obliczeniach: \n', x, '\n', coords)

    k = 2
    centroids = np.random.choice(len(x), k, replace=False)
    centroidsID = [x[item] for item in centroids]
    print('\n indeksy obiektów wybranych jako centroidy do pierwszej iteracji: \n', centroidsID)


    def my_func(centroid, item):
        cursor.execute(query_tekst(centroid, item))
        return sum_length_from_scratch(cursor.fetchall())


    distances = ([[my_func(centroid, item) for centroid in centroidsID] for item in x])

    points = np.array([np.argmin(i) for i in distances])
    print('\n wynik klasyfikacji: \n', points)

except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia.
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
