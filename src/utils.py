import re
import PySimpleGUI as sg

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

def importar_numeros_desde_archivo():
    ruta_archivo = sg.popup_get_file('Seleccione el archivo de números', file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")), icon=icono_ruta)
    if ruta_archivo:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        numeros = re.split(r',|\n', contenido)
        numeros = [num.strip() for num in numeros if validar_numero_telefono(num.strip())]
        return numeros
    return []