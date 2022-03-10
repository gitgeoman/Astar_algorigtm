import psycopg2
from DB_connection_functions import *
from DB_connection_parameters import user, password, host, port, database3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database3)
    cursor = connection.cursor()

    n = 500  # ile punktów
    k = 4  # ile klas
    no_of_iterations = 50  # ile iteracji

    # wybieram n budynkow (centroidy) z bazy danych
    cursor.execute(
        # f'SELECT id,the_geom AS geom, ST_AsText(the_geom) AS geomDD FROM public."00DrogiINTER_noded_vertices_pgr" ORDER BY random() limit {n}'
        f'SELECT id, geom AS geom, ST_AsText(geom) AS geomText FROM public."budynki_wawa_centroidy" WHERE id in (98642, 67825, 116986, 98408, 77274, 101181, 132431, 93914, 145211, 101030, 34828, 30926, 62567, 44244, 29602, 118337, 99930, 111794, 131409, 130682, 89119, 32528, 139619, 48428, 20973, 33024, 25549, 66815, 128730, 103876, 8693, 121083, 48248, 93809, 118571, 100437, 18877, 3665, 113781, 36388, 132637, 28124, 89716, 120553, 54469, 20314, 142392, 124897, 124639, 138810, 1332, 11378, 9375, 88096, 57839, 3460, 66431, 89651, 63575, 17947, 116674, 94129, 75218, 25618, 43966, 87155, 98155, 108229, 95749, 62943, 115989, 47840, 73215, 116312, 928, 25402, 102093, 123847, 86243, 146291, 8331, 75334, 121477, 123049, 1059, 125770, 135457, 40507, 108565, 119871, 32829, 112015, 93192, 13652, 136754, 4805, 18257, 22614, 131066, 118774, 98203, 33516, 109157, 2919, 98442, 141042, 20964, 80981, 72181, 40996, 72529, 56299, 115794, 52648, 65285, 113363, 89137, 52280, 103495, 101007, 117568, 10001, 96787, 92993, 72664, 64583, 99097, 88169, 121808, 15935, 18719, 146102, 109164, 72717, 35798, 121208, 61549, 141453, 96309, 41227, 116599, 48020, 39920, 1392, 139220, 97285, 23463, 42493, 135574, 110257, 7137, 122235, 104410, 42951, 119454, 130642, 109541, 77401, 110046, 98683, 68866, 3990, 85700, 117346, 59649, 26187, 118607, 124621, 80822, 113450, 133594, 400, 19713, 61228, 10117, 127483, 143846, 106657, 136784, 73088, 100882, 78194, 135855, 89299, 137225, 139588, 121133, 92733, 39248, 108088, 110258, 38732, 110775, 2551, 48775, 99948, 4809, 73971, 87715, 83380, 75754, 77969, 134253, 3779, 28634, 39510, 59403, 14254, 43225, 98383, 59460, 131740, 63074, 96195, 113827, 12909, 55247, 139168, 83049, 21779, 33804, 51282, 49225, 79519, 70616, 135494, 31681, 63934, 90065, 90132, 91202, 39879, 141433, 58758, 129158, 64463, 35260, 90701, 20517, 94060, 69175, 70117, 11395, 74617, 131374, 122373, 16465, 61983, 114664, 24921, 60050, 84910, 92000, 80819, 126823, 142805, 66844, 118670, 111700, 33950, 39642, 26663, 88301, 113102, 97503, 35934, 113401, 39073, 124316, 116612, 488, 58548, 96468, 103475, 109259, 17172, 78558, 89426, 128895, 131572, 106050, 101712, 21958, 3885, 18752, 85068, 85611, 11021, 53124, 5078, 64906, 91176, 36522, 99849, 94439, 141683, 11329, 34162, 57900, 25583, 5068, 79652, 2580, 58576, 107347, 107642, 31535, 76655, 125869, 10769, 23231, 98853, 46163, 148243, 102747, 32703, 51158, 29735, 17570, 8395, 29178, 9004, 138675, 123977, 2010, 121980, 103875, 143559, 136790, 9122, 100363, 114503, 102207, 35424, 91208, 50450, 4584, 32806, 2930, 41370, 53793, 138534, 100401, 134816, 102155, 52219, 141844, 147230, 37716, 135508, 34952, 13546, 45109, 101462, 141002, 143809, 121262, 57819, 138722, 102922, 91, 21393, 138731, 2083, 69155, 103966, 80223, 96060, 31186, 118188, 78608, 36707, 5009, 54140, 101783, 113175, 145421, 16551, 39319, 61618, 59557, 123123, 120957, 45271, 15700, 90428, 123632, 93160, 131673, 96333, 1585, 121885, 70157, 86664, 3103, 1173, 147247, 3336, 145095, 101124, 59122, 94750, 34956, 11748, 84374, 125660, 56054, 127178, 34701, 71730, 61182, 79391, 25597, 25174, 84612, 23729, 108560, 88103, 4891, 104479, 119153, 109621, 125595, 11125, 18972, 8971, 52456, 46837, 18534, 113084, 76013, 39360, 45156, 27789, 144008, 120180, 92874, 131155, 107175, 53877, 141508, 74601, 68265, 24145, 91607, 117216, 146926, 148483, 105014, 148081, 61048, 33719, 115435, 107768, 35464, 99550, 131243, 147390, 29620, 139884, 69930, 141525, 119366, 37065, 92503, 139820, 3630, 84962, 14257, 8486, 38619, 39583, 117016, 25295, 103908, 129523, 59292, 7562, 37698, 131283, 42536, 100286, 135436, 83119, 8792, 27630, 129918, 68483, 137098, 125644, 56893, 40542, 128973, 126453, 74566, 85593, 132344, 36109, 129427, 122503) limit {n}'
    )
    dane_budynki_z_bazy_danych = cursor.fetchall()

    # rozpakowuje dane o budynkach
    index_budynynki_z_bazy_danych = [item[0] for item in dane_budynki_z_bazy_danych]  # indeksy punktów
    coords_budynynki_z_bazy_danych = [(item[1]) for item in dane_budynki_z_bazy_danych]  # współrzedne punktów
    coordsDD_budynynki_z_bazy_danych = [(item[2]) for item in dane_budynki_z_bazy_danych]  # współrzedne punktów
    coordsDX_budynynki_z_bazy_danych = [[float(item[7:-1].split()[0]), float(item[7:-1].split()[1])] for item in
                                        coordsDD_budynynki_z_bazy_danych]
    coordsY_budynynki_z_bazy_danych = [float(item[6:-1].split()[0]) for item in coordsDD_budynynki_z_bazy_danych]
    coordsX_budynynki_z_bazy_danych = [float(item[7:-1].split()[1]) for item in coordsDD_budynynki_z_bazy_danych]

    zipped_dane_budynki_z_bazy_danych = list(
        zip(index_budynynki_z_bazy_danych,
            coordsY_budynynki_z_bazy_danych,
            coordsX_budynynki_z_bazy_danych,
            ))

    df_rozp_budynynki_z_bazy_danych = pd.DataFrame(
        zipped_dane_budynki_z_bazy_danych,
        columns=['db_index', 'coordsY', 'coordsX', ]
    )

    # print('\n rozpakowane dane w data frame df_r\n', df_rozp_budynynki_z_bazy_danych.to_string())

    #################snapowanie punktow budynkow do wezlow sieci drogowej z bazy danych

    tablica_na_snap_do_wezlow_sieci_drogowej = []
    for index, coordX, coordY in zip(df_rozp_budynynki_z_bazy_danych.db_index,
                                     df_rozp_budynynki_z_bazy_danych.coordsX,
                                     df_rozp_budynynki_z_bazy_danych.coordsY):
        cursor.execute(
            f'SELECT v.id, St_AsText(v.the_geom) FROM public."00DrogiINTER_noded_vertices_pgr" AS v, public."00DrogiINTER_noded" AS e '
            f'WHERE v.id = (SELECT id FROM public."00DrogiINTER_noded_vertices_pgr" '
            f'ORDER BY the_geom <-> ST_SetSRID(ST_MakePoint({coordY}, {coordX}), 4326) LIMIT 1 '
            f') '
            f'AND (e.source=v.id OR e.target=v.id) GROUP BY v.id, v.the_geom')
        nearese = cursor.fetchall()
        tablica_na_snap_do_wezlow_sieci_drogowej.append(nearese[0])

    # print('\n wszystkie_nearse \n ', tablica_na_snap_do_wezlow_sieci_drogowej)

    # rozpakowuje dane po snapie
    index_wezlow_sieci_drogowej_po_snapie = [item[0] for item in
                                             tablica_na_snap_do_wezlow_sieci_drogowej]  # indeksy punktów

    coords_wezlow_sieci_drogowej_po_snapie = [(item[1]) for item in
                                              tablica_na_snap_do_wezlow_sieci_drogowej]  # współrzedne punktów

    coordsDD_wezlow_sieci_drogowej_po_snapie = [(item[1]) for item in
                                                tablica_na_snap_do_wezlow_sieci_drogowej]  # współrzedne punktów

    coordsDX1 = [[float(item[7:-1].split()[0]), float(item[7:-1].split()[1])] for item in
                 coordsDD_wezlow_sieci_drogowej_po_snapie]

    coordsY1_wezlow_sieci_drogowej_po_snapie = [float(item[6:-1].split()[0]) for item in
                                                coordsDD_wezlow_sieci_drogowej_po_snapie]

    coordsX1_wezlow_sieci_drogowej_po_snapie = [float(item[7:-1].split()[1]) for item in
                                                coordsDD_wezlow_sieci_drogowej_po_snapie]

    zipped_dane_budynki_z_bazy_danych_po_snapie = list(zip(index_budynynki_z_bazy_danych,
                                                           coordsY_budynynki_z_bazy_danych,
                                                           coordsX_budynynki_z_bazy_danych,
                                                           index_wezlow_sieci_drogowej_po_snapie,
                                                           coordsY1_wezlow_sieci_drogowej_po_snapie,
                                                           coordsX1_wezlow_sieci_drogowej_po_snapie,
                                                           )
                                                       )

    df_rozp_wezlow_sieci_drogowej_po_snapie = pd.DataFrame(
        zipped_dane_budynki_z_bazy_danych_po_snapie,
        columns=['db_index_budynki', 'coordsY_budynki',
                 'coordsX_budynki', 'db_index', 'coordsY',
                 'coordsX', ])

    print('\n\n\n df_rozp_wezlow_sieci_drogowej_po_snapie \n\n\n',
          df_rozp_wezlow_sieci_drogowej_po_snapie.head().to_string())


    def my_func(centroid, item):
        postgreSQL_select_Query1 = f"SELECT MIN(r.seq) AS seq, " \
                                   f"e.old_id AS id, " \
                                   f"sum(e.distance) AS distance, " \
                                   f"ST_Collect(e.the_geom) AS geom " \
                                   f"FROM pgr_dijkstra('SELECT id, source, target, distance as cost FROM public.\"00DrogiINTER_noded\"', {centroid}, {item}, false ) AS r, " \
                                   f"public.\"00DrogiINTER_noded\" AS e " \
                                   f"WHERE r.edge=e.id " \
                                   f"GROUP BY e.old_id"

        cursor.execute(postgreSQL_select_Query1)
        return sum_length_from_scratch(cursor.fetchall())


    # print('\nIndeksy punktów w obliczeniach x: \n', x, 'wspolrzedne punktów w obliczeniach coords:\n', coords, '\n',coordsDD)

    # wybieram losowo k punktów na centroidy do pierwszej iteracji (oznacza to że będzie k grup)

    centroids = np.random.choice(
        len(index_wezlow_sieci_drogowej_po_snapie),
        k,
        replace=False
    )  # indeksy centroidów z danych po snapie

    ID_centroidow_wezlow_sieci_drogowej_po_snapie = [index_wezlow_sieci_drogowej_po_snapie[item] for item in
                                                     centroids]  # id centroidow
    print('\nIndeksy obiektów wybranych jako centroidy do pierwszej iteracji: \n',
          ID_centroidow_wezlow_sieci_drogowej_po_snapie)

    odleglosc_punkt_centroid = (
        [[my_func(centroid, item) for centroid in ID_centroidow_wezlow_sieci_drogowej_po_snapie] for item in
         index_wezlow_sieci_drogowej_po_snapie])

    # print('\nOdległości od każdego centroidów z każdego z punktów: \n', odleglosc_punkt_centroid)

    klasyfikacja = np.array(
        [np.argmin(i) for i in odleglosc_punkt_centroid])  # wybieram do którego centroidu jest najblizej do punktu

    print('\nWynik klasyfikacji: \n', klasyfikacja)

    # obliczam gdzie jest środek każdej z klas
    # wywołuję indeksy każdej klasy i ich współrzędne

    zipped_pierwsza_klasyfikacja = list(
        zip(index_budynynki_z_bazy_danych,
            coordsY_budynynki_z_bazy_danych,
            coordsX_budynynki_z_bazy_danych,
            index_wezlow_sieci_drogowej_po_snapie,
            coordsY1_wezlow_sieci_drogowej_po_snapie,
            coordsX1_wezlow_sieci_drogowej_po_snapie,
            odleglosc_punkt_centroid,
            klasyfikacja,
            ))
    df_pierwsza_klasyfikacja = pd.DataFrame(
        zipped_pierwsza_klasyfikacja,
        columns=['db_index_budynki', 'coordsY_budynki',
                 'coordsX_budynki', 'db_index', 'coordsY',
                 'coordsX', 'distances', 'klasyfikacja']
    )
    print('\n', df_pierwsza_klasyfikacja.head().to_string())

    # obliczam współrzędne dla nowych centroidów
    df_nowe_centroidy = pd.DataFrame(
        [df_pierwsza_klasyfikacja.groupby('klasyfikacja')['coordsX'].mean(),
         df_pierwsza_klasyfikacja.groupby('klasyfikacja')['coordsY'].mean()]
    ).T
    print('\n średnie współrzędne nowych centroidów \n\n', df_nowe_centroidy.to_string())

    list_of_dfs = [df_pierwsza_klasyfikacja, ]

    for _ in range(no_of_iterations):
        # SNAPOWANIE DO NAJBLIZSZEGO WEZLA SIATKI NOWYCH CENTROIDOW
        ID_centroidow_wezlow_sieci_drogowej_petla = []
        for index, coordX, coordY in zip(df_nowe_centroidy.index, df_nowe_centroidy.coordsX, df_nowe_centroidy.coordsY):
            cursor.execute(
                f'SELECT v.id, St_AsText(v.the_geom) FROM public."00DrogiINTER_noded_vertices_pgr" AS v, public."00DrogiINTER_noded" AS e '
                f'WHERE v.id = (SELECT id FROM public."00DrogiINTER_noded_vertices_pgr" '
                f'ORDER BY the_geom <-> ST_SetSRID(ST_MakePoint({coordY}, {coordX}), 4326) LIMIT 1 '
                f') '
                f'AND (e.source=v.id OR e.target=v.id) GROUP BY v.id, v.the_geom')
            nearese1 = cursor.fetchall()
            ID_centroidow_wezlow_sieci_drogowej_petla.append(nearese1[0][0])
        print('\n Indeksy obiektów wybranych jako centroidy w KOLEJNEJ iteracji \n ',
              ID_centroidow_wezlow_sieci_drogowej_petla)

        odleglosc_punkt_centroid_petla = (
            [[my_func(centroid, item) for centroid in ID_centroidow_wezlow_sieci_drogowej_petla] for item in
             index_wezlow_sieci_drogowej_po_snapie])

        klasyfikacja_petla = np.array([np.argmin(i) for i in
                                       odleglosc_punkt_centroid_petla])  # wybieram do którego centroidu jest najblizej do punktu

        zipped_petla = list(zip(index_budynynki_z_bazy_danych,
                                coordsY_budynynki_z_bazy_danych,
                                coordsX_budynynki_z_bazy_danych,
                                index_wezlow_sieci_drogowej_po_snapie,
                                coordsY1_wezlow_sieci_drogowej_po_snapie,
                                coordsX1_wezlow_sieci_drogowej_po_snapie,
                                odleglosc_punkt_centroid_petla,
                                klasyfikacja_petla
                                )
                            )
        df_petla = pd.DataFrame(zipped_petla,
                                columns=['db_index_budynki', 'coordsY_budynki',
                                         'coordsX_budynki', 'db_index', 'coordsY',
                                         'coordsX', 'distances', 'klasyfikacja'])
        print('\n df wynikowy dla bierzacej iteracji \n', df_petla.to_string())
        list_of_dfs.append(df_petla)

    # przegląd danych
    print(' TU WYŚWIETLAM KOMPLET WYNIKÓW W POSTACI DF>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>. \n', )

    for idx, one_df in enumerate(list_of_dfs):
        one_df.to_csv(f'results_of_classification/{idx}')
        print('\n df wynikowy \n', one_df.to_string())

    plt.subplots(3, 2, figsize=(10, 14))
    rysunek_nr = 0
    for numer in range(len(list_of_dfs))[-6:]:
        print('!!!!!!!!!!!!!!!!!!!', numer + 1)
        df_tmp = list_of_dfs[numer]
        groups = df_tmp.groupby('klasyfikacja')
        plt.subplot(3, 2, rysunek_nr + 1)
        rysunek_nr += 1
        for name, group in groups:
            plt.plot(group.coordsY, group.coordsX, marker='o', linestyle='', markersize=3, label=name)
            # do zrobienia centroidy w każdej iteracji
        plt.title(numer)
    # plt.legend()
    plt.show()

except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia,
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
