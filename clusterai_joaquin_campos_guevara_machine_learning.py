import pickle
from joblib import load
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

# primero cargamos los modelos entrenados previamente
PL1 = load("modelo_PL1.pkl")
PL2_optimo = load("modelo_PL2.pkl")


# ahora cargamos la particion que hicimos previamente
x_test = pd.read_pickle("x_test.pkl")
y_test = pd.read_pickle("y_test.pkl")


# ahora hacemos las predicciones utilizando ambos modelos y la porción del DF que separamos previamente para testear
y_pred_PL1 = PL1.predict(x_test)
mse_PL1 = mean_squared_error(y_test, y_pred_PL1)
rmse_PL1 = np.sqrt(mse_PL1)
r2_PL1 = r2_score(y_test, y_pred_PL1)


y_pred_PL2 = PL2_optimo.predict(x_test)
mse_PL2 = mean_squared_error(y_test, y_pred_PL2)
rmse_PL2 = np.sqrt(mse_PL2)
r2_PL2 = r2_score(y_test, y_pred_PL2)

# finalmente hacemos un print del score de la prediccion de cada modelo
print(f"PL1 modelo de Regresion Lineal      -> RMSE= {rmse_PL1:.2f} -- R2= {r2_PL1:.3f}")
print(f"PL2 modelo Gradient Boosting + PCA  -> RMSE= {rmse_PL2:.2f} -- R2= {r2_PL2:.3f}")
