import urllib.request  # for fetching websites
'''
    BeautifulSoup is not in the Python standard library.
    Need to install python-beautifulsoup4 in Arch Linux.
'''
from bs4 import BeautifulSoup   # for HTML parsing

# for file system operations
from os import listdir, remove, makedirs
from os.path import isfile, exists, basename
from os.path import join as join_path

from selectors import Selector
from notifiers import Notifier


# Tracks a (part of a) Website
class Tracker:
    def __init__(self, name, url, actions):
        self.name = name
        self.url = url
        self.actions = actions


    def check(self, w_dir):
        self.w_dir = w_dir
        # fetch new data
        with urllib.request.urlopen(self.url) as response:
            data = [BeautifulSoup(response, 'html.parser')]

        # start the recursion
        self.__iterate__(data, [], self.actions)


    def __iterate__(self, data, selectionsDone, actionsPending):
        if len(actionsPending) == 0:
            return  # leave because we are at a leaf

        actions = actionsPending[0]
        if not isinstance(actions, list):
            actions = [actions]

        for a in actions:
            if isinstance(a, Selector):     # This action is a selector.
                my_data = a.select(data)    # call the selector
                my_selectionsDone = selectionsDone + [a]
            elif isinstance(a, Notifier):   # This action is a notifier.
                my_data = data
                my_selectionsDone = selectionsDone

                # determine cache directory for the current query
                selstr = '.'.join(list(map(lambda s: repr(s), selectionsDone)))
                my_dir = join_path(self.w_dir, self.url.replace("/", "%2F"), selstr) 

                if exists(my_dir):
                    # fetch old data
                    old_files = sorted([f for f in listdir(my_dir) if isfile(join_path(my_dir,f))], key=int)
                    old_paths = [join_path(my_dir, f) for f in old_files]
                    old_data = []
                    for p in old_paths:
                        with open(p, 'r') as old_file:
                            old_data.append(BeautifulSoup(old_file, 'html.parser')) 
                    # call the notifier
                    a.notify(name, url, selectionsDone, old_data, my_data)
                    
                    # remove old snippets from cache
                    for p in old_paths:
                        remove(p)
                else:
                    print("New website added: "+self.name)
                    makedirs(my_dir)

                # store new snippets in cache
                for idx, snippet in enumerate(data):
                    with open(join_path(my_dir, str(idx)), 'w') as new_file:
                        new_file.write(snippet.prettify())

            self.__iterate__(my_data, my_selectionsDone, actionsPending[1:])
