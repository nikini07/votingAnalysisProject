import csv

filepath = 'Data.csv'

with open(filepath, newline='') as csvfile:
    # The DictReader function of the csv module assumes each row to be a dictionary
    reader = csv.DictReader(csvfile)     

    for row in reader:
        # print(row['Constituency name'])
        print(row)

