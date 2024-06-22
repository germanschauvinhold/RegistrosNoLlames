import csv
import os
import re
import PySimpleGUI as sg
import pyperclip
from datetime import datetime

# Ruta del ícono personalizado
icono_ruta = "c:/Users/EmaNot/Documents/RegistrosNoLlames/lupa.ico"
historial_archivo = "c:/Users/EmaNot/Documents/RegistrosNoLlames/historial_busquedas.txt"

def validar_numero_telefono(numero):
    # Regex para validar números de teléfono argentinos
    patron = re.compile(r'^(?:\+54|0)?(?:11|[2368]\d)\d{8}$')
    return patron.match(numero) is not None

def buscar_telefono_en_registro(numeros_buscar, ruta_archivo_registro):
    coincidencias = []
    no_encontrados = []
    with open(ruta_archivo_registro, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        registro_numeros = {linea[0] for linea in lector}
        for numero in numeros_buscar:
            if numero in registro_numeros:
                coincidencias.append(numero)
            else:
                no_encontrados.append(numero)
    return coincidencias, no_encontrados

def seleccionar_archivo():
    sg.theme('DarkBlue3')
    layout = [
        [sg.Text('Seleccione el archivo CSV del Registro No Llame')],
        [sg.Input(key='ruta_archivo'), sg.FileBrowse()],
        [sg.OK(), sg.Cancel()]
    ]
    window = sg.Window('Seleccionar archivo', layout, icon=icono_ruta)

    event, values = window.read()
    window.close()

    if event == 'OK':
        ruta_archivo = values['ruta_archivo']
        print(f"Archivo seleccionado: {ruta_archivo}")
        return ruta_archivo
    return None

def guardar_historial(busqueda, coincidencias, no_encontrados):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(historial_archivo, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp}\n")
        f.write(f"Búsqueda: {', '.join(busqueda)}\n")
        f.write(f"Encontrados: {', '.join(coincidencias)}\n")
        f.write(f"No Encontrados: {', '.join(no_encontrados)}\n\n")

def mostrar_historial():
    if not os.path.exists(historial_archivo):
        sg.popup("No hay historial disponible.", icon=icono_ruta)
        return
    with open(historial_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    sg.popup_scrolled(contenido, title="Historial de Búsquedas", icon=icono_ruta)

def importar_numeros_desde_archivo():
    ruta_archivo = sg.popup_get_file('Seleccione el archivo de números', file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")), icon=icono_ruta)
    if ruta_archivo:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        numeros = re.split(r',|\n', contenido)
        numeros = [num.strip() for num in numeros if validar_numero_telefono(num.strip())]
        return numeros
    return []

def main():
    ruta_archivo_registro = seleccionar_archivo()
    if not ruta_archivo_registro or not os.path.isfile(ruta_archivo_registro):
        sg.popup('Debe seleccionar un archivo de registro válido.', icon=icono_ruta)
        return
    
    # Inicializar la lista de números importados
    numeros_importados = []

    while True:
        layout = [
            [sg.Text('Ingrese los números de teléfono a buscar (mínimo 10), separados por comas o saltos de línea')],
            [sg.Multiline(key='numeros_telefonos', size=(50, 10), default_text=", ".join(numeros_importados))],
            [sg.Button('Importar números desde archivo')],
            [sg.OK(), sg.Cancel(), sg.Button('Mostrar Historial')]
        ]
        window = sg.Window('Buscar Teléfonos en Registro No Llame', layout, icon=icono_ruta)

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break
        elif event == 'OK':
            numeros_telefonos = re.split(r',|\n', values['numeros_telefonos'])
            numeros_telefonos = [num.strip() for num in numeros_telefonos if validar_numero_telefono(num.strip())]

            if len(numeros_telefonos) < 10:
                sg.popup('Debe ingresar al menos 10 números válidos.', icon=icono_ruta)
                continue

            coincidencias, no_encontrados = buscar_telefono_en_registro(numeros_telefonos, ruta_archivo_registro)

            if coincidencias or no_encontrados:
                resultado = f"Números Encontrados: {', '.join(coincidencias)}\nNúmeros No Encontrados: {', '.join(no_encontrados)}"
                layout_resultado = [
                    [sg.Text(resultado)],
                    [sg.Button('Copiar al portapapeles'), sg.Button('Guardar en archivo'), sg.OK()]
                ]
                window_resultado = sg.Window('Resultados de Búsqueda', layout_resultado, icon=icono_ruta)
                event_resultado, _ = window_resultado.read()

                if event_resultado == 'Copiar al portapapeles':
                    pyperclip.copy(resultado)
                    sg.popup('Los resultados han sido copiados al portapapeles.', icon=icono_ruta)
                elif event_resultado == 'Guardar en archivo':
                    ruta_guardar = sg.popup_get_file('Guardar como', save_as=True, file_types=(("Text Files", "*.txt"), ("All Files", "*.*")), icon=icono_ruta)
                    if ruta_guardar:
                        with open(ruta_guardar, 'w', encoding='utf-8') as f:
                            f.write(resultado)
                        sg.popup('Los resultados han sido guardados en el archivo.', icon=icono_ruta)
                window_resultado.close()

                # Guardar en el historial
                guardar_historial(numeros_telefonos, coincidencias, no_encontrados)
            else:
                sg.popup('No se encontraron coincidencias en el registro.', icon=icono_ruta)
        elif event == 'Importar números desde archivo':
            numeros_importados = importar_numeros_desde_archivo()
            if numeros_importados:
                sg.popup('Números importados correctamente.', icon=icono_ruta)
            window.close()
        elif event == 'Mostrar Historial':
            mostrar_historial()
            # Mantener la ventana principal abierta después de mostrar el historial

if __name__ == '__main__':
    main()
