# cleanup tickets.csv
# the 7.2k lines is actually 20k lines
import csv
with open('tickets.csv',encoding='utf-8') as f:
    reader = csv.reader(f)
    with open('output.csv', 'a+',encoding='utf-8') as g:
        for row in reader:
            g.write("\n")
            g.write(row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+","+row[6]+row[7])
    g.close()
f.close()