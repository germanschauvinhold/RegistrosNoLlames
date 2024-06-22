import PySimpleGUI as sg
from pathlib import Path
from utils import contar_registros, importar_numeros_desde_archivo, extraer_prefijos
from data_processing import buscar_telefono_en_registro, extraer_estadisticas
from ui import mostrar_grafico, mostrar_historial, guardar_resultado, copiar_al_portapapeles
from datetime import datetime

# Ruta del ícono personalizado
icono_ruta = "C:/Users/EmaNot/Documents/RegistrosNoLlames/images/lupa.ico"
# Ruta predeterminada para el historial de búsquedas
historial_ruta = Path("C:/Users/EmaNot/Documents/RegistrosNoLlames/output/historial_busquedas.txt")

def seleccionar_archivo():
    sg.theme('DarkBlue3')
    layout = [
        [sg.Text('Seleccione el archivo CSV del Registro No Llame')],
        [sg.Input(key='ruta_archivo'), sg.FileBrowse(initial_folder="C:/Users/EmaNot/Documents/RegistrosNoLlames/data")],
        [sg.OK(), sg.Cancel()]
    ]
    window = sg.Window('Seleccionar archivo', layout, icon=icono_ruta)

    event, values = window.read()
    window.close()

    if event == 'OK':
        ruta_archivo = values['ruta_archivo']
        if ruta_archivo and Path(ruta_archivo).is_file():
            total_registros = contar_registros(ruta_archivo)
            sg.popup(f"Archivo seleccionado: {ruta_archivo}\nTotal de registros en el archivo: {total_registros}", icon=icono_ruta)
        return ruta_archivo
    return None

def main():
    ruta_archivo_registro = seleccionar_archivo()
    if not ruta_archivo_registro or not Path(ruta_archivo_registro).is_file():
        sg.popup('Debe seleccionar un archivo de registro válido.', icon=icono_ruta)
        return
    
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
            numeros_telefonos = [num.strip() for num in numeros_telefonos]

            if len(numeros_telefonos) < 10:
                sg.popup('Debe ingresar al menos 10 números válidos.', icon=icono_ruta)
                continue

            coincidencias, no_encontrados, no_verificados = buscar_telefono_en_registro(numeros_telefonos, ruta_archivo_registro)

            if coincidencias or no_encontrados or no_verificados:
                resultado = f"Números Encontrados: {', '.join(coincidencias)}\nNúmeros No Encontrados: {', '.join(no_encontrados)}\nNúmeros No Verificados: {', '.join(no_verificados)}"
                layout_resultado = [
                    [sg.Text(resultado)],
                    [sg.Button('Copiar al portapapeles'), sg.Button('Guardar en archivo'), sg.Button('Mostrar Gráfico'), sg.OK()]
                ]
                window_resultado = sg.Window('Resultados de Búsqueda', layout_resultado, icon=icono_ruta)
                event_resultado, _ = window_resultado.read()

                if event_resultado == 'Copiar al portapapeles':
                    copiar_al_portapapeles(resultado)
                elif event_resultado == 'Guardar en archivo':
                    guardar_resultado(resultado)
                elif event_resultado == 'Mostrar Gráfico':
                    mostrar_grafico(coincidencias, no_encontrados, no_verificados)
                window_resultado.close()

                # Guardar en el historial
                guardar_historial(numeros_telefonos, coincidencias, no_encontrados, no_verificados)
            else:
                sg.popup('No se encontraron coincidencias en el registro.', icon=icono_ruta)
        elif event == 'Importar números desde archivo':
            numeros_importados = importar_numeros_desde_archivo()
            if numeros_importados:
                sg.popup('Números importados correctamente.', icon=icono_ruta)
            window.close()
        elif event == 'Mostrar Historial':
            mostrar_historial(historial_ruta)
            # Mantener la ventana principal abierta después de mostrar el historial

if __name__ == '__main__':
    main()
