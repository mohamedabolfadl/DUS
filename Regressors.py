# Regression Template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(4, input_dim=4, kernel_initializer='normal', activation='relu'))
	model.add(Dense(4,  kernel_initializer='normal', activation='relu'))
	model.add(Dense(4,  kernel_initializer='normal', activation='relu'))
    
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model



def get_x_ordered(x,y):
    lists = sorted(zip(*[x, y]))
    new_x, new_y = list(zip(*lists))
    return new_x

def get_y_ordered(x,y):
    lists = sorted(zip(*[x, y]))
    new_x, new_y = list(zip(*lists))
    return new_y


    
def get_R_2(y,yhat):
    SS_Residual = sum((y-yhat)**2)
    SS_Total = sum((y-np.mean(y))**2)
    return 1 - (float(SS_Residual))/SS_Total

def get_adjust_R_2(y,yhat,N_features):
    SS_Residual = sum((y-yhat)**2)
    SS_Total = sum((y-np.mean(y))**2)
    r_squared = 1 - (float(SS_Residual))/SS_Total
    return 1 - (1-r_squared)*(len(y)-1)/(len(y)-N_features-1)


# Importing the dataset
#dataset = pd.read_csv('Position_Salaries.csv')
dataset = pd.read_csv('train.csv')
X = dataset.iloc[:, :4].values
y = dataset.iloc[:, 4].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)



X_train = X
y_train = y
X_test = X
y_test = y



# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)

# Linear
# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
X_lin = X_train[:, 0]
X_lin = X_lin.reshape((len(X_lin),1))
regressor.fit(X_lin, y_train)
# Predicting the Test set results
X_lin_test = X_test[:,0]
X_lin_tes = X_lin_test.reshape((len(X_lin_test),1))
y_pred_lm = regressor.predict(X_lin_tes)
y_pred_lm = sc_y.inverse_transform(y_pred_lm)

# Multiple Linear
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)
# Predicting the Test set results
y_pred_ml = regressor.predict(X_test)
y_pred_ml = sc_y.inverse_transform(y_pred_ml)

# SVR
from sklearn.svm import SVR
regressor = SVR(kernel = 'rbf')
regressor.fit(X_train, y_train)
# Predicting a new result
y_pred_SVR = regressor.predict(X_test)
y_pred_SVR = sc_y.inverse_transform(y_pred_SVR)

# Decision tree
from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(random_state = 0)
regressor.fit(X_train, y_train)
# Predicting a new result
y_pred_DT = regressor.predict(X_test)
y_pred_DT = sc_y.inverse_transform(y_pred_DT)


# Random forest
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X_train, y_train)
# Predicting a new result
y_pred_RF = regressor.predict(X_test)
y_pred_RF = sc_y.inverse_transform(y_pred_RF)

# Polynomial
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 2)
X_poly = poly_reg.fit_transform(X_train)
poly_reg.fit(X_poly, y_train)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, y_train)
y_pred_poly = lin_reg_2.predict(poly_reg.fit_transform(X_test))
y_pred_poly = sc_y.inverse_transform(y_pred_poly)

# Neural Network
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

N_feat = X_test.shape[1]
classifier = Sequential()
classifier.add(Dense(units = 40, kernel_initializer = 'normal', activation = 'relu', input_dim = N_feat))
classifier.add(Dense(units = 1, kernel_initializer = 'normal'))
classifier.compile(loss='mean_squared_error', optimizer='adam')
histor = classifier.fit(X_train, y_train, batch_size = 10, epochs = 500)
y_pred_nn = classifier.predict(X_test)
y_pred_nn = sc_y.inverse_transform(y_pred_nn)



# Visualising the Regression results
X_plot = sc_X.inverse_transform(X_test)
plt.scatter(X_plot[:,0], y_test, color = 'red', s=1.9)
#"""
plt.plot(get_x_ordered(X_plot[:,0],y_pred_lm), get_y_ordered(X_plot[:,0],y_pred_lm), color = 'black',label = 'LIN', linewidth=0.6)
plt.plot(get_x_ordered(X_plot[:,0],y_pred_DT), get_y_ordered(X_plot[:,0],y_pred_DT), color = 'yellow',label = 'DT', linewidth=0.6)
plt.plot(get_x_ordered(X_plot[:,0],y_pred_ml), get_y_ordered(X_plot[:,0],y_pred_ml), color = 'green',label = 'ML', linewidth=0.6)
plt.plot(get_x_ordered(X_plot[:,0],y_pred_RF), get_y_ordered(X_plot[:,0],y_pred_RF), color = 'purple',label = 'RF', linewidth=0.6)
plt.plot(get_x_ordered(X_plot[:,0],y_pred_SVR), get_y_ordered(X_plot[:,0],y_pred_SVR), color = 'magenta',label = 'SVR', linewidth=0.6)
plt.plot(get_x_ordered(X_plot[:,0],y_pred_poly), get_y_ordered(X_plot[:,0],y_pred_poly), color = 'blue',label = 'POL', linewidth=0.6)
plt.plot(get_x_ordered(X_plot[:,0],y_pred_nn), get_y_ordered(X_plot[:,0],y_pred_nn), color = 'c',label = 'NN', linewidth=0.6)

#"""

"""
plt.scatter(X_plot[:,0], y_pred_lm, color = 'black',label = 'LIN')
plt.scatter(X_plot[:,0], y_pred_DT, color = 'yellow',label = 'DT')
plt.scatter(X_plot[:,0], y_pred_ml, color = 'green',label = 'ML')
plt.scatter(X_plot[:,0], y_pred_RF, color = 'purple',label = 'RF')
plt.scatter(X_plot[:,0], y_pred_SVR, color = 'magenta',label = 'SVR')
plt.scatter(X_plot[:,0], y_pred_poly, color = 'blue',label = 'POL')
plt.scatter(X_plot[:,0], y_pred_nn, color = 'c',label = 'NN', s=1.9)

"""

#legend = ax.legend(loc='upper center', shadow=True)

plt.title('Truth or Bluff (Regression Model)')
plt.xlabel('QM')
plt.ylabel('Pr')

plt.grid()
plt.show()


y_t = y_test
N = len(y_t)
cost_lm = sum(abs(y_t - y_pred_lm))/N
cost_DT = sum(abs(y_t - y_pred_DT))/N
cost_ml = sum(abs(y_t - y_pred_ml))/N
cost_RF = sum(abs(y_t - y_pred_RF))/N
cost_SVR = sum(abs(y_t - y_pred_SVR))/N
cost_poly = sum(abs(y_t - y_pred_poly))/N
cost_NN = sum(abs(y_t - y_pred_nn.reshape(N,)))/N


#

r2_lm = get_adjust_R_2(y_t,y_pred_lm,1)
r2_DT = get_adjust_R_2(y_t,y_pred_DT,X_test.shape[1])
r2_ml = get_adjust_R_2(y_t,y_pred_ml,X_test.shape[1])
r2_RF = get_adjust_R_2(y_t,y_pred_RF,X_test.shape[1])
r2_SVR = get_adjust_R_2(y_t,y_pred_SVR,X_test.shape[1])
r2_poly = get_adjust_R_2(y_t,y_pred_poly,X_poly.shape[1])
r2_nn = get_adjust_R_2(y_t,y_pred_nn.reshape(N,),X_test.shape[1])



diff_df_nn = pd.DataFrame()
diff_df_nn["Cost_diff"] = 100.0*(y_t-y_pred_nn.reshape(N,))/y_t

diff_df_lm = pd.DataFrame()
diff_df_lm["Cost_diff"] = 100.0*(y_t-y_pred_lm.reshape(N,))/y_t





# Visualising the Regression results (for higher resolution and smoother curve)
#X_grid = np.arange(min(X_test), max(X_test), 0.1)
#X_grid = X_grid.reshape((len(X_grid), 1))
#plt.scatter(X_test, y_test, color = 'red')
#plt.plot(X_grid, regressor.predict(X_grid), color = 'blue')
#plt.title('Truth or Bluff (Regression Model)')
#plt.xlabel('Position level')
#plt.ylabel('Salary')
#plt.show()
