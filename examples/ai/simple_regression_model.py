import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# House sizes (in square feet)
sizes = np.array([500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000])

# Prices (in $1000s)
prices = np.array([150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650])

X = sizes.reshape(-1, 1)  # shape: (n_samples, 1)
y = prices

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")
print(f"Slope (m): {model.coef_[0]:.2f}")
print(f"Intercept (b): {model.intercept_:.2f}")

print("\n")
em = "—"*40
print(em)
print(f"MSE: {mse:.2f}")
print(em)
print(f"R²: {r2:.2f}")
print(em)
print(f"Equation: price = {model.coef_[0]:.2f} * size + {model.intercept_:.2f}")  # |left      |
print(em)