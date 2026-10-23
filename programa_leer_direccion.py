# Programa para leer datos desde un archivo JSON y convertirlos en un diccionario.
# Se importa el modulo json para poder trabajar con archivos en formato JSON.
import json


# Esta funcion recibe la ruta de un archivo JSON, lee su contenido
# y convierte los datos obtenidos en un diccionario usando el comando dict.
def leer_dirección(ruta_archivo):
    # El bloque try intenta abrir y leer el archivo JSON indicado.
    try:
        # Se abre el archivo en modo lectura con codificacion UTF-8.
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            # Se cargan los datos del archivo JSON en una variable de Python.
            datos_json = json.load(archivo)

        # Se convierten los datos cargados a un diccionario usando el comando dict.
        datos_diccionario = dict(datos_json)

        # Se devuelve el diccionario generado.
        return datos_diccionario

    # Esta excepcion se ejecuta si el archivo JSON no existe o no se encuentra.
    except FileNotFoundError as exc:
        # Se vuelve a lanzar el error con un mensaje mas claro para el usuario.
        raise FileNotFoundError(f"No se encontro el archivo: {ruta_archivo}") from exc

    # Esta excepcion se ejecuta si el archivo existe pero su contenido no es un JSON valido.
    except json.JSONDecodeError as exc:
        # Se vuelve a lanzar el error indicando que el JSON no tiene un formato correcto.
        raise json.JSONDecodeError("El archivo no contiene un JSON valido", exc.doc, exc.pos) from exc


# Esta funcion crea un archivo JSON de ejemplo con los datos solicitados.
def crear_json_de_ejemplo(ruta_archivo):
    # Se define un diccionario con la direccion, la cantidad de alumnos,
    # el puerto y el estado de debug.
    datos = {
        "dirección": "Lima 757",
        "cantidad de alumnos": 3547,
        "puerto": 8080,
        "debug": True
    }

    # Se abre o crea el archivo JSON en modo escritura con codificacion UTF-8.
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        # Se escriben los datos en formato JSON, conservando caracteres especiales.
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


# Punto de entrada principal del programa.
if __name__ == "__main__":
    # Se define el nombre del archivo JSON que contendra los datos.
    archivo_json = "datos_configuracion.json"

    # Se crea el archivo JSON de ejemplo con la informacion requerida.
    crear_json_de_ejemplo(archivo_json)

    # Se llama a la funcion leer_dirección para leer el archivo y convertirlo en diccionario.
    resultado = leer_dirección(archivo_json)

    # Se muestra en pantalla el diccionario resultante.
    print("Diccionario generado:")
    print(resultado)
