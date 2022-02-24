# nawiąż połączenie
import psycopg2
from DB_connection_functions import *
from DB_connection_parameters import user, password, host, port, database3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database3)
    cursor = connection.cursor()

    # ile punktow
    n = 5
    cursor.execute(
        # f'SELECT id, ST_AsText(geom) FROM public.centroidy_budynki ORDER BY random() limit {n}'
        f'SELECT id, ST_AsText(geom) FROM public.budynki_wawa_centroidy ORDER BY random() limit {n}'

    )
    buildings_table = cursor.fetchall()

    ############################ ROZPAKOWUJE DANE ############################

    indeksy_budynki = [column[0] for column in buildings_table]
    # print(indeksy_budynki)
    wspolrzedna_budynki_X = [float(column[1][6:-1].split()[0]) for column in buildings_table]
    wspolrzedna_budynki_Y = [float(column[1][6:-1].split()[1]) for column in buildings_table]
    df = pd.DataFrame(
        list(zip(indeksy_budynki, wspolrzedna_budynki_X, wspolrzedna_budynki_Y)),
        columns=['indeks', 'X', 'Y']
    )
    print('\n\ndf z danymi początkowymi: \n', df)

    dane_snapowane = []
    # Snapowanie do węzłów siatki graf wszystkich punktow
    for index, coordX, coordY in zip(df.indeks, df.X, df.Y):
        qstring = f'SELECT id, source, ST_AsText(geom), target FROM public."500m_g" ORDER BY geom <-> ST_SetSRID(ST_MakePoint({coordX},{coordY}), 4326) LIMIT 1'

        # print(qstring)
        cursor.execute(qstring)
        dane_snapowane.append(cursor.fetchall()[0])
    # print(dane_snapowane)

    ############################ ROZPAKOWUJE DANE po snapie ############################

    indeksy_punktow_siatki = [column[0] for column in dane_snapowane]
    print('\n\nindeksy po snapie: \n', indeksy_punktow_siatki)
    source_linii = [column[1] for column in dane_snapowane]
    wspolrzedna_lini_siatki = [column[2] for column in dane_snapowane]
    target_linii = [column[3] for column in dane_snapowane]

    df_punktow_siatki = pd.DataFrame(
        list(zip(indeksy_punktow_siatki, source_linii, target_linii, wspolrzedna_lini_siatki)),
        columns=['indeksy_punktow_siatki', 'source_linii', 'target_linii', 'wspolrzedna_lini_siatki']
    )

    print('\n\n df z punktami siatki: \n', df_punktow_siatki.to_string())

    # ############################# grupowanie ############################
    k = 2
    indeksy_punktow_centralnych_w_grupie = np.random.choice(len(indeksy_punktow_siatki), k,
                                                            replace=False)

    #############TRZEBA wybrać source centroidów i target punktów i między nimi liczyć odległość!!!!!!!!!!!!!!!!!!!!!!

    # wybieram losowo indeksy centroidów
    centroidsID = [[indeksy_punktow_siatki[item], source_linii[item]] for item in
                   indeksy_punktow_centralnych_w_grupie]  # id i source obiektów wybranych do pierwszej iteracji
    print('\n Source punktow z najbliższych węzłów grafu: \n', centroidsID)
    centroidsAA = [indeksy_punktow_siatki[item] for item in indeksy_punktow_centralnych_w_grupie]
    print(centroidsAA)  # <<<< indeksy centroidów do grupowania w pierwszej iteracji
    df_filtered = df_punktow_siatki.query(f'indeksy_punktow_siatki in ({centroidsAA})')
    print('\n\n\n\nfiltered ', df_filtered.to_string())


    def my_func(source, target):
        postgreSQL_select_Query = \
            f'SELECT * FROM pgr_astar(\'SELECT id, source, target, cost, reverse_co, x1, y1, x2, y2 FROM public."500m_g"\', {source}, {target}, directed := false, heuristic := 5)'
        print(postgreSQL_select_Query)
        cursor.execute(postgreSQL_select_Query)
        response = cursor.fetchall()
        response = response[-1][5]
        return response


    distances = [[[my_func(source, target)] for target in df_filtered.target_linii] for source in
                 df_punktow_siatki.source_linii]

    print('\n\nOdległości po do każdego z centroidów z każdego z punktów: \n', distances)

    df_distances = pd.DataFrame(distances)

    print('\n\n', df_distances, '\n\n')
    # print('\n\n', df_distances.T)

    # df_distances = df_distances.T
    # df_distances.columns = df_filtered.source_linii
    # print('\n\n to jest df_distances\n\n', df_distances)
    #
    # # zrobione jest zliczanie odległości miedzy wskazywanymi punktami siatki
    # # tearaz do zrobienia grupowanie

    klasyfikacja = np.array(
        [np.argmin(i) for i in distances])  # wybieram do którego centroidu jest najblizej do punktu

    df_klasyfikacja = pd.DataFrame(klasyfikacja)

    print('\nWynik klasyfikacji: \n', klasyfikacja)

    # klasyfikacja jest poprawiona 

except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia.
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
