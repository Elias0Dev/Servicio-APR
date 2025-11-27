import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar datos desde CSV (exportado desde Django)
# El CSV debe tener al menos: total_pagar, consumo, subsidio, corte,
# fecha_emision, fecha_vencimiento, estado_pago
df = pd.read_csv(
    'Factura.csv',
    sep=';',                # <- separador correcto
    parse_dates=['fecha_emision', 'fecha_vencimiento']
)

# 2. Ingeniería de características

# Booleanos a 0/1
df['subsidio_int'] = df['subsidio'].astype(int)
df['corte_int'] = df['corte'].astype(int)

# Días entre emisión y vencimiento
df['dias_vencimiento'] = (df['fecha_vencimiento'] - df['fecha_emision']).dt.days

# (Opcional) eliminar filas con datos faltantes básicos
df = df.dropna(subset=['total_pagar', 'consumo', 'estado_pago', 'dias_vencimiento'])

# Variable objetivo: estado_pago (True/False -> 1/0)
df['estado_pago_int'] = df['estado_pago'].astype(int)

# 3. Definir X (features) e y (target)
features = ['total_pagar', 'consumo', 'subsidio_int', 'corte_int', 'dias_vencimiento']
X = df[features]
y = df['estado_pago_int']

# 4. Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 5. Entrenar modelo RandomForest binario
clf = RandomForestClassifier(
    n_estimators=200,
    max_depth=5,
    min_samples_leaf=10,
    random_state=42
)
clf.fit(X_train, y_train)

# 6. Guardar modelo para usarlo en Django
joblib.dump(clf, 'modelo_estado_pago.pkl')

# 7. Evaluación
y_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print("\nMatriz de confusión prueba:\n", cm)
print("\nReporte de clasificación prueba:\n", classification_report(
    y_test, y_pred, labels=[0,1], target_names=['No paga', 'Paga']
))

# 8. Gráfico: Matriz de confusión
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No paga', 'Paga'],
            yticklabels=['No paga', 'Paga'])
plt.xlabel('Predicción')
plt.ylabel('Etiqueta real')
plt.title('Matriz de Confusión (Estado de pago)')
plt.show()

# 9. Gráfico extra: Importancia de características
importances = clf.feature_importances_
plt.figure(figsize=(6,4))
plt.bar(features, importances, color='tomato')
plt.xticks(rotation=45)
plt.title('Importancia de las características')
plt.ylabel('Importancia')
plt.tight_layout()
plt.show()
