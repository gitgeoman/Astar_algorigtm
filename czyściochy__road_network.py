import psycopg2

from DB_connection_parameters import user, password, host, port, database3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rozpakowuje_dane_z_bazy_danych(dane_budynki_z_bazy_danych):
    coordsDD_budynynki_z_bazy_danych = [(item[2]) for item in dane_budynki_z_bazy_danych]  # współrzedne punktów

    zipped_dane_budynki_z_bazy_danych = list(
        zip([item[0] for item in dane_budynki_z_bazy_danych],
            [float(item[7:-1].split()[1]) for item in coordsDD_budynynki_z_bazy_danych],
            [float(item[6:-1].split()[0]) for item in coordsDD_budynynki_z_bazy_danych],
            ))

    return pd.DataFrame(
        zipped_dane_budynki_z_bazy_danych,
        columns=['db_index_budynki', 'coordsX_budynki', 'coordsY_budynki', ]
    )


def sum_length_from_scratch(tablica):
    dlugosc_drogi = 0
    for row in tablica:
        dlugosc_drogi = dlugosc_drogi + float(row[2])
    return dlugosc_drogi


def my_func(centroid, item):  # funkcja do odnajdywania najkrotszej drogi miedzy punktami w sieci drogowej

    postgreSQL_select_Query1 = f"SELECT MIN(r.seq) AS seq, " \
                               f"e.old_id AS id, " \
                               f"e.distance AS distance, " \
                               f"ST_Collect(e.the_geom) AS geom " \
                               f"FROM pgr_dijkstra('SELECT id, source, target, distance as cost FROM public.\"00DrogiINTER_noded\"', {centroid}, {item}, false ) AS r, " \
                               f"public.\"00DrogiINTER_noded\" AS e " \
                               f"WHERE r.edge=e.id " \
                               f"GROUP BY e.old_id, e.distance"

    cursor.execute(postgreSQL_select_Query1)
    return sum_length_from_scratch(cursor.fetchall())


# SNAPUJE DANE DO SIECI DROGOWEJ
def snapowanie_budynkow_do_sieci_drogowej(df_rozpakowane_dane_o_budynkach):
    tablica_na_snap_do_wezlow_sieci_drogowej = []
    for index_b, coordX_b, coordY_b in zip(df_rozpakowane_dane_o_budynkach.db_index_budynki,
                                           df_rozpakowane_dane_o_budynkach.coordsY_budynki,
                                           df_rozpakowane_dane_o_budynkach.coordsX_budynki):
        cursor.execute(
            f'SELECT v.id, St_AsText(v.the_geom) FROM public."00DrogiINTER_noded_vertices_pgr" AS v, public."00DrogiINTER_noded" AS e '
            f'WHERE v.id = (SELECT id FROM public."00DrogiINTER_noded_vertices_pgr" '
            f'ORDER BY the_geom <-> ST_SetSRID(ST_MakePoint({coordX_b}, {coordY_b}), 4326) LIMIT 1 '
            f') '
            f'AND (e.source=v.id OR e.target=v.id) GROUP BY v.id, v.the_geom')
        nearese = cursor.fetchall()
        tablica_na_snap_do_wezlow_sieci_drogowej.append(nearese[0])

    coordsDD_wezlow_sieci_drogowej_po_snapie = [(item[1]) for item in tablica_na_snap_do_wezlow_sieci_drogowej]  # współrzedne punktów

    zipped_dane_budynki_z_bazy_danych_po_snapie = list(zip(
        df_rozpakowane_dane_o_budynkach.db_index_budynki,
        df_rozpakowane_dane_o_budynkach.coordsX_budynki,
        df_rozpakowane_dane_o_budynkach.coordsY_budynki,
        [item[0] for item in tablica_na_snap_do_wezlow_sieci_drogowej],
        [float(item[7:-1].split()[1]) for item in coordsDD_wezlow_sieci_drogowej_po_snapie],
        [float(item[6:-1].split()[0]) for item in coordsDD_wezlow_sieci_drogowej_po_snapie]
    ))
    df_rozp_wezlow_sieci_drogowej_po_snapie = pd.DataFrame(
        zipped_dane_budynki_z_bazy_danych_po_snapie,
        columns=['db_index_budynki', 'coordsX_budynki', 'coordsY_budynki', 'index_snap', 'X_snap', 'Y_snap', ]
    )
    # print('\n\n\n df_rozp_wezlow_sieci_drogowej_po_snapie: \n', df_rozp_wezlow_sieci_drogowej_po_snapie.to_string())

    return df_rozp_wezlow_sieci_drogowej_po_snapie


def snapowanie_centroidow_do_sieci_drogowej(df_nowe_centroidy):
    tablica_na_snap_do_wezlow_sieci_drogowej = []
    for coordX_b, coordY_b in zip(df_nowe_centroidy.Y_snap, df_nowe_centroidy.X_snap):
        cursor.execute(
            f'SELECT v.id, St_AsText(v.the_geom) FROM public."00DrogiINTER_noded_vertices_pgr" AS v, public."00DrogiINTER_noded" AS e '
            f'WHERE v.id = (SELECT id FROM public."00DrogiINTER_noded_vertices_pgr" '
            f'ORDER BY the_geom <-> ST_SetSRID(ST_MakePoint({coordX_b}, {coordY_b}), 4326) LIMIT 1 '
            f') '
            f'AND (e.source=v.id OR e.target=v.id) GROUP BY v.id, v.the_geom')
        nearese_loop = cursor.fetchall()

        tablica_na_snap_do_wezlow_sieci_drogowej.append(nearese_loop[0])

    coordsDD_wezlow_sieci_drogowej_po_snapie = [(item[1]) for item in tablica_na_snap_do_wezlow_sieci_drogowej]  # współrzedne punktów

    zipped_dane_budynki_z_bazy_danych_po_snapie = list(zip(
        [item[0] for item in tablica_na_snap_do_wezlow_sieci_drogowej],
        [float(item[6:-1].split()[0]) for item in coordsDD_wezlow_sieci_drogowej_po_snapie],
        [float(item[7:-1].split()[1]) for item in coordsDD_wezlow_sieci_drogowej_po_snapie]
    ))
    df_rozp_wezlow_sieci_drogowej_po_snapie = pd.DataFrame(
        zipped_dane_budynki_z_bazy_danych_po_snapie,
        columns=['index_snap', 'X_snap', 'Y_snap', ]
    )
    # print('\n\n\n df_rozp_wezlow_sieci_drogowej_po_snapie: \n', df_rozp_wezlow_sieci_drogowej_po_snapie.to_string())

    return df_rozp_wezlow_sieci_drogowej_po_snapie


try:
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database3)
    cursor = connection.cursor()

    n = 30  # ile punktów
    k = 5  # ile klas
    no_of_iterations = 10  # ile iteracji

    # POBIERAM DANE Z BAZY DANYCH
    cursor.execute(
        f'SELECT id, geom AS geom, ST_AsText(geom) AS geomText FROM public."budynki_wawa_centroidy" WHERE id in '
        f'(107928, 715, 71239, 3208, 11886, 112065, 67538, 15797, 87341, 147743, 87155, 37643, 137208, 18530, 135400, 28711, 137367, 95230, 89859, 125530, 42806, 77479, 19067, 82170, 36567, 77064, 124159, 42722, 63825, 105184, 42158, 113438, 131625, 105316, 9211, 67100, 54973, 39689, 139736, 100104, 136069, 63594, 7431, 108783, 50423, 119633, 75855, 16307, 13292, 138946, 47980, 4388, 61097, 10492, 50892, 77293, 46653, 69850, 57813, 52506, 62145, 90210, 99424, 34805, 77713, 27719, 147222, 106266, 146770, 29427, 86169, 316, 115027, 106259, 97220, 35069, 23531, 38824, 42425, 135415, 64775, 10088, 68579, 63944, 20882, 48954, 68586, 102326, 95552, 84685, 33028, 79006, 10609, 27195, 142178, 53718, 51565, 65124, 91054, 80358, 67863, 147299, 46036, 25555, 31826, 147968, 45628, 113315, 104177, 81325, 126551, 105623, 126575, 129739, 96789, 119912, 33070, 38608, 91564, 134292, 8815, 73649, 18157, 7637, 19384, 83123, 31265, 88223, 60590, 110657, 5134, 12037, 3757, 68888, 6992, 87670, 106724, 86545, 16298, 101034, 40599, 91521, 104483, 119843, 3116, 124863, 2097, 61904, 29011, 109681, 37990, 186, 59256, 17699, 3758, 142361, 34536, 145098, 73165, 77333, 43298, 45837, 141959, 56363, 44138, 27475, 92870, 99413, 27582, 64700, 132987, 41320, 38522, 136415, 69086, 52959, 85119, 54593, 130010, 3377, 141228, 130591, 24534, 67867, 12587, 101123, 146602, 75313, 146843, 76762, 1781, 106624, 21465, 43094, 73603, 46881, 137103, 78889, 131771, 114754, 133205, 129922, 70504, 115008, 124971, 65766, 30377, 31732, 145042, 43134, 118945, 107873, 141899, 144874, 68102, 118665, 116281, 17781, 23675, 21766, 66841, 11280, 71235, 35180, 84597, 74085, 66009, 46269, 66093, 91810, 15890, 34612, 96807, 36364, 138932, 137404, 27289, 70736, 10770, 76396, 21972, 16104, 91554, 11604, 80444, 105518, 118701, 15716, 109837, 85360, 58202, 36793, 39424, 39724, 91195, 20270, 73186, 61705, 84886, 20510, 54176, 89713, 2305, 83812, 109341, 23704, 135778, 146409, 138864, 61991, 114064, 25838, 39346, 73447, 115358, 110089, 92346, 126775, 104381, 128435, 95310, 6554, 67701, 143193, 28441, 145026, 75099, 62113, 136894, 39339, 117918, 64455, 102128, 98028, 124421, 62803, 82102, 94893, 3282, 130716, 146217, 99769, 85658, 84173, 139806, 20430, 90407, 131150, 64052, 133803, 81173, 35514, 48739, 41539, 67198, 55174, 100727, 47923, 113366, 100871, 111181, 76015, 56534, 92201, 132062, 34890, 8652, 65831, 104957, 117138, 140604, 89567, 143244, 76286, 21421, 63613, 49476, 31512, 109989, 83711, 111210, 59911, 19262, 90200, 94368, 3137, 126993, 124265, 128244, 114167, 4514, 38484, 73444, 131507, 49573, 115646, 102824, 29370, 18968, 69193, 46957, 79803, 130358, 104018, 39018, 28563, 137592, 44755, 134103, 59721, 101648, 6603, 122496, 693, 25893, 111614, 13895, 137187, 52512, 34721, 121328, 38239, 17281, 85099, 50367, 21685, 139213, 110942, 36262, 29239, 57898, 115762, 49890, 91751, 11748, 94906, 96489, 109201, 93916, 117279, 92304, 8456, 100878, 8971, 90972, 92630, 146831, 118531, 117793, 25767, 43447, 121857, 103436, 80986, 27343, 27566, 93732, 14053, 9265, 1778, 115823, 25420, 20008, 81792, 71009, 29455, 27275, 112039, 42648, 131956, 121018, 111935, 5876, 54749, 91266, 142998, 147985, 67496, 19780, 99662, 7787, 93816, 1642, 122287, 123666, 112100, 136696, 7211, 53779, 71957, 117564, 63046, 106363, 29943, 48432, 34439, 48506, 127353, 54695, 72450, 131360, 145512, 110525, 11622, 121347, 75953, 41637, 142330, 51671, 97034, 120902, 21217, 133046, 23904, 98237, 136007, 138157, 140685, 131958, 46361, 113788, 83199, 126029, 55091, 89182, 3639, 12655, 4991, 114650, 128162, 57087, 91702, 137842, 115115, 4546, 17636, 56957, 139837, 91659, 12364, 102216, 82917, 70840, 24659, 65922, 81878, 67258, 75975, 51149, 17840, 136108, 132706, 47399, 74153, 78546, 141412, 59122, 116521, 68667, 110256, 116830, 120216, 97862, 90057, 144696, 79173, 12517, 57284, 46366, 126517, 139292, 129826, 32331, 132371, 56593, 99719, 9622, 37295, 96449, 6114, 141665, 104775, 17484, 41310, 2453, 85681, 15476, 20190, 107189, 61029, 86815, 24671, 68374, 85793, 47577, 55573, 100363, 10156, 105724, 628, 85237, 77080, 71560, 122689, 117619, 69335, 39850, 32439, 79955, 48815, 15660, 32716, 82399, 125410, 142010, 1732, 148715, 116992, 41886, 102507, 21424, 146285, 20215, 122228, 95859, 128748, 33889, 38338, 98461, 112426, 136635, 5821, 66251, 121022, 117689, 6316, 27722, 54386, 51701, 88846, 2636, 101704, 62264, 42686, 140731, 130842, 87806, 52413, 24148, 47513, 24794, 74211, 114356, 80487, 55955, 45228, 124484, 56228, 78159, 112780, 3443, 129295, 86749, 146777, 39786, 98803, 49108, 40023, 140103, 35470, 31029, 34979, 42179, 6993, 128788, 145436, 132417, 69602, 66504, 129656, 59125, 91575, 117139, 26477, 132109, 2738, 5820, 19487, 98875, 99150, 27347, 79976, 54911, 135670, 130870, 9252, 68832, 101682, 145417, 36149, 27890, 15651, 116625, 81959, 67306, 108769, 119120, 135362, 70478, 137185, 30246, 61067, 136587, 40867, 89205, 84431, 82974, 52085, 5388, 59293, 67955, 53327, 128126, 23073, 130659, 59526, 111069, 72922, 16084, 82655, 109399, 106130, 129138, 113595, 45387, 145062, 85495, 51353, 129768, 10316, 83558, 42836, 100156, 56606, 15971, 31310, 100547, 100003, 96452, 96041, 74411, 122631, 107778, 22262, 34527, 24936, 19860, 28216, 116295, 44424, 140999, 24786, 89354, 45989, 145753, 110381, 111621, 119447, 44216, 46781, 104270, 59461, 2231, 46941, 3356, 69057, 44615, 6443, 91821, 49715, 136249, 16457, 56684, 143364, 69823, 99202, 66462, 116544, 44211, 87193, 102130, 102628, 26918, 130355, 142646, 52603, 101024, 140732, 146810, 90001, 85212, 82179, 71953, 25257, 45302, 140193, 38837, 21438, 72533, 51448, 28355, 77454, 104431, 66409, 72135, 12680, 21246, 45545, 6483, 125818, 14118, 6538, 2127, 130760, 106644, 250, 26827, 17940, 45107, 57308, 139635, 118727, 83450, 44422, 89225, 145581, 19872, 117668, 25655, 140464, 52684, 33982, 67911, 118895, 88400, 19547, 572, 55324, 46740, 106085, 83608, 113078, 21778, 89257, 60423, 66819, 98488, 76206, 74986, 68962, 68656, 8457, 12128, 81347, 36062, 6929, 105093, 50934, 134946, 2011, 133258, 129946, 53651, 64594, 34677, 57267, 90517, 8569, 27354, 103194, 82481, 24714, 119430, 79602, 54879, 46675, 3504, 25450, 6303, 31515, 16915, 85952, 80867, 112833, 24119, 123718, 109551, 12591, 132630, 8999, 114429, 62261, 53908, 2283, 95698, 25594, 34079, 35429, 148739, 50562, 74987, 43373, 94026, 72413, 4429, 87587, 94434, 135229, 86875, 78909, 33735, 72427, 148655, 35224, 110410, 68058, 59881, 133709, 69969, 2445, 87346, 118351, 122943, 66906, 123106, 101452, 9126, 132097, 565, 76707, 81650, 7752, 22631, 114812, 105928, 124948, 45521, 39983, 144349, 66552, 144851, 15713, 41657, 120145, 31970, 51111, 50915, 4857, 109772, 89141, 101227, 138234, 108307, 134465, 100825, 18269, 50333, 123109, 74379, 8991, 112549, 27278, 11419, 78732, 50882, 16529, 44674, 110218, 138975, 52795, 73004, 122047, 9755, 62234, 28374, 27121, 39565, 143883, 118799, 147526, 98066, 77114, 14126, 128432, 58787, 43565, 111199, 99093, 75442, 75128, 131722, 23771, 102135, 56566, 104983, 43958, 38756, 104365, 78979, 24495, 76857, 21836, 32118, 120805, 22812, 127367, 22987, 144369, 20141, 82964, 64053, 18686, 57934, 62840, 1706, 18131, 98026, 125853, 115205, 95707, 118435, 10887, 40668, 109214, 85178, 111501, 22784, 69100, 140580, 90076) '
        f'limit {n}'
    )

    df_snapowane_dane = snapowanie_budynkow_do_sieci_drogowej(
        rozpakowuje_dane_z_bazy_danych(
            cursor.fetchall()
        )
    )

    # wybieram losowo k punktów na centroidy do pierwszej iteracji (oznacza to że będzie k grup)
    np.random.seed(55)
    centroids = np.random.choice(len(df_snapowane_dane.index_snap), k, replace=False)  # indeksy centroidów z danych po snapie

    ID_centroidow_wezlow_sieci_drogowej_po_snapie = [df_snapowane_dane.index_snap[item] for item in
                                                     centroids]  # id centroidow
    print('\n\n**************************************\n Dane po snapie', '\n**************************************\n', df_snapowane_dane.to_string())
    print(
        '\n\n**************************************\n Wylosowane centroidy do pierwszej iteracji idx_snap: \n************************************\n',
        ID_centroidow_wezlow_sieci_drogowej_po_snapie)

    # przeprowadzam klasyfikacje na df
    klasyfikacja = np.array(
        [np.argmin(i) for i in [[my_func(centroid, item) for centroid in ID_centroidow_wezlow_sieci_drogowej_po_snapie]
                                for item in df_snapowane_dane.index_snap]])
    print("\n**************************************\n"
          "klasyfikacja '0'",
          '\n**************************************\n', klasyfikacja)

    df_snapowane_dane['klasyfikacja'] = klasyfikacja

    print("\n\n**************************************\n"
          "df_snapowane_dane+ klasyfikacja '0'",
          '\n**************************************')
    print(df_snapowane_dane.to_string())

    list_of_df = [df_snapowane_dane]

    ######################################################################################################
    ####################################NOWE CENTROIDY
    for numer in range(no_of_iterations):
        print(f'\n################### ITERACJA {numer} #################################')
        tmp = list_of_df[numer]

        df_nowe_centroidy_loop = pd.DataFrame([
            list_of_df[numer].groupby('klasyfikacja')['Y_snap'].mean(),
            list_of_df[numer].groupby('klasyfikacja')['X_snap'].mean()
        ]).T
        print("\n\n**************************************\n"
              "nowe centroidy DF",
              '\n**************************************')
        # Snapowanie centroidow wspolrzednych do siatki drogowej
        df_nowe_centroidy_loop = snapowanie_centroidow_do_sieci_drogowej(df_nowe_centroidy_loop)
        print('\n nowe centroidy po snapie\n', df_nowe_centroidy_loop.to_string())

        # OBLICZAM Odległości
        klasyfikacja_loop = np.array(
            [np.argmin(i) for i in [[my_func(centroid, item) for centroid in df_nowe_centroidy_loop.index_snap]
                                    for item in df_snapowane_dane.index_snap]])
        tmp['klasyfikacja'] = klasyfikacja_loop

        print('\n', klasyfikacja_loop)
        list_of_df.append(tmp)

except(Exception, psycopg2.Error) as error:
    print("Próba połączenia zakończona niepowodzeniem", error)
finally:
    # zamkniecie nawiazanego połączenia,
    if (connection):
        cursor.close()
        connection.close()
        print("Zakończono połączenie")
