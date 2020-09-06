import time
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
import pandas as pd
import numpy as np
from time import sleep
from facebook_business.adobjects.campaign import Campaign as AdCampaign
from facebook_business.adobjects.user import User
from facebook_business.adobjects.ad import Ad
from datetime import datetime
from datetime import timedelta

def video_col_data(string,df):
    col_name = string.split('_')[1] + "_3"
    df = df.astype(str).str.split('/|:|,|}|]',expand=True).add_prefix(string.split('_')[1]+ "_")    
    df2 = df[col_name].astype(str).str.replace("'",'').str.replace("None",'0').str.strip()
    return df2




my_app_id = "********"
my_app_secret = "********"
my_access_token = "********"

FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token, api_version='v7.0')

start= "2020-04-22"
end= "2020-05-03"

act = AdAccount('act_********')
params = {'time_increment' : 1,'time_range': {'since': start , 'until': end}, 'level' : 'ad',
          'breakdowns' : ['publisher_platform','platform_position','device_platform']}

fields = ['ad_name','adset_name','campaign_name',
    'impressions','clicks','video_thruplay_watched_actions',
          'video_continuous_2_sec_watched_actions',
    'video_p25_watched_actions', 'video_p50_watched_actions','estimated_ad_recall_rate', 
    'video_p75_watched_actions', 'video_p95_watched_actions', 
    'video_p100_watched_actions', 'website_purchase_roas',
    'spend','inline_link_clicks','unique_inline_link_clicks','video_play_actions','actions']
async_job = act.get_insights(params=params, fields = fields, is_async=True)
#Insights
df = pd.DataFrame()
async_job.api_get()
while async_job[AdReportRun.Field.async_status] != 'Job Completed' or async_job[AdReportRun.Field.async_percent_completion] < 100:
    time.sleep(1)
    async_job.api_get()      


df = pd.DataFrame(async_job.get_result())
df.head()
