# Loading the required modules

import psycopg2

from conn_data import user, password, host, port, database
import numpy as np

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from A_star import kmeans

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()

    # ile punktów
    n = 4000

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
    tablica_dane = np.column_stack([coordsY, coordsX], )

    print('>>>>>>>>>>>>>>>>>>>>>', tablica_dane)

    pca = PCA(2)
    df = pca.fit_transform(tablica_dane)

    label = kmeans(df, 5, 10000)

    u_labels = np.unique(label)
    for i in u_labels:
        plt.scatter(df[label == i, 0], df[label == i, 1], label=i)
    plt.legend()
    plt.grid
    plt.show()


except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia.
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
