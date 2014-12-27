#!/usr/bin/python

import argparse
import subprocess
import json
from subprocess import call
from time import gmtime, strftime
import time
import re
import pdb

parser = argparse.ArgumentParser(description='Tool to gather load page time data.')

parser.add_argument('urlfile', help='a file containing the list of url to open')
parser.add_argument('bwrate', help='the bandwith rate under which the load will operate. \
                    refer to tc documentation for syntax')
parser.add_argument('runs', help='the number of run you want to perform', type=int)
                     

args = parser.parse_args()

#Modify constants here
rawdata    = '/var/www/html/bandwidth/raw_data'
wd         = '/home/max/codeZ/bandwidth/'
data       =  wd + 'data.json'
chrome     = '/opt/google/chrome/google-chrome'
serie_time = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    
def requester():
    #get url list and call them through chrome
    with open(args.urlfile, 'r') as uf:
        urlz = uf.readlines()

    #open chrome
    cmd = '/opt/google/chrome/google-chrome --ignore-certificate-errors &'
    subprocess.call(cmd, shell=True)

    #this arbitrary timer allow the first openened tab to send data to the php listener
    #the following write allow to get ride of this data
    #FIXME: /!\ load can take more than 2 scd ... /!\ 
    time.sleep(2)

    #write trash into the file to start at line 1 :)
    with open(rawdata, 'w') as rd:
        rd.write(args.bwrate + "\n")
    
    url_nb = len(urlz)
    data_serie = {}
    data_serie[args.bwrate] = {}

    for c in range(0, args.runs):
        offset = c * url_nb
        for url in urlz:
            print 'loading ' + url
            subprocess.call('/opt/google/chrome/google-chrome --ignore-certificate-errors ' + url,
                            shell=True);

        #FIXME: make sure that all pages have been load to manipulate raw_data.json
        time.sleep(8)
            
        #parse raw_data and build a structure to calculate the mean 
        index_run = c + 1
        data_serie[args.bwrate][index_run] = {}

        with open(rawdata, 'r') as rd:
            lines = rd.readlines()
            for line in range(offset + 1, offset + url_nb + 1):
                #print 'reading from ' + str(offset + 1) + ' to ' + str(offset + url_nb)
                parsed     = lines[line].rstrip('\r\n')
                sparsed    = re.split(' : ', parsed)
                format_url = re.sub('(http)s?://', '', sparsed[0])
                format_url = format_url.rstrip('/')
                data_serie[args.bwrate][index_run][format_url] = sparsed[1]

    #create a backup for the runs serie
    backup_file = wd + args.bwrate + '_all_runs_' + serie_time
    cmd = 'touch ' + backup_file
    subprocess.call(cmd, shell=True);
    with open(backup_file, 'w') as bck:
         bck.write(json.dumps(data_serie))

    return data_serie


def operateMean(data):
    #gather data for each url over all the runs and compute mean
    data_mean = {}
    data_mean[args.bwrate] = {}
    with open(args.urlfile, 'r') as uf:
        urlz = uf.readlines()
        for url in urlz:
            url = url.rstrip('\r\n')
            temp = 0.000 
            for run in range(1, args.runs + 1):
                temp += float(data[args.bwrate][run][url])
   
            mean_lt = temp / run
            print 'mean for ' + url + ' is ' + str(mean_lt)
            data_mean[args.bwrate][url] = str(mean_lt)
   
    #save the results into a file
    result_file = wd + args.bwrate + '_mean_' + serie_time 
    cmd = 'touch ' + result_file
    subprocess.call(cmd, shell=True)
    with open(result_file, 'w') as res:
        res.write(json.dumps(data_mean))

    return data_mean


data      = requester()
mean_data = operateMean(data)
