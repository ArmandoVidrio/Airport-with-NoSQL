# EN ESTE ARCHIVO POBLAREMOS TODA NUESTRA BASE DE DATOS

import datetime
from random import choice, randint, randrange

CQL_FILE = 'data.cql'

aerolineas = ["Aeroméxico", "Volaris", "Interjet", "Aeromar", "VivaAerobus"]

generos = ["Hombre","Mujer","Prefiero no decirlo"]

razones = ["Vacaciones/placer", "Trabajo", "Vuelta a casa"]

estancias = ["Hotel", "Casa", "Amigos"]

transportes = ["Taxi del aeropuerto", "Renta de autos", "Transporte público", "Recogida", "Auto propio"]

aeropuertos = ["PDX", "GDL", "SJC", "LAX", "JFK"]

conexiones = ["No es de conexion","Es de conexion"]

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date

def generadorPrincipal(cantidad=1000):
    infovuelo_stmt = "INSERT INTO infovuelos(aerolinea, ubicacion_origen, ubicacion_destino, dia, mes, anio, conexion,edad,genero,razon,estancia,transporte) VALUES('{}','{}','{}',{},{},{},'{}',{},'{}','{}','{}','{}');"

    for i in range(cantidad):
        ### insertamos la info en el CQL
        with open(CQL_FILE, "a") as fd:  # cambiar "w" a "a"
            ### creamos la informacion de los vuelos
            aerolinea = choice(aerolineas)
            ubicacion_origen = choice(aeropuertos)
            ubicacion_destino = choice(aeropuertos)
            while ubicacion_destino == ubicacion_origen:
                ubicacion_destino = choice(aeropuertos)
            ### creamos una fecha al azar
            fecharandom = random_date(datetime.datetime(2018, 1, 1), datetime.datetime(2023, 11, 24))
            dia = fecharandom.day
            mes = fecharandom.month
            anio = fecharandom.year
            conexion = choice(conexiones)
            edad = randint(12, 80)
            genero = choice(generos)
            razon = choice(razones)
            estancia = choice(estancias)
            transporte = choice(transportes)

            ### actualizamos el statement
            fd.write(infovuelo_stmt.format(aerolinea, ubicacion_origen, ubicacion_destino, dia, mes, anio, conexion,edad,genero,razon,estancia,transporte) + '\n')

if __name__ == "__main__":
    generadorPrincipal()
