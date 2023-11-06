import snowflake.connector
import pandas as pd
import pygsheets
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import glob
import re
import s3fs
import datetime
from datetime import datetime



import pdb; pdb.set_trace()
key = 'AKIA3VSWBZ65MYZK4JJC'
secret = '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'
bytes_to_write = df.to_csv(None).encode()
# bytes_to_write = df.to_csv('s3://snowflakecsvfiles/session_evaluation/session_evaluation1.csv', index=False)
fs = s3fs.S3FileSystem(key=key, secret=secret)
with fs.open('s3://snowflakecsvfiles/session_evaluation/session_evaluation.csv', 'wb') as f: f.write(bytes_to_write)
conn.cursor().execute("""COPY INTO fivetran1_bi.session_evaluation FROM s3://snowflakecsvfiles/session_evaluation/session_evaluation.csv
	CREDENTIALS = (aws_key_id='AKIA3VSWBZ65MYZK4JJC',aws_secret_key='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') FILE_FORMAT=(field_delimiter=',')""".format(aws_access_key_id=key,aws_secret_access_key=secret))
