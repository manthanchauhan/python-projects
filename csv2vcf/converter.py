import pandas
import os

def convert_to_vcf(datafile):
    outputfile = datafile[:-4] + 'vcard.txt'
    vcf = open(outputfile, "w+")
    df = pandas.read_csv(datafile)
    for indx, row in df.iterrows():
        vcf.write('BEGIN:VCARD\nVERSION:3.0\n')
        vcf.write('FN:' + row['Name'] + '\n')
        vcf.write('N:;' + row['Name'] + ';;;\n')
        try:
            vcf.write('EMAIL;TYPE=INTERNET;TYPE=HOME:' + row['Email'] + '\n')
        except:
            pass
        vcf.write('TEL;TYPE=CELL:' + str(int(row['Contact'])) + '\n')
        vcf.write('END:VCARD\n')
    vcf.close()
    os.rename(outputfile, datafile[:-3] + 'vcf')

if __name__=='__main__':
    datafile = 'C:\\Users\\manth\\OneDrive\\Techtronix\\Recruitment.csv'
    convert_to_vcf(datafile)    



