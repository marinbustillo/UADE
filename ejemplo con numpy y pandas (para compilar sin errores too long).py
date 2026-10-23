# -*- coding: utf-8 -*-  # Define la codificación UTF-8 para permitir tildes y caracteres en español.

import numpy as np  # Importa NumPy con el alias np para realizar cálculos vectorizados sobre arreglos numéricos.
import pandas as pd  # Importa Pandas con el alias pd para crear, limpiar, transformar y agrupar datos tabulares.

ventas = pd.DataFrame({  # Crea un DataFrame llamado ventas con datos simulados de una tienda.
    "producto": ["Notebook", "Mouse", "Teclado", "Monitor", "Mouse", "Notebook"],
    "region": ["Norte", "Sur", "Norte", "Centro", "Sur", "Centro"],  # Define la región donde ocurrió cada venta.
    "precio": ["$850", "$25", "$45", "$300", None, "$850"],
    "cantidad": [2, 10, 5, 3, 4, 1]  # Define la cantidad vendida en cada registro.
})  # Cierra la creación del DataFrame ventas.

print("DATOS ORIGINALES")  # Imprime un título para mostrar los datos antes de limpiarlos.
print(ventas)  # Muestra en pantalla el DataFrame original con productos, regiones, precios y cantidades.
print()  # Imprime una línea en blanco para separar visualmente las secciones del resultado.

ventas_limpias = ventas.copy()  # Crea una copia del DataFrame para limpiar los datos sin modificar la tabla original.
ventas_limpias["precio"] = ventas_limpias["precio"].str.replace("$", "", regex=False)
ventas_limpias["precio"] = pd.to_numeric(ventas_limpias["precio"], errors="coerce")
precio_promedio = ventas_limpias["precio"].mean()
ventas_limpias["precio"] = ventas_limpias["precio"].fillna(precio_promedio)
ventas_limpias["precio"] = ventas_limpias["precio"].round(2)  # Redondea los precios a 2 decimales.
ventas_limpias["cantidad"] = pd.to_numeric(ventas_limpias["cantidad"], errors="coerce")
ventas_limpias["cantidad"] = ventas_limpias["cantidad"].fillna(0).astype(int)

print("DATOS LIMPIOS")  # Imprime un título para mostrar los datos después de limpiar precios y cantidades.
print(ventas_limpias)  # Muestra el DataFrame limpio con precios numéricos y cantidades válidas.
print()  # Imprime una línea en blanco para separar visualmente las secciones del resultado.

precios_numpy = ventas_limpias["precio"].to_numpy()  # Convierte la columna precio en un arreglo de NumPy.
cantidades_numpy = ventas_limpias["cantidad"].to_numpy()  # Convierte la columna cantidad en un arreglo de NumPy.
totales_numpy = precios_numpy * cantidades_numpy  # Calcula el total de cada venta multiplicando precio por cantidad.
ventas_limpias["total"] = totales_numpy  # Agrega la columna total al DataFrame usando el resultado calculado con NumPy.
ventas_limpias["total"] = ventas_limpias["total"].round(2)  # Redondea el total de cada venta a 2 decimales.
ventas_limpias["venta_alta"] = np.where(ventas_limpias["total"] >= ventas_limpias["total"].mean(), "Sí", "No")

print("VENTAS CON TOTAL CALCULADO")  # Imprime un título para mostrar el resultado del cálculo de ingresos por venta.
print(ventas_limpias[["producto", "region", "precio", "cantidad", "total", "venta_alta"]])
print()  # Imprime una línea en blanco para separar visualmente las secciones del resultado.

ingresos_por_region = ventas_limpias.groupby("region", as_index=False)["total"].sum()
ingresos_por_region = ingresos_por_region.sort_values(by="total", ascending=False)
ingresos_por_region["total"] = ingresos_por_region["total"].round(2)  # Redondea los ingresos agrupados a 2 decimales.

print("INGRESO TOTAL POR REGIÓN")  # Imprime un título para mostrar el resumen agrupado por región.
print(ingresos_por_region)  # Muestra el ingreso total obtenido por cada región.
print()  # Imprime una línea en blanco para separar visualmente las secciones del resultado.

region_ganadora = ingresos_por_region.iloc[0]["region"]  # Obtiene el nombre de la región con mayor ingreso total.
ingreso_ganador = ingresos_por_region.iloc[0]["total"]  # Obtiene el ingreso total de la región ganadora.
producto_mayor_venta = ventas_limpias.loc[ventas_limpias["total"].idxmax(), "producto"]
venta_mayor_valor = ventas_limpias["total"].max()  # Obtiene el valor de la venta individual más alta.

print("INTERPRETACIÓN")  # Imprime un título para presentar la interpretación de resultados.
print(f"La región con mayor ingreso total es {region_ganadora}, con un ingreso de ${ingreso_ganador}.")
print(f"La venta más alta corresponde al producto {producto_mayor_venta}, con un total de ${venta_mayor_valor}.")
print()  # Imprime una línea en blanco para separar visualmente las secciones del resultado.

print("RECOMENDACIÓN")  # Imprime un título para presentar la recomendación final.
print(f"Priorizar acciones comerciales en la región {region_ganadora}, qué productos impulsan sus ingresos")

