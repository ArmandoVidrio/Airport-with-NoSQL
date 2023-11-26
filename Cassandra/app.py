#!/usr/bin/env python3
import logging
import os
import random
import model

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('investments.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'investments')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

def print_menu():
    print('\n')
    mm_options = {
        1: "Mostrar porcentaje de personas adultas que toman vuelos",
        2: "Mostrar cantidad de vuelos que llegaron a un aeropuerto de no conexion",
        3: "Mostrar los mejores meses para abrir restaurantes",
        4: "Salir"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])


def get_instrument_value(instrument):
    instr_mock_sum = sum(bytearray(instrument, encoding='utf-8'))
    return random.uniform(1.0, instr_mock_sum)


def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)


    while(True):
        print_menu()
        option = int(input('Ingresa tu opcion: '))
        if option == 1: ###mostrar % de personas que toman vuelos +18
            model.cantidadAdultosEnVuelos(session)
        if option == 2: ###mostrar los aeropuertos de los vuelos que no son conexion
            model.cantidadAeropuertosNoConexion(session)
        if option == 3: ###mostrar vuelos donde la estancia sea diferente a casa
            model.mejoresMesesAbrirRestaurantes(session)
        if option == 4:
            print("ADIOS AMIGOS")
            exit(0)

if __name__ == '__main__':
    main()