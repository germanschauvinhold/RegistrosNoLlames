import PySimpleGUI as sg
import pyperclip
import matplotlib.pyplot as plt

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
        sg.popup("No hay historial disponible.")
        return
    with open(historial_ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()
    sg.popup_scrolled(contenido, title="Historial de Búsquedas")

def guardar_resultado(resultado):
    ruta_guardar = sg.popup_get_file('Guardar como', save_as=True, file_types=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if ruta_guardar:
        with open(ruta_guardar, 'w', encoding='utf-8') as f:
            f.write(resultado)
        sg.popup('Los resultados han sido guardados en el archivo.')

def copiar_al_portapapeles(texto):
    pyperclip.copy(texto)
    sg.popup('Los resultados han sido copiados al portapapeles.')
