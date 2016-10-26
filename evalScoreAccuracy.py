import pandas as pd
from sklearn.metrics import mean_squared_error

scorePath = "./data/output_data/profession.train.result"
df = pd.read_csv(scorePath, names = ['name' , 'category' , 'trueScore', 'estScore'] , sep = '\t', encoding = 'utf-8')
mse = mean_squared_error(df['trueScore'], df['estScore'])
print("Mean sqaure error: :", mse)

# # Cross Validation Regression MSE
# import pandas
# from sklearn import cross_validation
# from sklearn.linear_model import LinearRegression
# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data"
# names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
# dataframe = pandas.read_csv(url, delim_whitespace=True, names=names)
# array = dataframe.values
# X = array[:,0:13]
# print(X)
# Y = array[:,13]
# num_folds = 10
# num_instances = len(X)
# seed = 7
# kfold = cross_validation.KFold(n=num_instances, n_folds=num_folds, random_state=seed)
# model = LinearRegression()
# scoring = 'mean_squared_error'
# results = cross_validation.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
# print("MSE: %.3f (%.3f)") % (results.mean(), results.std())
