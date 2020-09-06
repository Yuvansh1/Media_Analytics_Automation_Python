library("RAdwords")
library(RMySQL)
library(dplyr)

load("C:/Users/New User/Desktop/Snowflake/****.RData")

##click, cost ,impression,
##CTR , session, evaluation, appointment , verified appointment , purchase , inspection
body2 <- statement(select = c('Date','AdGroupId','AdGroupName', 'CampaignId','CampaignName', 'Impressions', 'Clicks', 'Cost'),
                  report = "ADGROUP_PERFORMANCE_REPORT",
                  #report = "CAMPAIGN_PERFORMANCE_REPORT",
                  #report = "GEO_PERFORMANCE_REPORT",

                  start = Sys.Date()-1,
                  end = Sys.Date()-1)

data2 <- getData(clientCustomerId = '****',
                google_auth = google_auth,
                statement = body2)
colnames(data2)<-c("NEW_DATE","CAMPAIGN_ID","CAMPAIGN","AD_GROUP_ID","AD_GROUP","IMPRESSIONS","CLICKS","COST")


#Run Python file through R
#source_python("C:/Users/New User/Desktop/Snowflake/nntp.py")
#insert_to_snowflake <- ads_googly(data1,"adwords_brand_adgroup")
