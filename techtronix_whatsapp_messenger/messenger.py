import pandas
import os
import converter

import data_cleaner

datafile = 'Recruitment.csv'
# clean data of typeform------------------------------------------------------------------------------------------------
# data_cleaner.cleaner(datafile='Recruitment.csv', columns_by_labels=False, drop=True, col_to_drop=[0, 5, 6, 7],
#                      column_names=['Name' , 'Contact', 'Year', 'Theme'], Sno_add=True,
#                      sorter="Name")
print('Please perform a manual check')
manual_check = input()
# create vcf card-------------------------------------------------------------------------------------------------------
converter.convert_to_vcf(datafile)
# uploading vcf card----------------------------------------------------------------------------------------------------



