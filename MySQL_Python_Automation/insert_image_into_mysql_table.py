import mysql.connector


conn = mysql.connector.connect(host='*****', user='****', passwd='****', db='**')

photo = open("photo.png")
show_photo = photo.read()
#To fetch data using mysql connection
cur = conn.cursor()
cur.execute("INSERT into DATABASE.TABLE values (1, %s)", (show_photo,))
conn.commit()
print('Images insert Successfully!!')

#Image will store in BLOB format in DB