# nawiąż połączenie
import psycopg2
from funkcje_do_bazy_danych import *
from conn_data import user, password, host, port, database

import numpy as np

#dane wejsciowe
#x=punkty wspolrzedne a,b
#k = liczba klas

try:
    connection = psycopg2.connect(user=user,password= password, host=host, port=port, database=database)
    cursor = connection.cursor()

    # wywołaj funkcje obliczenia odległości
    lista = [[1441, 1500]]
    # ten kawałek w pętli
    for item in lista:
        cursor.execute(query_tekst(item[0], item[1]))
        print(obliczanie_odleglosci(cursor.fetchall()))























except(Exception, psycopg2.Error) as error:
    print ("Próba połączenia zakończona niepowodzeniem", error)
finally:
    #zamkniecie nawiazanego połączenia.
        if(connection):
            cursor.close()
            connection.close()
            print("Zakończono połączenie")

