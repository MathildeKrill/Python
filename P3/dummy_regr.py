import matplotlib.pyplot as plt  # To visualize
from sklearn.linear_model import LinearRegression
import random
import numpy

def column_reshape(a_list):
    return numpy.reshape(a_list, (-1, 1))

random.seed()
X = column_reshape([i + 0.25 * (random.random() * 2 - 1) for i in range(0, 100)])
Y = column_reshape([2*i + 100. for i in range(0, 100)])
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions
print(linear_regressor.coef_)
plt.scatter(X, Y)
plt.plot(X, Y_pred, color='red')
plt.show()