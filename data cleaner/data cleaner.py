def correct_names(df, sorter):
    names = list(df[sorter])
    l = len(names)
    for i in range(0, l):
        names[i] = names[i].split()
        li = len(names[i])
        for j in range(0, li):
            names[i][j] = names[i][j][0].upper() + names[i][j][1:].lower()
        s = names[i][0]
        li = len(names[i])
        for j in range(1, li):
            s = s + ' ' + names[i][j]
        names[i][0] = s
    names = [l[0] for l in names]
    return names

import pandas
import os

datafile = 'D:\Git\python-projects\data cleaner\data.csv'
outputfile = 'D:\Git\python-projects\data cleaner\dataout.csv'
columns_to_drop = [0, 1]
column_names = ['Enrollment No.', 'Name', 'Group']
Sno_add = True
sorter = 'Name'

df = pandas.read_csv(datafile)
df[sorter] = correct_names(df, sorter)
df.sort_values(by= sorter, axis= 0, ascending= True, inplace=True)
df.drop(labels=df.columns[columns_to_drop], axis=1, inplace= True)
df.columns = column_names
rows = df.shape[0]
if Sno_add:
    df.insert(loc= 0, column= 'S. No', value= range(1, rows + 1))
df.to_csv(outputfile, index=False)
os.remove(datafile)
os.rename(outputfile, datafile)
print('Sorted')