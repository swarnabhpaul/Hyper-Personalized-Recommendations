import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import tensorflow as tf
from tensorflow.keras import layers, regularizers, models, optimizers
import joblib

pd.set_option('display.max_columns', None)

# ----------------------------
# 1. Load and Merge the Data
# ----------------------------
# Load data from CSV files
customers = pd.read_csv('customers_usa.csv')
loan_products = pd.read_csv('loan_product_data.csv')
loan_apps = pd.read_csv('loan_applications.csv')

# Assume the common key in customers and loan_apps is 'cid'
# And loan_apps has a foreign key 'loan_product_id' to join with loan_products

# Merge loan applications with customers on 'cid'
data = pd.merge(loan_apps, customers, on='cid', how='left')

# Merge the resulting data with loan products on 'loan_product_id'
data = pd.merge(data, loan_products, on='loan_product_id', how='left')

# ----------------------------
# 2. Create Target Variable
# ----------------------------
# We consider only 'approved' as positive (1); both 'rejected' and 'pending' as negative (0).
data['approved'] = np.where(data['status'] == 'approved', 1, 0)

# ----------------------------
# 3. Drop ID Columns and Unused Fields
# ----------------------------
# Drop id-type columns and the original status column (since target is now created)
id_columns = ['cid', 'application_id', 'loan_product_id', 'name', 'location', 'occupation']
data = data.drop(columns=id_columns + ['status'])


# ----------------------------
# 4. Feature Engineering
# ----------------------------
# If an application_date (or similar) column exists, convert it to datetime and extract features.
if 'application_date' in data.columns:
    data['application_date'] = pd.to_datetime(data['application_date'], errors='coerce')
    # Example: extract the month as a cyclical feature (sine and cosine components)
    data['app_month'] = data['application_date'].dt.month
    data['app_month_sin'] = np.sin(2 * np.pi * data['app_month'] / 12)
    data['app_month_cos'] = np.cos(2 * np.pi * data['app_month'] / 12)
    # Drop raw date columns if no longer needed
    data = data.drop(columns=['application_date', 'app_month'])

# ----------------------------
# 5. Identify Feature Columns
# ----------------------------
# We'll use all remaining columns (except the target 'approved') as features.
# We'll let the preprocessor decide based on the datatype.
features = data.drop(columns=['approved'])
target = data['approved']

# Option 1: Automatically determine numeric and categorical features
numeric_features = features.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = features.select_dtypes(include=['object']).columns.tolist()

print("Numeric features:", numeric_features)
print("Categorical features:", categorical_features)

# ----------------------------
# 6. Preprocessing Pipeline
# ----------------------------
# Pipeline for numeric features: scaling
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Pipeline for categorical features: one-hot encoding
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine transformations using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# ----------------------------
# 7. Split Data and Transform
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(features, target, 
                                                    test_size=0.2, random_state=42)

# print(X_train.iloc[0])

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

joblib.dump(preprocessor, 'preprocessor_loan.joblib')

# Input dimension for the model
input_dim = X_train_processed.shape[1]

# ----------------------------
# 8. Build the Deep Neural Network Model
# ----------------------------
model = models.Sequential([
    layers.InputLayer(input_shape=(input_dim,)),
    layers.Dense(128, activation='relu'),#, kernel_regularizer=regularizers.l2(0.0001)),
    # layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),# kernel_regularizer=regularizers.l2(0.0001)),
    # layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),# kernel_regularizer=regularizers.l2(0.0001)),
    # layers.Dropout(0.3),
    layers.Dense(16, activation='relu'),# kernel_regularizer=regularizers.l2(0.0001)),
    # layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')  # Output: probability of approval
])

model.compile(optimizer=optimizers.Adam(learning_rate=0.01), loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# ----------------------------
# 9. Train the Model
# ----------------------------
history = model.fit(X_train_processed, y_train, 
                    validation_split=0.2,
                    epochs=100,
                    batch_size=32,
                    verbose=1)

model.save('loan_approval_model.keras')

# ----------------------------
# 10. Evaluate the Model
# ----------------------------
loss, accuracy = model.evaluate(X_test_processed, y_test, verbose=0)
print(f'Test Accuracy: {accuracy:.4f}')

# Optionally, output predicted probabilities for test set:
y_pred_prob = model.predict(X_test_processed)
# print(y_pred_prob[:20], y_test[:20])

for layer in model.layers:
    if 'Dropout' in str(layer):
        continue
    weights = layer.get_weights()  # List of numpy arrays
    print(f"Layer: {layer.name}")
    print(f"Weights: {weights[0]}")
    print(f"Biases: {weights[1]}")
