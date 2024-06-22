import csv
import os
import re
import PySimpleGUI as sg

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
    window = sg.Window('Seleccionar archivo', layout)

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
        sg.popup('Debe seleccionar un archivo de registro válido.')
        return
    
    # Solicitar al usuario que ingrese los números a buscar
    layout = [
        [sg.Text('Ingrese los números de teléfono a buscar, separados por comas')],
        [sg.InputText(key='numeros_telefonos')],
        [sg.OK(), sg.Cancel()]
    ]
    window = sg.Window('Buscar Teléfonos en Registro No Llame', layout)

    event, values = window.read()
    window.close()

    if event == 'OK':
        numeros_telefonos = values['numeros_telefonos'].split(',')
        numeros_telefonos = [num.strip() for num in numeros_telefonos if validar_numero_telefono(num.strip())]

        if not numeros_telefonos:
            sg.popup('No se han ingresado números válidos.')
            return
        
        # Buscar los números en el archivo de registro
        coincidencias = buscar_telefono_en_registro(numeros_telefonos, ruta_archivo_registro)

        if coincidencias:
            sg.popup(f'Se encontraron los siguientes números en el registro: {", ".join(coincidencias)}')
        else:
            sg.popup('No se encontraron coincidencias en el registro.')
    else:
        sg.popup('Operación cancelada.')

if __name__ == '__main__':
    main()
