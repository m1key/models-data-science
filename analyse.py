import pandas as pd

data = pd.read_csv('../models-to-csv/result.csv')

print "Highest prices:"
print data.sort('price', ascending = False).head()

print "Most expensive models:"
print data.groupby('model').mean().sort('price', ascending = False).head()

print "Most expensive for each model:"
print data.groupby('model')['price'].max().head()

print "Most expensive for each model, getting the data frame:"
def max_price(group):
	return group.loc[group['price'] == group['price'].max()]

most_expensive_for_each_model = data.groupby('model', as_index = False).apply(max_price).reset_index(drop=True)
print most_expensive_for_each_model

def min_price(group):
	return group.loc[group['price'] == group['price'].min()]

print "Least expensive for each model:"
least_expensive_for_each_model = data.groupby('model', as_index = False).apply(min_price).reset_index(drop = True)
print least_expensive_for_each_model

print "Most expensive for each model, where just one category exists:"
most_expensive_standalone = most_expensive_for_each_model.groupby('model').filter(lambda x: len(x) == 1).sort(['price', 'category', 'model'])
print most_expensive_standalone

print "Least expensive for each model, where just one category exists:"
least_expensive_standalone = least_expensive_for_each_model.groupby('model').filter(lambda x: len(x) == 1).sort(['price', 'category', 'model'])
print least_expensive_standalone

print "Most expensive for each model, where just one category exists, starting with S:"
print most_expensive_standalone[most_expensive_standalone['category'].str.startswith('S')].sort(['category', 'price'])

print "Most commonly most expensive:"
print most_expensive_standalone.groupby('category').agg(['mean', 'count'])['price'].sort(['count', 'mean'])

print "Most commonly least expensive:"
print least_expensive_standalone.groupby('category').agg(['mean', 'count'])['price'].sort(['count', 'mean'], ascending = True)

print "Biggest difference:"
def difference(group):
	group['difference'] = group['price'].max() - group['price'].min()
	return group
print data.groupby('model', as_index = False).apply(difference).reset_index(drop = True).sort('difference').drop_duplicates(cols = 'model')[['model', 'difference']]

print "Most expensive for each model containing a string:"
print most_expensive_for_each_model[most_expensive_for_each_model['category'].str.contains("all P")]

print "Standard deviation:"

pd.set_option('display.float_format', lambda x: '%.3f' % x)
print data.groupby('model')['price'].std().order(ascending = False)

print "Least to most specialised, subset of columns:"
print data.groupby(['model']).count().sort('category')['category']

print "Where most expensive contains the word Black"
most_expensive_bm = most_expensive_standalone[most_expensive_standalone['category'].str.contains("Black")]

print "All for those above"
print data[data['model'].isin(most_expensive_bm['model'])]

print "STD and mean for those for whom most expensive category contains Black:"
print data[data['model'].isin(most_expensive_standalone[most_expensive_standalone['category'].str.contains("Black")]['model'])].groupby(['model']).agg(['mean', 'std'])

print "Sort by STD:"
print data[data['model'].isin(most_expensive_standalone[most_expensive_standalone['category'].str.contains("p Off")]['model'])].groupby(['model']).agg(['std', 'mean']).sort([('price', 'std')])

withS = data[data['category'].str.startswith('Sma')]
allWithS = data[data['model'].isin(withS['model'])]
allWithS.groupby('model').count().reset_index().sort(['price'])

data[data['model'].isin(data[data['category'].str.startswith('Bla')]['model'])].groupby('model').count().reset_index().sort(['price'])
