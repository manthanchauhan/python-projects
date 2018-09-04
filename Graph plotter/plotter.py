import pandas as pd
import matplotlib.pyplot as plt
from sys import path
path.append('D:\\Git\\python-projects\\data cleaner\\')
from data_cleaner import cleaner

datafile= 'D:\Git\python-projects\Graph plotter\data.csv'
cleaner(datafile=datafile,drop=False, columns_by_labels=False, col_to_drop= [], column_names=['year', 'submit time'], Sno_add=False, sorter='submit time')

