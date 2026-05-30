import pandas as pd

from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans

import joblib

print("Loading Data...")

rfm = pd.read_csv(

"Data/processed/rfm_features.csv"

)

print("Scaling Features...")

scaler = StandardScaler()

scaled = scaler.fit_transform(

rfm[

[
'Recency',

'Frequency',

'Monetary'

]

]

)

print("Training KMeans...")

kmeans = KMeans(

n_clusters=4,

random_state=42

)

kmeans.fit(

scaled

)

print("Saving Models...")

joblib.dump(

scaler,

"models/saved_models/scaler.pkl"

)

joblib.dump(

kmeans,

"models/saved_models/kmeans.pkl"

)

print(

"Done"

)