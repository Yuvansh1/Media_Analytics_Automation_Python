 # importing Pandas library 
 # pip install mysql-connector
import pandas as pd 
import os
import mysql.connector

mySQLconnection = mysql.connector.connect(host='****',
								 database='****',
								 user='****',
								 password='****')

cursor = mySQLconnection.cursor()

cursor.execute("select * from **** where date(date) > '2016-01-01' and date(date) <= '2016-03-31'")
df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
df.to_csv('C:/Users/New User/Desktop/out10.csv', index=False)
print("File is saved in Download Folder of your system !!")