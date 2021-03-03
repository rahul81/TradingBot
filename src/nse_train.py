import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.preprocessing import StandardScaler

from get_nse_data import resample
from ta import add_all_ta_features


df = resample()

df = add_all_ta_features(
    df, open="Open", high="High", low="Low", close="Close", volume="Volume"
)
df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(0)

scaler = StandardScaler()
data = df.drop(
    ["five_d_obs", "thirty_d_obs", "sixty_d_obs", "Open", "Low", "High"], axis=1
)
data = scaler.fit_transform(data)
target = ["five_d_obs"]

x_train, x_test, y_train, y_test = train_test_split(
    data, df[target[0]].values, test_size=0.2, random_state=0
)

model = LogisticRegression(
    solver="liblinear", C=0.05, multi_class="ovr", random_state=0
)

model.fit(x_train, y_train)

preds = model.predict(x_test)

loss = mean_squared_error(y_test, preds)

print(f"{target[0]} model loss: {loss}")

print("--------------------------------")

print(
    f"{target[0]} model classification_report: \n {classification_report(y_test,preds)}"
)
