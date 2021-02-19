from time import gmtime
import time
import shutil
import webbrowser
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import mechanize as m
import zipfile
import os
import pathlib
from pathlib import Path

br = m.Browser()

#waitTime_int is how many seconds you want the program to wait for the file
#to download before moving it
waitTime_int = 15

#interval_int is how many minutes the script will wait before executing
#GetData() again.  THIS VALUE MUST BE A DIVISOR OF 60!  Note that you
#will have to manually enter the minutes at which you want the script
#to grab the file, see the While Loop at the bottom of the script.
interval_int = 15

secondsPerMinute_int = 60

def GetData():
    gmTime = time.strftime("%Y%m%d%H%M", time.gmtime())
    dayHour = gmTime[0 : 10]
    minutes = gmTime[10 : 12]
    intervalCount_int = int(int(minutes) / interval_int)
    minutes_int = intervalCount_int * interval_int
    padding = "0" if minutes_int < 10 else ""
        #this code constructs the links for mechanize to grab files from
    dateTime = dayHour + padding + str(minutes_int) + "00"
    #these variables are the names of the files as listed on gdelt - these
        #are also the names that the files will be given once downloaded
    exportFileName = dateTime + ".export.CSV.zip"
    print(exportFileName)
    mentionsFileName = dateTime + ".mentions.CSV.zip"
    gkgFileName = dateTime + ".gkg.csv.zip"
        #these variables are the URLs at which each file can be found
    exportURL = "http://data.gdeltproject.org/gdeltv2/" + exportFileName
    mentionsURL = "http://data.gdeltproject.org/gdeltv2/" + mentionsFileName
    gkgURL = "http://data.gdeltproject.org/gdeltv2/" + gkgFileName
    print(exportURL)
        #this code uses mechanize to download then name the files
    br.retrieve(exportURL, filename=exportFileName)
    br.retrieve(mentionsURL, filename=mentionsFileName)
    br.retrieve(gkgURL, filename=gkgFileName)
        #this code waits for the specified time to ensure the files were successfully downloaded
    time.sleep(waitTime_int)
        #dir is the filepath to the folder containing this python application
    dir = "C:/Users/Garrison/Documents/13th Grade/geoparsing/SUMMER/"
        #initialDir is the filepath for where the files are downloaded by default
    initialDir = dir + "GDELTFinalDataGetter/GDELTFinalDataGetter/"
        #sourcePaths show where the files naturally end up once downloaded
    exportSourcePath = initialDir + exportFileName
    mentionsSourcePath = initialDir + mentionsFileName
    gkgSourcePath = initialDir + gkgFileName
        #destPaths show where you want the files to be moved/unzipped to
    exportDestPath = dir + "UnzippedExports"
    print(exportDestPath)
    mentionsDestPath = dir + "DLoadedFiles"
    gkgDestPath = dir + "DLoadedFiles"
        #this code unzips the desired files to their destPath
    with zipfile.ZipFile(exportSourcePath, 'r') as zip_ref:
        zip_ref.extractall(exportDestPath)
        #this code moves the desired files to their destPath
    shutil.move(mentionsSourcePath, mentionsDestPath)
    shutil.move(gkgSourcePath, gkgDestPath)
    time.sleep(10)
    #this code removes the folders that have already been unzipped
    os.remove(exportSourcePath)
    time.sleep(10)
    dataframe = pd.read_csv(Path(exportDestPath + "/" + dateTime + ".export.CSV"), encoding = "iso-8859-1", sep='\t', lineterminator='\n')
    print(dataframe)

while (True):
    currentTime = int(time.strftime("%M", time.gmtime()))
    if ((currentTime % interval_int) == 0):
        time.sleep(180)
        GetData()
