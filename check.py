#!/usr/bin/python3

'''
    Websitecheck

    Use Python 3.
    
'''

#import os   # for determining file and directory paths
#home = os.path.dirname(os.path.abspath(__file__))

from os.path import join as join_path
from config import cache_dir,sites  # list of tracked websites, directory of websitecheck's cache

#make sure cache dir exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

for site in sites:
    
    # Display identifiers of tracked websites for debugging purposes
    print(site.name + ": ", end = '')
    site.check(join_path(cache_dir,site.name))

