#Import Packages
import fnmatch
import pysftp
import os
import pandas as pd
from datetime import datetime
from zipfile import ZipFile
import glob, os
from openpyxl import load_workbook

today_date = datetime.today().strftime("%Y%m%d") #Current date with format
#today_date = datetime.strptime('2020-08-10', '%Y-%m-%d').strftime("%Y%m%d")
df = pd.DataFrame() #Create Empty Dataframe
#Set Path before executing workflow
path = 'C:/Users/yuvbhard/Downloads/New Folder/'
#To remove all files from directory initially
test = 'C:/Users/yuvbhard/Downloads/New Folder/*'
r = glob.glob(test)
for i in r:
   os.remove(i)

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  
with pysftp.Connection('********', username='********', password='********', cnopts=cnopts) as sftp:
    with sftp.cd('data'):
         for filename in sftp.listdir():
                if fnmatch.fnmatch(filename, "*.zip") and fnmatch.fnmatch(filename, today_date + "*") and fnmatch.fnmatch(filename, "*[FIle Name]*"):
                    sftp.get(filename,path+ "\\" + filename)
                    with ZipFile(path+ "\\" + filename, 'r') as zip:
                        csv_file = zip.extractall(path)
                        df = pd.read_csv(path+"********.csv")