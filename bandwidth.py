#!/usr/bin/python

import argparse
import subprocess
import json
from subprocess import call
from time import gmtime, strftime
import time
import re

parser = argparse.ArgumentParser(description='Tool to gather load page time data.')

parser.add_argument('urlfile', help='a file containing the list of url to open')
parser.add_argument('bwrate', help='the bandwith rate under which the load will operate. \
                    refer to tc documentation for syntax')
parser.add_argument('runs', help='the number of run you want to perform', type=int)
                     

args = parser.parse_args()

#Modify constants here
rawdata = '/var/www/html/bandwidth/raw_data.json'
wd      = '/home/max/codeZ/bandwidth/'
data    =  wd + 'data.json'
chrome  = '/opt/google/chrome/google-chrome'
    
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

        #make sure that all pages have been load to manipulate raw_data.json
        time.sleep(8)
            
        #parse raw_data and build a structure to calculate the mean 
        index_run = c + 1
        data_serie[args.bwrate][index_run] = {}

        with open(rawdata, 'r') as rd:
            lines = rd.readlines()
            for line in range(offset + 1, offset + url_nb + 1):
                #print 'reading from ' + str(offset + 1) + ' to ' + str(offset + url_nb)
                parsed    = lines[line].rstrip('\r\n')
                sparsed   = re.split(' : ', parsed)
                data_serie[args.bwrate][index_run][sparsed[0]] = sparsed[1]

    #create a backup for the runs serie
    backup_file = wd + args.bwrate + '_' + strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    cmd = 'touch ' + backup_file
    subprocess.call(cmd, shell=True);
    with open(backup_file, 'w') as bck:
         bck.write(json.dumps(data_serie))

    return 1


def operateMean():
    return 1


requester()
