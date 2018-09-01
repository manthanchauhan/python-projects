import pandas
datafile = 'D:\Git\python-projects\csv sorter\data.csv'
outputfile = 'D:\Git\python-projects\csv sorter\dataout.csv'
df = pandas.read_csv(datafile)
df.sort_values(by='name', axis = 0, ascending=True, inplace= True)
df.to_csv(outputfile)
print('Sorted')