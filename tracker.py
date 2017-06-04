import urllib.request  # for fetching websites
'''
    BeautifulSoup is not in the Python standard library.
    Need to install python-beautifulsoup4 in Arch Linux.
'''
from bs4 import BeautifulSoup   # for HTML parsing

# for file system operations
from os.path import join as join_path, exists

from selectors import Selector
from checkers import Checker


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
                data_new = a.select(data)    # call the selector
                my_selectionsDone = selectionsDone + [a]
            elif isinstance(a, Checker):   # This action is a notifier.
                data_new = data
                my_selectionsDone = selectionsDone

                # determine cache directory for the current query
                selstr = '.'.join(list(map(lambda s: repr(s), selectionsDone)))
                c_dir = join_path(self.w_dir, self.url.replace("/", "%2F"), selstr) 

                if exists(c_dir):
                    a.check(self.name, self.url, data_new, c_dir)

                else:
                    print("New website added: "+self.name)
                    makedirs(c_dir)
                    a.check(self.name, self.url, data_new, c_dir, silent=True)


            self.__iterate__(data_new, my_selectionsDone, actionsPending[1:])
