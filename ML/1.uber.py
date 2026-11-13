import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from math import radians, sin, cos, sqrt, atan2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

df = pd.read_csv("uber.csv")

print(df.head())
print(df.shape)
print(df.info())
print(df.describe())

df = df.drop(['Unnamed: 0', 'key'], axis=1)

print(df.isnull().sum())

df = df.dropna()

df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

df['hour'] = df['pickup_datetime'].dt.hour
df['day'] = df['pickup_datetime'].dt.day
df['month'] = df['pickup_datetime'].dt.month
df['year'] = df['pickup_datetime'].dt.year
df['dayofweek'] = df['pickup_datetime'].dt.dayofweek

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return 6371 * c

df['distance_km'] = df.apply(
    lambda row: haversine_distance(
        row['pickup_latitude'],
        row['pickup_longitude'],
        row['dropoff_latitude'],
        row['dropoff_longitude']
    ),
    axis=1
)

print(df[['pickup_latitude', 'pickup_longitude',
          'dropoff_latitude', 'dropoff_longitude',
          'distance_km']].head())

df = df.drop('pickup_datetime', axis=1)

df = df[df['fare_amount'] > 0]

sns.boxplot(x=df['fare_amount'])
plt.show()

Q1 = df['fare_amount'].quantile(0.25)
Q3 = df['fare_amount'].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df['fare_amount'] < lower) |
    (df['fare_amount'] > upper)
]

print("Number of outliers:", len(outliers))

df = df[
    (df['fare_amount'] >= lower) &
    (df['fare_amount'] <= upper)
]

correlation = df.corr(numeric_only=True)
print(correlation)

sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.show()

X = df.drop('fare_amount', axis=1)
y = df['fare_amount']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)

r2_lr = r2_score(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
mae_lr = mean_absolute_error(y_test, y_pred_lr)

print("\nLinear Regression Results:")
print("R2:", r2_lr)
print("RMSE:", rmse_lr)
print("MAE:", mae_lr)

rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

print("Random Forest training started...")

rf.fit(X_train, y_train)

print("Random Forest training completed!")

y_pred_rf = rf.predict(X_test)

print("Random Forest prediction completed!")

r2_rf = r2_score(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
mae_rf = mean_absolute_error(y_test, y_pred_rf)

print("\nRandom Forest Results:")
print("R2:", r2_rf)
print("RMSE:", rmse_rf)
print("MAE:", mae_rf)

results = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest'],
    'R2': [r2_lr, r2_rf],
    'RMSE': [rmse_lr, rmse_rf],
    'MAE': [mae_lr, mae_rf]
})

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

print(results.to_string(index=False))