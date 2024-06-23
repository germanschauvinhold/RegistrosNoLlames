import PySimpleGUI as sg
import pyperclip
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

# Base path to the current script directory
base_path = Path.home() / "Documents" / "RegistrosNoLlames"

# Asegurarse de que la carpeta root exista
base_path.mkdir(parents=True, exist_ok=True)

# Ruta del ícono personalizado (relativa a la base path)
icono_ruta = base_path / "images" / "lupa.ico"

# Ruta de historial en la carpeta "Documents/RegistrosNoLlames"
historial_ruta = Path.home() / "Documents" / "RegistrosNoLlames" / "output" / "historial_busquedas.txt"

# Asegurarse de que la carpeta de historial existe
historial_ruta.parent.mkdir(parents=True, exist_ok=True)

def mostrar_grafico(coincidencias, no_encontrados, no_verificados):
    fig, ax = plt.subplots()
    etiquetas = ['Encontrados', 'No Encontrados', 'No Verificados']
    cantidades = [len(coincidencias), len(no_encontrados), len(no_verificados)]
    
    ax.pie(cantidades, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF5722', '#FFC107'])
    ax.axis('equal')
    plt.title('Proporción de Números Encontrados, No Encontrados y No Verificados')
    plt.show()

def mostrar_historial(historial_ruta):
    if not historial_ruta.exists():
        sg.popup("No hay historial disponible.", icon=icono_ruta)
        return
    with open(historial_ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()
    sg.popup_scrolled(contenido, title="Historial de Búsquedas", icon=icono_ruta)

def guardar_resultado(resultado):
    ruta_guardar = sg.popup_get_file('Guardar como', save_as=True, file_types=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if ruta_guardar:
        with open(ruta_guardar, 'w', encoding='utf-8') as f:
            f.write(resultado)
        sg.popup('Los resultados han sido guardados en el archivo.')

def copiar_al_portapapeles(texto):
    pyperclip.copy(texto)
    sg.popup('Los resultados han sido copiados al portapapeles.')

def guardar_historial(busqueda, coincidencias, no_encontrados, no_verificados):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(historial_ruta, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp}\n")
        f.write(f"Búsqueda: {', '.join(busqueda)}\n")
        f.write(f"Encontrados: {', '.join(coincidencias)}\n")
        f.write(f"No Encontrados: {', '.join(no_encontrados)}\n")
        f.write(f"No Verificados: {', '.join(no_verificados)}\n\n")

