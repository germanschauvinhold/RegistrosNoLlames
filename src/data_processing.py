import csv
from utils import validar_numero_telefono

def buscar_telefono_en_registro(numeros_buscar, ruta_archivo_registro):
    coincidencias = []
    no_encontrados = []
    no_verificados = []
    with open(ruta_archivo_registro, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        registro_numeros = {linea[0] for linea in lector}
        for numero in numeros_buscar:
            if not validar_numero_telefono(numero):
                no_verificados.append(numero)
            elif numero in registro_numeros:
                coincidencias.append(numero)
            else:
                no_encontrados.append(numero)
    return coincidencias, no_encontrados, no_verificados

def extraer_estadisticas(archivo_ruta):
    """ Extrae estadísticas del archivo de registros """
    prefijos = {}
    with open(archivo_ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for linea in lector:
            prefijo = linea[0][:2]
            if prefijo in prefijos:
                prefijos[prefijo] += 1
            else:
                prefijos[prefijo] = 1
    return prefijos
