import re

def validar_numero_telefono(numero):
    """ Valida si un número de teléfono argentino es correcto """
    patron = re.compile(r'^(?:\+54|0)?(?:11|[2368]\d)\d{8}$')
    return patron.match(numero) is not None

def contar_registros(archivo_ruta):
    """ Cuenta la cantidad de registros en un archivo CSV """
    with open(archivo_ruta, newline='', encoding='utf-8') as archivo:
        return sum(1 for _ in archivo)

def extraer_prefijos(numeros):
    """ Extrae los prefijos de una lista de números """
    prefijos = [numero[:2] for numero in numeros]
    return prefijos

