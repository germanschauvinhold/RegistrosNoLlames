import csv
import re
import PySimpleGUI as sg
from utils import validar_numero_telefono
from pathlib import Path

# Base path to the current script directory
base_path = Path.home() / "Documents" / "RegistrosNoLlames"

# Asegurarse de que la carpeta root exista
base_path.mkdir(parents=True, exist_ok=True)

# Ruta del ícono personalizado (relativa a la base path)
icono_ruta = base_path / "images" / "lupa.ico"

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

def importar_numeros_desde_archivo():
    ruta_archivo = sg.popup_get_file('Seleccione el archivo de números', file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")), icon=icono_ruta)
    if ruta_archivo:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        numeros = re.split(r',|\n', contenido)
        numeros = [num.strip() for num in numeros if validar_numero_telefono(num.strip())]
        return numeros
    return []