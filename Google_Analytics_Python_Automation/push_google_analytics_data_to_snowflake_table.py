#pip install --upgrade google-api-python-client
#pip install oauth2client
#pip install pandas
#pip install --upgrade snowflake-sqlalchemy
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
from snowflake.connector import DictCursor
from sqlalchemy import create_engine


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'C:/Users/New User/Desktop/ga_credentials.json'
VIEW_ID = '*****'
page_size = "2000001"

DIMENSIONS = ["ga:date","ga:sourceMedium","ga:campaign","ga:city","ga:deviceCategory","ga:landingPagePath"]
METRICS = ["ga:sessions","ga:goal4Completions"]

def initialize_analyticsreporting():
	credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
	analytics = build('analyticsreporting', 'v4', credentials=credentials)
	return analytics

def get_report(analytics):
	return analytics.reports().batchGet(
		body={
			'reportRequests': [
			{
				'viewId': VIEW_ID,
				'pageSize': page_size,
				# 'dateRanges': [{'startDate': '2daysAgo', 'endDate': 'today'}],
				'dateRanges': [{'startDate': '2019-06-14', 'endDate': '2019-06-15'}],
				'metrics': [{'expression':i} for i in METRICS],
				'dimensions': [{'name':j} for j in DIMENSIONS]
			}]
		}).execute()


def convert_to_dataframe(response):
	for report in response.get('reports', []):
		columnHeader = report.get('columnHeader', {})
		dimensionHeaders = columnHeader.get('dimensions', [])
		metricHeaders = [i.get('name',{}) for i in columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])]
		finalRows = []
	

		for row in report.get('data', {}).get('rows', []):
			dimensions = row.get('dimensions', [])
			metrics = row.get('metrics', [])[0].get('values', {})
			rowObject = {}
		
			for header, dimension in zip(dimensionHeaders, dimensions):
				rowObject[header] = dimension
			
			for metricHeader, metric in zip(metricHeaders, metrics):
				rowObject[metricHeader] = metric

			finalRows.append(rowObject)
			rowObject['ga:date'] = datetime.strptime(rowObject['ga:date'], '%Y%m%d').strftime('%Y-%m-%d')
	dataFrameFormat = pd.DataFrame(finalRows)
	return dataFrameFormat      
		


def main():
	analytics = initialize_analyticsreporting()
	response = get_report(analytics)
	df = convert_to_dataframe(response)
	print(df)
	df.to_csv('C:/Users/New User/Desktop/out3.csv', index=False)
	df = df.reset_index(drop = True)	
	engine =create_engine("******")
	connection = engine.connect()
	for k in range(0,len(df),10000):
		temp_df = df[k:k+9999]
		temp_df.to_sql(name='*****',con=connection, if_exists='append', index=False)

	print('Data Saved in Snowflake Session Evaluation Table!')

if __name__ == '__main__':
	main()