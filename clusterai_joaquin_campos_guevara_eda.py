# Importamos las librerías para manipular datos
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# leemos el DataSet desde el repositorio. Como es mayor a 25mb lo subimos comprimido
airbnb = pd.read_csv("airbnb_us.zip")

# imprimimos las primeras 5 filas del dataframe para entender mejor como son los datos a manipular
airbnb.head()

# usamos la funcion .info() para entender el tipo de dato de cada variable, las dimensiones del dataframe y cuántos valores no nulos hay por variable.
airbnb.info()

# vemos que hay variables que contienen valores nulos y son irrelevantes para nuestro objetivo.
# para eivtar problemas más adelante y que el codigo corra más holgado, listamos las columnas a eliminar del DF
variables_a_eliminar = [
    'id',
    'name',
    'description',
    'thumbnail_url',
    'host_has_profile_pic',
    'host_identity_verified',
    'host_response_rate',
    'host_since',
    'first_review',
    'review_scores_rating',
    'last_review',
    'zipcode',
    'amenities',
]
# eliminamos estas columnas y modificamos el DF en una misma linea
airbnb.drop(variables_a_eliminar, axis=1, inplace=True)

# analizamos nuevamente el df luego de esta ultima modificacion y vemos que aun tenemos valores nulos en algunas columnas que no queremos eliminar
airbnb.isnull().sum()

# para la dimension neighbourhood, tenemos 1458 registros nulos de 19.308, es decir el 7,5% de los datos.
# decidimos conservar los registros, completando los nulos en 'neighbourhood' con el valor más repetido para la correspondiente 'city':
# para lograrlo, agrupamos por ciudad y obtenemos el neighbourhood más frecuente en esa city con una funcion lambda (si hubira un empate, .iloc[0] elige el primer neighbourhood)
moda_city = (
    airbnb.groupby('city')['neighbourhood'].agg(lambda x: x.mode().iloc[0])
)
# ahora creamos un diccionario con indice city y sus neighbourhood más frecuentes. luego completaremos los nulos recorriendo este diccionario
moda_dict = moda_city.to_dict()
# ahora recorremos la columna neighbourhood. Si encuentra un nulo, remplaza con el diccionario. si no es nulo, deja el valor original
airbnb['neighbourhood'] = airbnb.apply(
    lambda row: moda_dict[row['city']] if pd.isna(row['neighbourhood']) else row['neighbourhood'],
    axis=1
)

# al ser pocos registros y todas variables numericas, vamos a completar el dataframe con la mediana de cada variable
for col in ['bathrooms','bedrooms','beds']:
  airbnb[col] = airbnb[col].fillna(airbnb[col].median())

# aun hay que seguir tranformando el dataframe
# la columna instant_bookable debería ser un booleano donde f=False y t=True
airbnb['instant_bookable'].head()

# para evitar problemas, vamos a modificar el tipo de esta columna y tambien a declarar algunas variables como tipo 'string' ya que python no está pudiendo identificarlas correctamente y las cataloga como 'object'.
airbnb[['property_type','room_type','bed_type','cancellation_policy','city', 'neighbourhood']]=airbnb[['property_type','room_type','bed_type','cancellation_policy','city', 'neighbourhood']].astype('string')
airbnb['instant_bookable']=airbnb['instant_bookable'].map({'f': False , 't': True})
airbnb.info()

# para las variables categoricas relevantes para el posterior analisis, habría que generar variables dummies numericas para poder considerar estas dimensiones en el modelo de machine learning
city_dummies = pd.get_dummies(airbnb['city'])
property_dummies= pd.get_dummies(airbnb['property_type'])
room_dummies= pd.get_dummies(airbnb['room_type'])
bed_dummies= pd.get_dummies(airbnb['bed_type'])
cancellation_dummies= pd.get_dummies(airbnb['cancellation_policy'])
neigh_dummies = pd.get_dummies(airbnb['neighbourhood'])
# ahora las unimos al DF a trabajar
airbnb = pd.concat([airbnb, city_dummies, property_dummies, room_dummies, bed_dummies, cancellation_dummies, neigh_dummies], axis=1)
# falta eliminar las columnas categoricas originales del DF para que solo queden las dummies
airbnb = airbnb.drop(
    ['city', 'property_type', 'room_type', 'bed_type', 'cancellation_policy', 'neighbourhood'], axis=1)

# guardamos el dataframe procesado como airbnb_df para poder entrenar a los modelos de ML
airbnb.to_csv("airbnb_df.csv", index=False)
