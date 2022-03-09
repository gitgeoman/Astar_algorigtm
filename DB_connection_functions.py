def query_tekst(source, target):
    postgreSQL_select_Query = f"SELECT MIN(r.seq) AS seq, " \
                              f"e.old_id AS id, " \
                              f"sum(e.distance) AS distance, " \
                              f"ST_Collect(e.the_geom) AS geom " \
                              f"FROM pgr_dijkstra('SELECT id, source, target, distance as cost FROM public.\"00DrogiINTER_noded\"', {source}, {target}, false ) AS r, " \
                              f"public.\"00DrogiINTER_noded\" AS e " \
                              f"WHERE r.edge=e.id " \
                              f"GROUP BY e.old_id"
    # print(postgreSQL_select_Query)
    return postgreSQL_select_Query


def sum_length_from_scratch(tablica):
    # print(tablica)
    dlugosc_drogi = 0
    for row in tablica:
        dlugosc_drogi = dlugosc_drogi + float(row[2])
    return dlugosc_drogi
