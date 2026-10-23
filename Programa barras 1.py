# Importa el módulo pyplot para construir gráficos.
import matplotlib.pyplot as plt
# Define las etiquetas ordenadas del eje horizontal.
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
# Define una medición de ventas para cada mes.
ventas = [120, 135, 128, 150, 170, 182]
# Crea una figura y un área de dibujo de 8 por 4 pulgadas.
fig, ax = plt.subplots(figsize=(8, 4))
# Dibuja la serie como línea y marca cada observación con un círculo.
ax.plot(meses, ventas, marker="o")
# Escribe un título que describe la métrica y el período.
ax.set_title("Ventas mensuales")
# Nombra la variable representada en el eje horizontal.
ax.set_xlabel("Mes")
# Nombra la variable y la unidad del eje vertical.
ax.set_ylabel("Unidades")
# Ajusta los márgenes internos para evitar recortes de texto.
fig.tight_layout()
# Muestra la figura en pantalla.
plt.show()
