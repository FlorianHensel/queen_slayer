import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential, layers

df = pd.read_csv("train_data_1000.csv")
df["eval"] = df["eval"].clip(lower = -15, upper = 15)
X = df.drop(columns = "eval")
y = df[["eval"]]

# CHANGE ENCODING
for i in range(1, 65):
    X[f'feat_{i}'] = X[f'feat_{i}'].replace([-3, 3], [-4, 4])

# CHANGE ENCODING
for i in range(1, 65):
    X[f'feat_{i}'] = X[f'feat_{i}'].replace([-2.9, 2.9], [-3, 3])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model definition
model = Sequential()
model.add(layers.Dense(1000, activation='relu', input_dim=X.shape[1]))
model.add(layers.Dense(800, activation='relu'))
model.add(layers.Dense(300, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='linear'))

model.compile(loss='mae', optimizer='adam')
model.fit(X_train, y_train, batch_size=248, epochs=15,verbose=1)
model.evaluate(X_test, y_test, verbose = 1)

# serialize model to JSON
model2_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model2_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
