import pandas as pd
import re
import PySimpleGUIQt as sg  # Cambiamos a PySimpleGUIQt para usar PyQt5

# Función para validar números de teléfono argentinos
def es_telefono_valido(numero):
    patron = re.compile(r'^(\+54|0)?(9)?(11|[2-9]\d)\d{7,8}$')
    return patron.match(numero) is not None

# Crear el diseño de la ventana
layout = [
    [sg.Text("Seleccione el archivo de registros 'No llame':"), sg.Input(), sg.FileBrowse(key="-FILE-")],
    [sg.Text("Ingrese un número de teléfono argentino para buscar:"), sg.InputText(key="-NUMERO-")],
    [sg.Button("Buscar"), sg.Button("Salir")]
]

# Crear la ventana
window = sg.Window("Búsqueda en Registro 'No llame'", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Salir":
        break
    if event == "Buscar":
        archivo_csv = values["-FILE-"]
        numero = values["-NUMERO-"]

        if not archivo_csv:
            sg.popup("Por favor, seleccione un archivo.")
        elif not numero:
            sg.popup("Por favor, ingrese un número de teléfono.")
        elif not es_telefono_valido(numero):
            sg.popup(f"El número {numero} no es válido.")
        else:
            try:
                # Leer el archivo CSV (sin nombres de columnas, usaremos índices)
                lista_no_llame = pd.read_csv(archivo_csv, chunksize=100000, header=None, usecols=[0])
                encontrado = False

                # Buscar el número en cada fragmento del archivo
                for chunk in lista_no_llame:
                    if any(chunk[0].astype(str).str.contains(numero)):
                        encontrado = True
                        break

                if encontrado:
                    sg.popup(f"El número {numero} está en la lista 'No llame'.")
                else:
                    sg.popup(f"El número {numero} no está en la lista 'No llame'.")
            except FileNotFoundError:
                sg.popup(f"El archivo {archivo_csv} no fue encontrado. Verifica la ruta y el nombre del archivo.")
            except Exception as e:
                sg.popup(f"Ocurrió un error al procesar el archivo: {e}")

window.close()
