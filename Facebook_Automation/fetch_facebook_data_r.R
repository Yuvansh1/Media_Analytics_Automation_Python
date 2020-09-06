library(rfacebookstat)
library(lubridate)
library(reticulate)
#library(RMySQL)
# Auth
account="act_*****"
token <- "*****"
# Get statistic
Campaign_s <- fbGetMarketingStat(accounts_id = account,
                                 breakdowns = "region",
                                 level = "campaign", fields = "campaign_id,campaign_name,impressions,reach,clicks,spend",
                                 interval = "day",request_speed = "fast",date_start = '2019-03-01', date_stop = '2019-03-31',api_version = "v3.3",
                                 access_token = token)
#today_date <- Sys.Date()
df = write.csv(Campaign_s,paste0("C:/Users/New User/Desktop/campaign_", today_date ,".csv"), row.names=F)
#source_python("C:/Users/New User/Desktop/Snowflake/nntp.py")
#insert_to_snowflake <- ads_googly(Campaign_s,"fb_region")