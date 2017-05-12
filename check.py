#!/usr/bin/python3

'''
    Websitecheck

    Use Python 3.
    
'''

import os   # for determining file and directory paths

#home directory
#from os.path import expanduser
#home = expanduser("~")
home = os.path.dirname(os.path.abspath(__file__))

#working directory
data_dir = os.path.join(home, ".websitecheck")
#make sure it exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def path_to_file(filename):
    return os.path.join(data_dir, filename)


from websites import sites  # import list of tracked websites

'''
    ================
    Functions
    ================
'''


# Notification function. Currently sends an email via some Gmail account.
'''
    ===============
    Main script
    ===============
'''

for site in sites:
    
    # Display identifiers of tracked websites for debugging purposes
    print()
    print(site.name + ": ", end = '')

    site.check(path_to_file(site.name))

