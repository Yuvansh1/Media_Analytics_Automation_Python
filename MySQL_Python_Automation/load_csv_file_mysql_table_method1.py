import csv
import MySQLdb
from datetime import datetime

conn = MySQLdb.connect(host='*****', user='****', passwd='****', db='**')
with open('C:/Users/New User/Desktop/tmp.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row['date'], row['****'], row['****'])
        row['new_date'] = datetime.strptime(row['date'], '%m/%d/%Y %H:%M').strftime('%Y-%m-%d')
        print(row['new_date'])
        conn = MySQLdb.connect(host='*****', user='****', passwd='****', db='**')
        sql_statement = "INSERT IGNORE INTO *** VALUES (%s,%s,%s)"
        cur = conn.cursor()
        cur.executemany(sql_statement,[(row['date'], row['****'], row['****'])])
        conn.escape_string(sql_statement)
        conn.commit()
print("CSV has been imported into the database")
