# Registros No Llame

Este proyecto es una herramienta para gestionar y analizar números de teléfono en relación con el Registro Nacional de "No Llamar" en Argentina. Permite verificar si los números de teléfono están registrados para no recibir llamadas promocionales y proporciona varias funcionalidades adicionales como importar números, generar gráficos y mantener un historial de búsquedas.

## Características

- **Búsqueda de Números**: Verifica si los números de teléfono están en el Registro Nacional de "No Llamar".
- **Importar Números**: Permite importar números de teléfono desde un archivo de texto o CSV.
- **Mostrar Resultados**: Muestra los resultados de la búsqueda, incluyendo números encontrados, no encontrados y no verificados.
- **Gráficos**: Genera gráficos que muestran la proporción de números encontrados, no encontrados y no verificados.
- **Historial de Búsquedas**: Guarda y muestra un historial de todas las búsquedas realizadas.
- **Información del Archivo**: Proporciona estadísticas sobre el archivo del Registro "No Llamar", como la cantidad total de registros.

## Requisitos del Sistema

- **Sistema Operativo**: Windows
- **Python**: Python 3.6 o superior (para desarrollo, no necesario para el uso del ejecutable)
- **Bibliotecas de Python**: PySimpleGUI, pyperclip, matplotlib

## Instalación

### Para Usuarios Finales (sin Python)

Si no tienes Python instalado y solo necesitas el ejecutable, puedes descargar el archivo ejecutable desde la carpeta `dist` una vez generado. No se requieren pasos de instalación adicionales.

### Para Desarrolladores

Si deseas modificar o ejecutar el código fuente, sigue estos pasos:

1. **Clonar el Repositorio**

   ```bash
   git clone https://github.com/germanschauvinhold/RegistrosNoLlame.git


Estructura del Proyecto
El proyecto está organizado de la siguiente manera:

RegistrosNoLlames/
│
├── src/
│   ├── main.py              # Archivo principal del programa
│   ├── utils.py             # Funciones de utilidad
│   ├── data_processing.py   # Lógica de procesamiento de datos
│   └── ui.py                # Interfaz de usuario
│
├── data/                    # Archivos de datos, como el CSV del Registro "No Llamar"
│
├── docs/
│   └── README.md            # Este archivo
│
├── output/                  # Salidas del programa, como el historial de búsquedas
│
└── images/
    └── lupa.ico             # Icono utilizado en el programa

Contribución
Las contribuciones son bienvenidas. Por favor, sigue estos pasos para contribuir:

Realiza un fork del proyecto.
Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
Realiza tus cambios y haz commit (git commit -m 'Añadir nueva funcionalidad').
Empuja tu rama (git push origin feature/nueva-funcionalidad).
Abre un Pull Request.
Licencia
Este proyecto está bajo la Licencia MIT