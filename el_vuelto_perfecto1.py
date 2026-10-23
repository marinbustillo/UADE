# El vuelto perfecto
# Programa para calcular la menor cantidad de monedas y billetes
# necesarios para devolver una cantidad en pesos argentinos.

# Lista de monedas y billetes disponibles, ordenada de mayor a menor
monedas_y_billetes = [20000, 10000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]

# Diccionario donde se guardara la cantidad necesaria de cada moneda o billete
vuelto = {}

# Entrada de dinero a devolver
cantidad = int(input("Ingrese la cantidad de dinero a devolver en pesos argentinos: "))

# Guardamos la cantidad original para mostrarla al final
cantidad_original = cantidad

# Ciclo for para calcular el vuelto usando la menor cantidad de monedas y billetes
for valor in monedas_y_billetes:
    cantidad_de_piezas = cantidad // valor
    vuelto[valor] = cantidad_de_piezas
    cantidad = cantidad % valor

# Impresion del resultado final
print("\nEl vuelto perfecto para", cantidad_original, "pesos argentinos es:")

for valor in monedas_y_billetes:
    print("Billetes/monedas de", valor, "pesos:", vuelto[valor])
