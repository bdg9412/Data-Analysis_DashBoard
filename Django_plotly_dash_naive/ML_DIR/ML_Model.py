import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

def get_next_LinearRegression():
    df = px.data.gapminder().query("country=='India'")

    # Data type change
    x=df[0:-2]["pop"].to_numpy()
    y=df[1:-1]["pop"].to_numpy()
    y_test = df[-2:-1]["pop"].to_numpy()

    # Data shape change
    x=np.reshape(x,(-1,1))
    y=np.reshape(y,(-1,1))
    y_test=np.reshape(y_test,(-1,1))

    clf = LinearRegression()
    ml=clf.fit(x,y)

    return ml.predict(y_test)

def get_next_SVR():
    df = px.data.gapminder().query("country=='India'")

    # Data type change
    x=df[0:-2]["pop"].to_numpy()
    y=df[1:-1]["pop"].to_numpy()
    y_test = df[-2:-1]["pop"].to_numpy()

    # Data shape change
    x=np.reshape(x,(-1,1))
    y=np.reshape(y,(-1,1))
    y_test=np.reshape(y_test,(-1,1))

    clf = SVR()
    ml=clf.fit(x,y)

    return ml.predict(y_test)