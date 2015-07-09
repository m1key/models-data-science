import pandas as pd

data = pd.read_csv('../models-to-csv/result.csv')

# Highest prices:
print data.sort('price', ascending = False).head()

# Most expensive models:
print data.groupby('model').mean().sort('price', ascending = False).head()
