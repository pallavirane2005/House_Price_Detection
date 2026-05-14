import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('train.csv')
print('Dataset shape:', df.shape)

target = 'SalePrice'
selected_features = ['LotArea', 'OverallQual', 'OverallCond', 'YearBuilt', 'GrLivArea', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd', 'GarageCars', 'TotalBsmtSF']
categorical_features = ['Neighborhood', 'HouseStyle', 'KitchenQual']
all_features = selected_features + categorical_features

X = df[all_features].copy()
y = df[target]

for col in selected_features:
    X[col] = X[col].fillna(X[col].median())
for col in categorical_features:
    X[col] = X[col].fillna(X[col].mode()[0])
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print('R2 Score:', r2_score(y_test, y_pred))
print('MAE: $', mean_absolute_error(y_test, y_pred))

joblib.dump(model, 'model.pkl')
print('Model saved!')