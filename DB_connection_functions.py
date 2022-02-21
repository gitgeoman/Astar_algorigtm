def query_tekst(source, target):
    postgreSQL_select_Query = f"SELECT MIN(r.seq) AS seq, " \
                              f"e.old_id AS id, " \
                              f"e.name, " \
                              f"e.type, " \
                              f"sum(e.distance) AS distance, " \
                              f"ST_Collect(e.the_geom) AS geom " \
                              f"FROM pgr_dijkstra('SELECT id, source, target, distance as cost FROM public.\"lineEdges_noded\"', {source}, {target}, false ) AS r, " \
                              f"public.\"lineEdges_noded\" AS e " \
                              f"WHERE r.edge=e.id " \
                              f"GROUP BY e.old_id, e.name, e.type"
    # print(postgreSQL_select_Query)
    return postgreSQL_select_Query


def sum_length_from_scratch(tablica):
    dlugosc_drogi = 0
    for row in tablica:
        dlugosc_drogi = dlugosc_drogi + float(row[4])
    return dlugosc_drogi
