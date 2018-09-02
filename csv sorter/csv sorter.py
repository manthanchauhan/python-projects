import pandas
#datafile = 'D:\Git\python-projects\csv sorter\data.csv'
datafile = '/home/manthan/Git/python-projects/email-sender/data.csv'
#outputfile = 'D:\Git\python-projects\csv sorter\dataout.csv'
outputfile = '/home/manthan/Git/python-projects/email-sender/data.csv'
df = pandas.read_csv(datafile)
df.sort_values(by='name', axis = 0, ascending=True, inplace= True)
df.to_csv(outputfile)
print('Sorted')