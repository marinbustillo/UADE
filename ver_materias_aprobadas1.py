# Ver materias aprobadas
# Programa para buscar en un archivo CSV las materias aprobadas
# por un estudiante de la UADE a partir de su DNI.

import csv

# Nombre del archivo CSV que debe estar en la misma carpeta que este programa
archivo_csv = "materias_aprobadas_uade.csv"

# Solicitar el DNI al usuario
DNI_buscado = input("Ingrese el DNI del estudiante: ")

# Variables para guardar los datos encontrados
nombre_estudiante = ""
materias_aprobadas = []

# Abrir y leer el archivo CSV
# Se espera que el archivo tenga columnas en este orden:
# nombre, DNI, materia_aprobada
with open(archivo_csv, mode="r", encoding="utf-8") as archivo:
    lector_csv = csv.reader(archivo)

    # Saltar la primera fila si contiene encabezados
    encabezado = next(lector_csv)

    # Recorrer todas las filas del archivo CSV
    for fila in lector_csv:
        nombre = fila[0]
        DNI = fila[1]
        materia = fila[2]

        # Si el DNI coincide, guardar el nombre y la materia aprobada
        if DNI == DNI_buscado:
            nombre_estudiante = nombre
            materias_aprobadas.append(materia)

# Preparar el resultado final
if len(materias_aprobadas) > 0:
    resultado = (
        "Nombre del estudiante: " + nombre_estudiante + "
" +
        "DNI: " + DNI_buscado + "
" +
        "Materias aprobadas en UADE: " + ", ".join(materias_aprobadas)
    )
else:
    resultado = (
        "No se encontraron materias aprobadas para el DNI: " + DNI_buscado
    )

# Imprimir el nombre del estudiante, su DNI y todas las materias aprobadas
print(resultado)
