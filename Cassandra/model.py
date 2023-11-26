#!/usr/bin/env python3
import logging
import calendar
from rich.console import Console

console = Console()

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_FLIGHTSINFO_TABLE = """
CREATE TABLE IF NOT EXISTS infovuelos (
    aerolinea text,
    ubicacion_origen text,
    ubicacion_destino text,
    dia int,
    mes int,
    anio int,
    conexion text,
    edad int,
    genero text,
    razon text,
    estancia text,
    transporte text,
    PRIMARY KEY ((conexion,razon),edad)
);
"""
# Crear índices secundarios
CREATE_INDEX_ON_EDAD = """
CREATE INDEX IF NOT EXISTS edad_index ON infovuelos (edad);
"""
CREATE_INDEX_ON_RAZON = """
CREATE INDEX IF NOT EXISTS razon_index ON infovuelos (razon);
"""
CREATE_INDEX_ON_CONEXION = """
CREATE INDEX IF NOT EXISTS conexion_index ON infovuelos (conexion);
"""

###estructura de querys
SELECT_USUARIOS_MAYORES = """
SELECT COUNT(*) AS MayoresEdad FROM infovuelos WHERE edad >= 18 ALLOW FILTERING;
"""
###funciona con la confi actual
SELECT_USUARIOS = """
SELECT COUNT(*) AS TotalUsuarios FROM infovuelos;
"""
###Necesita el allow filtering ya que son 2 predicados
SELECT_OBTENER_VUELOS_UTILES = """
SELECT * FROM infovuelos WHERE edad >= 18 AND razon = 'Vacaciones/placer' ALLOW FILTERING;
"""

###funciona con la confi actual
SELECT_AEROPUERTOS_NO_CONEXION="""
SELECT COUNT(*) as aeropuertosnoconexion FROM infovuelos WHERE conexion='No es de conexion';
"""

###funciona con la confi actual
SELECT_CANTIDAD_VUELOS="""
SELECT COUNT(*) as aeropuertostotales FROM infovuelos;
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_FLIGHTSINFO_TABLE)

def cantidadAdultosEnVuelos(session):
    log.info("MOSTRANDO TODOS LOS ADULTOS EN VUELOS")
    stmt = session.prepare(SELECT_USUARIOS_MAYORES)
    result = session.execute(stmt) 
    numeroDeMayores = result.one().mayoresedad
    ###necesitamos saber la cantidad de usuarios
    stmt2 = session.prepare(SELECT_USUARIOS)
    result2 = session.execute(stmt2)
    numeroDeUsuarios = result2.one().totalusuarios
    porcentaje = (numeroDeMayores*100)/numeroDeUsuarios
    print("\n")
    print("|----------------------------------------------------------------------------------|")
    console.print(f"TOTAL DE PERSONAS MAYORES QUE TOMARON VUELOS DURANTE EL AÑO: [bold]{numeroDeMayores}[/bold]")
    console.print(f"% PORCENTAJE DE USUARIOS MAYORES DE EDAD QUE TOMARON VUELOS DURANTE EL AÑO: [bold]{round(porcentaje,2)}%[/bold]")
    print("|----------------------------------------------------------------------------------|")

def cantidadAeropuertosNoConexion(session):
    log.info("Informacion de los aeropuertos que no son conexion")
    stmt = session.prepare(SELECT_AEROPUERTOS_NO_CONEXION)
    result = session.execute(stmt)
    cantidad = result.one().aeropuertosnoconexion
    ###ahora necesitamos sacar el porcentaje de los vuelos
    stmt2 = session.prepare(SELECT_CANTIDAD_VUELOS)
    resultado2 = session.execute(stmt2)
    vuelostotales = resultado2.one().aeropuertostotales
    porcentaje = (cantidad*100)/vuelostotales
    print("\n")
    console.print("|----------------------------------------------------------------------------------|")
    console.print(f"CANTIDAD DE VUELOS QUE LLEGARON A UN AEROPUERTO DE NO CONEXION: [bold]{cantidad}[/bold]")
    console.print(f"CANTIDAD EN PORCENTAJE: [bold]{round(porcentaje,2)}%[/bold]")
    print("|----------------------------------------------------------------------------------|")

def mejoresMesesAbrirRestaurantes(session):
    log.info("Obteniendo mejores meses para abrir restaurantes")
    stmt = session.prepare(SELECT_OBTENER_VUELOS_UTILES)
    result = session.execute(stmt)
    diccionario = {
    1: 0,  # enero
    2: 0,  # febrero
    3: 0,  # marzo
    4: 0,  # abril
    5: 0,  # mayo
    6: 0,  # junio
    7: 0,  # julio
    8: 0,  # agosto
    9: 0,  # septiembre
    10: 0,  # octubre
    11: 0,  # noviembre
    12: 0  # diciembre
}

    # Iteramos sobre el resultado y actualizamos el diccionario
    for row in result:
        if row.mes in diccionario:
            diccionario[row.mes] += 1

    ##iteramos por el diccionario para saber el mes que mas se repite
    maximo = -1
    mejormes = ""
    for item in diccionario:
        if diccionario[item] >= maximo:
            maximo = diccionario[item]
            mejormes = item

    ###obtenemos el nombre del mes
    mesnombre = _obtener_nombre_mes(mejormes)
    ###imprimimos el resultado
    console.log(f"Mes recomendado para abrir restaurantes: [bold]{mesnombre}[/bold]")
    console.log(f"Cantidad de vuelos en ese mes: [bold]{maximo}[/bold]")

def _obtener_nombre_mes(numero_mes):
    try:
        nombre_mes = calendar.month_name[numero_mes]
        return nombre_mes
    except IndexError:
        return "Mes inválido"