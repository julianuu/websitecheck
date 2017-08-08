#!/usr/bin/python3

'''
    Websitecheck

    Use Python 3.
    
'''

from os import makedirs
from os.path import exists
from config import sites, cache_dir  # list of tracked websites, directory of websitecheck's cache

# make sure cache dir exists
if not exists(cache_dir):
    makedirs(cache_dir)

for site in sites:
    # Display identifiers of tracked websites for debugging purposes
    print(site.name + ":")
    site.check(cache_dir)
