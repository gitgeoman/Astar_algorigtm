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
    n = 500
    cursor.execute(
        # f'SELECT id, ST_AsText(geom) FROM public.centroidy_budynki ORDER BY random() limit {n}'
        # f'SELECT id, ST_AsText(geom) FROM public.budynki_wawa_centroidy ORDER BY random() limit {n}'
        f'SELECT id, ST_AsText(geom) FROM public.budynki_wawa_centroidy ORDER BY random() limit {n}'

    )
    buildings_table = cursor.fetchall()
    print(buildings_table)
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
    A_to_sa_wspolrzedne_source_X = [float(wspolrzedna[11:].split(',')[0].split()[0]) for wspolrzedna in
                                    wspolrzedna_lini_siatki]
    A_to_sa_wspolrzedne_source_Y = [float(wspolrzedna[11:].split(',')[0].split()[1]) for wspolrzedna in
                                    wspolrzedna_lini_siatki]

    df_punktow_siatki = pd.DataFrame(
        list(zip(indeksy_punktow_siatki, source_linii, target_linii, wspolrzedna_lini_siatki)),
        columns=['indeksy_punktow_siatki', 'source_linii', 'target_linii', 'wspolrzedna_lini_siatki']
    )

    print('\n\n df z punktami siatki: \n', df_punktow_siatki.to_string())

    # ############################# grupowanie ############################
    k = 4
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
    print('\n\n\n\nfiltered ', f'indeksy_punktow_siatki in ({centroidsAA})', '\n\n', df_filtered.to_string())


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

    klasyfikacja = np.array(
        [np.argmin(i) for i in distances])  # wybieram do którego centroidu jest najblizej do punktu

    df_klasyfikacja = pd.DataFrame(klasyfikacja)

    print('\nWynik klasyfikacji: \n', klasyfikacja)

    print('\n\n\n sumaryczny ', df_klasyfikacja, )

    df_sumaryczny = pd.DataFrame(list(
        zip(indeksy_punktow_siatki, distances, klasyfikacja, A_to_sa_wspolrzedne_source_X,
            A_to_sa_wspolrzedne_source_Y)),
        columns=['indeksy_punktow_siatki', 'distances', 'klasyfikacja', 'A_to_sa_wspolrzedne_source_X',
                 'A_to_sa_wspolrzedne_source_Y'
                 ])
    print(df_sumaryczny.to_string())

    # obliczam współrzędne środka geometrycznego linii dla nowych środków
    df1 = pd.DataFrame([df_sumaryczny.groupby('klasyfikacja')['A_to_sa_wspolrzedne_source_X'].mean(),
                        df_sumaryczny.groupby('klasyfikacja')['A_to_sa_wspolrzedne_source_Y'].mean()]).T
    print('\n średnie współrzędne nowych centroidów \n\n', df1.to_string())

    plt.plot(figsize=(10, 10))

    no_of_iterations = 4
    list_of_dfs = [df_sumaryczny, ]

    for _ in range(no_of_iterations):
        centroidsID = []
        data_centroid_lines = []
        # SNAPOWANIE DO Węzła nowych środków geometrycznych
        for index, coordX, coordY in zip(df1.index, df1.A_to_sa_wspolrzedne_source_X, df1.A_to_sa_wspolrzedne_source_Y):
            # print (index, coordX, coordY)
            qstring = f'SELECT id, source, ST_AsText(geom), target FROM public."500m_g" ORDER BY geom <-> ST_SetSRID(ST_MakePoint({coordX},{coordY}), 4326) LIMIT 1'
            print(qstring)
            cursor.execute(qstring)

            nearese = cursor.fetchall()
            data_centroid_lines.append(nearese)

            centroidsID.append(nearese[0][0])
            # rozpakowuje po snapie
        print('surowe dane po snapie loop: <<<<<<<<<<<<<<<<<<\n', data_centroid_lines)

        indeksy_punktow_siatki_loop = [column[0][0] for column in data_centroid_lines]
        print('\n\nindeksy po snapie loop: \n', indeksy_punktow_siatki_loop)
        source_linii_loop = [column[0][1] for column in data_centroid_lines]
        print('\n\nsource po snapie loop: \n', source_linii_loop)
        wspolrzedna_lini_siatki_loop = [column[0][2] for column in data_centroid_lines]
        print('\n\nwspolrzedna_lini_siatki_loop po snapie: \n', wspolrzedna_lini_siatki_loop)
        target_linii_loop = [column[0][3] for column in data_centroid_lines]
        print('\n\ntarget_linii_loop po snapie: \n', target_linii_loop)
        A_to_sa_wspolrzedne_source_X_loop = [float(wspolrzedna[11:].split(',')[0].split()[0]) for wspolrzedna in
                                             wspolrzedna_lini_siatki_loop]
        A_to_sa_wspolrzedne_source_Y_loop = [float(wspolrzedna[11:].split(',')[0].split()[1]) for wspolrzedna in
                                             wspolrzedna_lini_siatki_loop]

        df_punktow_siatki_loop = pd.DataFrame(
            list(zip(indeksy_punktow_siatki_loop, source_linii_loop, target_linii_loop, wspolrzedna_lini_siatki_loop)),
            columns=['indeksy_punktow_siatki_loop', 'source_linii_loop', 'target_linii_loop',
                     'wspolrzedna_lini_siatki_loop']
        )

        print('\n\n df z punktami siatki: \n', df_punktow_siatki_loop.to_string())

        print('\n Indeksy obiektów wybranych jako centroidy w iteracji \n ',
              centroidsID)
        print(f'indeksy_punktow_siatki_loop in ({centroidsID})')
        df_filtered_loop = df_punktow_siatki_loop.query(f'indeksy_punktow_siatki_loop in ({centroidsID})')
        print('\n\n\n\nfiltered indeksy_punktow_siatki_loop \n>>>>>>>>>>>>>>>>>>>>>>>\n', df_filtered_loop.to_string())

        distances_loop = [[[my_func(source, target)] for source in df_filtered_loop.target_linii_loop] for target in
                          df_punktow_siatki.source_linii]  # tutaj troche nazwy pomieszały sie w tym df

        print('\n\n\n\ndistances_loop \n>>>>>>>>>>>>>>>>>>>>>>>\n', distances_loop)

        klasyfikacja_loop = np.array([np.argmin(i) for i in distances_loop])
        print('\nWynik klasyfikacji: \n', klasyfikacja_loop)

        df_sumaryczny_loop = pd.DataFrame(list(
            zip(indeksy_punktow_siatki, distances_loop, klasyfikacja_loop, A_to_sa_wspolrzedne_source_X,
                A_to_sa_wspolrzedne_source_Y)),
            columns=['indeksy_punktow_siatki', 'distances', 'klasyfikacja', 'A_to_sa_wspolrzedne_source_X',
                     'A_to_sa_wspolrzedne_source_Y'
                     ])
        print(df_sumaryczny_loop.to_string())
        # obliczam współrzędne środka geometrycznego linii dla nowych środków
        df1 = pd.DataFrame([df_sumaryczny_loop.groupby('klasyfikacja')['A_to_sa_wspolrzedne_source_X'].mean(),
                            df_sumaryczny_loop.groupby('klasyfikacja')['A_to_sa_wspolrzedne_source_Y'].mean()]).T
        print('\n średnie współrzędne nowych centroidów \n\n', df1.to_string())
        list_of_dfs.append(df_sumaryczny_loop)

    for one_df in list_of_dfs:
        print('\n df wynikowy \n', one_df.to_string())

    plt.plot(figsize=(10, 10))
    plt.subplots(3, 2, figsize=(10, 14))
    for numer in range(len(list_of_dfs)):
        print('!!!!!!!!!!!!!!!!!!!', numer + 1)
        df_tmp = list_of_dfs[numer]
        groups = df_tmp.groupby('klasyfikacja')
        plt.subplot(3, 2, numer + 1)
        for name, group in groups:
            plt.plot(group.A_to_sa_wspolrzedne_source_Y, group.A_to_sa_wspolrzedne_source_X, marker='o', linestyle='',
                     markersize=3, label=name)
            # do zrobienia centroidy w każdej iteracji
        plt.title(numer)
    # plt.legend()
    plt.grid()
    plt.show()
    # do zrobienie -> wyniki na tle mapy

except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia.
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
