import csv
def read_data():
    filename = 'data.csv'
    contacts = []
    datafile = open(filename, 'r')
    datareader = csv.reader(datafile)
    fields = datareader.next()
    email_pos = -1
    name_pos = -1
    l = len(fields)
    for i in range(0, l):
        if fields[i] == 'name':
            name_pos = i
        elif fields[i] == 'email':
            email_pos = i
        if email_pos != -1 and name_pos != -1:
            break
    for row in datareader:
        name = row[name_pos]
        email = row[email_pos]
        contacts.append([name, email])
    return contacts
contacts = read_data()
for contact in contacts:
    print(contact[0], end = ' ')
    print(contact[1])


    
            