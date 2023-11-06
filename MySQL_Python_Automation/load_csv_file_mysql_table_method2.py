import csv
import MySQLdb
from datetime import datetime



connection = MySQLdb.connect(host='*****', user='***', passwd='****', db='**')
cursor = connection.cursor()

import pdb; pdb.set_trace()
query = "LOAD DATA INFILE 'C:/Users/New User/Desktop/nnnp.csv' INTO TABLE **** FIELDS TERMINATED BY ';' ENCLOSED BY '\"' ESCAPED BY '\\\\'"
cursor.execute( query )
print("CSV has been imported into the database")
connection.commit()