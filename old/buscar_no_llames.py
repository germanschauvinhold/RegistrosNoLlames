import csv
import os
import re
import PySimpleGUI as sg

# Ruta del ícono personalizado
icono_ruta = "c:/Users/EmaNot/Documents/RegistrosNoLlames/lupa.ico"  # Asegúrate de que esta ruta sea correcta y que el archivo exista

def validar_numero_telefono(numero):
    # Regex para validar números de teléfono argentinos
    patron = re.compile(r'^(?:\+54|0)?(?:11|[2368]\d)\d{8}$')
    return patron.match(numero) is not None

def buscar_telefono_en_registro(numeros_buscar, ruta_archivo_registro):
    coincidencias = []
    with open(ruta_archivo_registro, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for linea in lector:
            if linea[0] in numeros_buscar:
                coincidencias.append(linea[0])
    return coincidencias

def seleccionar_archivo():
    sg.theme('DarkBlue3')
    layout = [
        [sg.Text('Seleccione el archivo CSV del Registro No Llame')],
        [sg.Input(key='ruta_archivo'), sg.FileBrowse()],
        [sg.OK(), sg.Cancel()]
    ]
    window = sg.Window('Seleccionar archivo', layout, icon=icono_ruta)  # Añadir ícono

    event, values = window.read()
    window.close()

    if event == 'OK':
        ruta_archivo = values['ruta_archivo']
        print(f"Archivo seleccionado: {ruta_archivo}")  # Mensaje de depuración
        return ruta_archivo
    return None

def main():
    # Solicitar al usuario que seleccione el archivo de registro
    ruta_archivo_registro = seleccionar_archivo()
    if not ruta_archivo_registro or not os.path.isfile(ruta_archivo_registro):
        sg.popup('Debe seleccionar un archivo de registro válido.', icon=icono_ruta)
        return
    
    # Solicitar al usuario que ingrese los números a buscar
    layout = [
        [sg.Text('Ingrese los números de teléfono a buscar (mínimo 10), separados por comas o saltos de línea')],
        [sg.Multiline(key='numeros_telefonos', size=(50, 10))],
        [sg.OK(), sg.Cancel()]
    ]
    window = sg.Window('Buscar Teléfonos en Registro No Llame', layout, icon=icono_ruta)  # Añadir ícono

    event, values = window.read()
    window.close()

    if event == 'OK':
        # Separar números por comas o saltos de línea y validar
        numeros_telefonos = re.split(r',|\n', values['numeros_telefonos'])
        numeros_telefonos = [num.strip() for num in numeros_telefonos if validar_numero_telefono(num.strip())]

        if len(numeros_telefonos) < 10:
            sg.popup('Debe ingresar al menos 10 números válidos.', icon=icono_ruta)
            return
        
        # Buscar los números en el archivo de registro
        coincidencias = buscar_telefono_en_registro(numeros_telefonos, ruta_archivo_registro)

        if coincidencias:
            sg.popup(f'Se encontraron los siguientes números en el registro: {", ".join(coincidencias)}', icon=icono_ruta)
        else:
            sg.popup('No se encontraron coincidencias en el registro.', icon=icono_ruta)
    else:
        sg.popup('Operación cancelada.', icon=icono_ruta)

if __name__ == '__main__':
    main()