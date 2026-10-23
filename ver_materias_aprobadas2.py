# Programa para consultar materias aprobadas desde un archivo CSV.
# El programa crea un archivo CSV de ejemplo, solicita un DNI al usuario
# y busca todas las materias aprobadas asociadas a ese DNI.

# Se importa el modulo csv para leer y escribir archivos CSV.
import csv


# Esta funcion recibe la ruta del archivo CSV y un numero de DNI.
# Luego busca todas las materias aprobadas de la persona con ese DNI.
def ver_materias_aprobadas(ruta_archivo_csv, dni_buscado):
    # Se crea una lista vacia para guardar las materias aprobadas encontradas.
    materias_aprobadas = []

    # Se crea una variable para guardar el nombre de la persona, si se encuentra.
    nombre_persona = None

    # El bloque try intenta abrir y leer el archivo CSV indicado.
    try:
        # Se abre el archivo CSV en modo lectura con codificacion UTF-8.
        with open(ruta_archivo_csv, "r", encoding="utf-8", newline="") as archivo_csv:
            # Se utiliza DictReader para leer cada fila del CSV como un diccionario.
            lector_csv = csv.DictReader(archivo_csv)

            # Se valida que el archivo CSV tenga los encabezados esperados.
            columnas_requeridas = {"nombre", "DNI", "materia aprobada", "debug"}

            # Si el archivo CSV no tiene encabezados, fieldnames sera None.
            if lector_csv.fieldnames is None:
                raise ValueError("El archivo CSV no contiene encabezados.")

            # Se verifica que todas las columnas requeridas existan en el archivo CSV.
            if not columnas_requeridas.issubset(set(lector_csv.fieldnames)):
                raise ValueError("El archivo CSV no contiene todas las columnas requeridas.")

            # Se recorre cada fila del archivo CSV.
            for fila in lector_csv:
                # Se compara el DNI ingresado por el usuario con el DNI de la fila actual.
                if fila["DNI"] == dni_buscado:
                    # Se guarda el nombre de la persona encontrada.
                    nombre_persona = fila["nombre"]

                    # Se agrega la materia aprobada a la lista de materias.
                    materias_aprobadas.append(fila["materia aprobada"])

        # Se devuelve un diccionario usando el comando dict.
        # El diccionario contiene el DNI consultado, el nombre encontrado,
        # las materias aprobadas y la cantidad total de materias aprobadas.
        return dict({
            "DNI": dni_buscado,
            "nombre": nombre_persona,
            "materias aprobadas": materias_aprobadas,
            "cantidad de materias aprobadas": len(materias_aprobadas)
        })

    # Esta excepcion se ejecuta si el archivo CSV no existe o no se encuentra.
    except FileNotFoundError as exc:
        # Se vuelve a lanzar el error con un mensaje mas claro para el usuario.
        raise FileNotFoundError(f"No se encontro el archivo CSV: {ruta_archivo_csv}") from exc

    # Esta excepcion se ejecuta si ocurre un error propio de lectura del archivo CSV.
    except csv.Error as exc:
        # Se vuelve a lanzar el error indicando que hubo un problema con el formato CSV.
        raise csv.Error(f"Ocurrio un error al leer el archivo CSV: {exc}") from exc

    # Esta excepcion se ejecuta si faltan columnas o el archivo no tiene encabezados validos.
    except ValueError as exc:
        # Se vuelve a lanzar el error para explicar que el archivo no cumple con el formato esperado.
        raise ValueError(f"El archivo CSV no tiene el formato esperado: {exc}") from exc

    # Esta excepcion captura cualquier otro error inesperado durante la ejecucion de la funcion.
    except Exception as exc:
        # Se vuelve a lanzar el error indicando que ocurrio un problema inesperado.
        raise RuntimeError(f"Ocurrio un error inesperado al procesar el archivo CSV: {exc}") from exc


# Esta funcion crea un archivo CSV de ejemplo con los datos solicitados.
def crear_csv_de_ejemplo(ruta_archivo_csv):
    # Se define una lista de diccionarios con alumnos, DNI, materias aprobadas y debug.
    datos = [
        {"nombre": "Ana Perez", "DNI": "12345678", "materia aprobada": "Matematica", "debug": "true"},
        {"nombre": "Ana Perez", "DNI": "12345678", "materia aprobada": "Historia", "debug": "true"},
        {"nombre": "Juan Gomez", "DNI": "87654321", "materia aprobada": "Programacion", "debug": "true"},
        {"nombre": "Juan Gomez", "DNI": "87654321", "materia aprobada": "Base de Datos", "debug": "true"},
        {"nombre": "Laura Diaz", "DNI": "11223344", "materia aprobada": "Ingles", "debug": "true"}
    ]

    # Se abre o crea el archivo CSV en modo escritura con codificacion UTF-8.
    with open(ruta_archivo_csv, "w", encoding="utf-8", newline="") as archivo_csv:
        # Se definen los encabezados del archivo CSV.
        encabezados = ["nombre", "DNI", "materia aprobada", "debug"]

        # Se crea un escritor CSV que utilizara los encabezados definidos.
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=encabezados)

        # Se escribe la primera linea del archivo CSV con los nombres de las columnas.
        escritor_csv.writeheader()

        # Se escriben todas las filas de datos en el archivo CSV.
        escritor_csv.writerows(datos)


# Punto de entrada principal del programa.
if __name__ == "__main__":
    # Se define el nombre del archivo CSV que contendra los datos.
    archivo_csv = "materias_aprobadas.csv"

    # Se crea el archivo CSV de ejemplo con la informacion requerida.
    crear_csv_de_ejemplo(archivo_csv)

    # Se solicita al usuario que ingrese el numero de DNI que desea consultar.
    dni_ingresado = input("Ingrese el numero de DNI a consultar: ").strip()

    # Se llama a la funcion ver_materias_aprobadas para buscar las materias aprobadas.
    resultado = ver_materias_aprobadas(archivo_csv, dni_ingresado)

    # Se muestra en pantalla el diccionario resultante.
    print("Resultado de la consulta:")
    print(resultado)

    # Se informa de forma clara si no se encontraron materias para el DNI ingresado.
    if resultado["cantidad de materias aprobadas"] == 0:
        print("No se encontraron materias aprobadas para el DNI ingresado.")
