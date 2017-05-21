#!/usr/bin/python3

'''
    Websitecheck

    Use Python 3.
    
'''

#import os   # for determining file and directory paths

import os.path
from config import cache_dir,sites  # list of tracked websites, directory of websitecheck's cache

#make sure cache dir exists
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

for site in sites:
    
    # Display identifiers of tracked websites for debugging purposes
    print(site.name + ":")
    site.check(cache_dir)

