import snowflake.connector
import pandas as pd
import numpy as np
import csv
from snowflake.connector import DictCursor
from datetime import datetime
from sqlalchemy import create_engine

#import pdb; pdb.set_trace()
conn = snowflake.connector.connect(user='*******',password='*******',account='*******',role='READ_ONLY',warehouse='*******',database='*******')
sql_statement = "select * from ******* limit 10"
cur = conn.cursor()
df = pd.DataFrame(cur.fetchall())
#print(df)

df = df.reset_index(drop = True)	
engine =create_engine("**************")
connection = engine.connect()
for k in range(0,len(df),13999):
	temp_df = df[k:k+13999]
	temp_df.to_sql(name='*******',con=connection, if_exists='append', index=False)