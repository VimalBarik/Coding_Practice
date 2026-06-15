import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

df = pd.read_csv("Train.csv")

df.head()

df.info()

df.describe().transpose()

import seaborn as sns

df.head()

from sklearn.model_selection import train_test_split

X = df.drop("Reached.on.Time_Y.N", axis= 1)

X.head()

y = df["Reached.on.Time_Y.N"]

y.head()

print(y.value_counts(normalize=True))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state=42, shuffle=True)

X_train

from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

X_train_processed = X_train.drop('ID', axis=1)

X_test_processed = X_test.drop('ID', axis=1)

X_train_processed.info()

X_train_cat = X_train_processed.select_dtypes(include = ['category', 'object'])

X_train_num = X_train_processed.select_dtypes(include= ['int64'])

X_test_cat = X_test_processed.select_dtypes(include = ['category', 'object'])
X_test_num = X_test_processed.select_dtypes(include= ['int64'])

ohe = OneHotEncoder()
X_train_ohe = ohe.fit_transform(X_train_cat)
X_test_ohe = ohe.transform(X_test_cat)

print(X_train_ohe.toarray())

scaler = MinMaxScaler()
X_train_scale = scaler.fit_transform(X_train_num)
X_test_scale = scaler.transform(X_test_num)

X_test_scale

X_train_ohe_dense = X_train_ohe.toarray()
X_test_ohe_dense = X_test_ohe.toarray()

X_train_final = np.concatenate((X_train_scale, X_train_ohe_dense), axis=1)
X_test_final = np.concatenate((X_test_scale, X_test_ohe_dense), axis=1)

X_train_final.shape[1]

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.optimizers import Adam

custom_learning_rate = 0.001

custom_adam = Adam(learning_rate=custom_learning_rate)

model = Sequential([
    tf.keras.Input(shape = (19,)),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(64, activation = 'relu'),
    Dropout(0.3),
    Dense(2, activation='softmax')
])

model.compile(optimizer = custom_adam,
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'])

y_train_ohe = tf.keras.utils.to_categorical(y_train, num_classes=2)
y_test_ohe = tf.keras.utils.to_categorical(y_test, num_classes=2)


model.build((None, X_train_final.shape[1]))

history = model.fit(
    X_train_final,
    y_train_ohe,
    epochs = 50,
    verbose= 2,
    batch_size= 32,
    validation_data = (X_test_final, y_test_ohe)
)

def predict_on_single_row(single_row_data):
    input_df = pd.DataFrame([single_row_data])


    if 'ID' in input_df.columns:
        input_processed = input_df.drop('ID', axis=1)
    else:
        input_processed = input_df.copy()


    input_cat = input_processed.select_dtypes(include = ['object'])
    input_num = input_processed.select_dtypes(include= ['int64'])


    input_scale = scaler.transform(input_num)


    input_ohe = ohe.transform(input_cat).toarray()


    input_final = np.concatenate((input_scale, input_ohe), axis=1)


    predictions = model.predict(input_final)


    predicted_class = np.argmax(predictions, axis=1)[0]


    if predicted_class == 1:
        result = "The shipment is predicted to reach on time."
    else:
        result = "The shipment is predicted NOT to reach on time."

    return predicted_class, result

user_input_series = pd.Series({
    'ID': 0,
    'Warehouse_block': 'D',
    'Mode_of_Shipment': 'Flight',
    'Customer_care_calls': 4,
    'Customer_rating': 2,
    'Cost_of_the_Product': 177,
    'Prior_purchases': 3,
    'Product_importance': 'low',
    'Gender': 'F',
    'Discount_offered': 44,
    'Weight_in_gms': 1233
})

predicted_class, prediction_result = predict_on_single_row(user_input_series)

print(f"Predicted Class: {predicted_class}")
print(f"Prediction Result: {prediction_result}")

