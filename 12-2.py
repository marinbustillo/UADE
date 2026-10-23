# Importa el dataset Wine incluido en Scikit-learn.
from sklearn.datasets import load_wine
# Importa la función para separar train y test.
from sklearn.model_selection import train_test_split
# Importa StandardScaler para estandarizar las variables.
from sklearn.preprocessing import StandardScaler
# Importa el clasificador de regresión logística.
from sklearn.linear_model import LogisticRegression
# Importa Pipeline para organizar el flujo de preprocesamiento.
from sklearn.pipeline import Pipeline
# Importa las métricas de clasificación.
from sklearn.metrics import accuracy_score, confusion_matrix
# Carga las características químicas en X y las clases en y.
X, y = load_wine(return_X_y=True)
# Divide los datos y mantiene la proporción de cada clase.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
# Crea un Pipeline con escalado y regresión logística.
modelo = Pipeline([
    ("escalador", StandardScaler()),
    ("logistica", LogisticRegression(max_iter=500))
])
# Entrena el Pipeline con el conjunto de entrenamiento.
modelo.fit(X_train, y_train)
# Predice las clases del conjunto de prueba.
y_pred = modelo.predict(X_test)
# Calcula el accuracy de la clasificación.
accuracy = accuracy_score(y_test, y_pred)
# Calcula la matriz de confusión.
matriz = confusion_matrix(y_test, y_pred)
# Muestra el accuracy redondeado.
print("Accuracy:", round(accuracy, 3))
# Muestra la matriz de confusión.
print("Matriz de confusión:\n", matriz)
# Muestra cinco clases reales.
print("Reales:", y_test[:5])
# Muestra cinco clases predichas.
print("Predichas:", y_pred[:5])
