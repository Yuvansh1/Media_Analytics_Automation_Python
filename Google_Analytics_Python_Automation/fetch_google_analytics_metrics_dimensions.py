"""Hello Analytics Reporting API V4."""
import pandas as pd
import pygsheets
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
#KEY_FILE_LOCATION = '<REPLACE_WITH_JSON_FILE>'
#VIEW_ID = '<REPLACE_WITH_VIEW_ID>'
KEY_FILE_LOCATION = 'C:/Users/New User/Desktop/ga_credentials.json'
VIEW_ID = '****'

DIMENSIONS = ["ga:date","ga:sourceMedium","ga:campaign","ga:city","ga:deviceCategory","ga:landingPagePath"]
METRICS = ["ga:sessions","ga:goal4Completions"]

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """

  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '3daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression':i} for i in METRICS],
          'dimensions': [{'name':j} for j in DIMENSIONS]
#          'metrics': [{'expression': 'ga:sessions','ga:goal4Completions'}],
#          'dimensions': [{'name': 'ga:date','ga:sourceMedium','ga:campaign','ga:city','ga:deviceCategory','ga:landingPagePath'}]
        }]
      }
  ).execute()

def print_response(response):
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
      
      
    dataFrameFormat = pd.DataFrame(finalRows)
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    print_response(response)
    df = convert_to_dataframe(response)
    export_to_sheets(df)
    df.to_csv("C:/Users/New User/Desktop/out.csv", index=False)

def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  df = print_response(response)   #df = pandas dataframe
  export_to_sheets(df)                  #outputs to spreadsheet. comment to skip
  print(df)                             
  df = convert_to_dataframe(response)
  export_to_sheets(df)
  df.to_csv("C:/Users/New User/Desktop/out.csv", index=False)

if __name__ == '__main__':
  main() 
