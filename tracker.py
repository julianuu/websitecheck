import urllib.request  # for fetching websites
from bs4 import BeautifulSoup   # for HTML parsing

# for file system operations
from os import makedirs
from os.path import join as join_path, exists

from selectors import Selector
from checkers import Checker

def pathify(s):
    return s.replace("/", "%2F")

class Tracker:
    def __init__(self, name, url, actions):
        self.name = name
        self.url = url
        self.actions = actions


    def check(self, w_dir):
        from config import html_parser

        # TODO: This is a hack, not good practice
        self.w_dir = w_dir

        # fetch new data
        with urllib.request.urlopen(self.url) as response:
            data = [BeautifulSoup(response, html_parser)]

        # start the recursion
        self.__iterate__(data, [], self.actions)


    # TODO: Maybe allow trees of actions
    # TODO: The current implementation of alternative actions does not make too much sense
    def __iterate__(self, data, selectionsDone, actionsPending):
        if len(actionsPending) == 0:
            return  # leave because we are at a leaf

        actions = actionsPending[0]
        # TODO: Currently, actions will almost never be a list because of the implementation
        if not isinstance(actions, list):
            actions = [actions]

        for a in actions:
            if isinstance(a, Selector):     # This action is a selector.
                data_new = a.select(data)    # call the selector
                my_selectionsDone = selectionsDone + [a]
            elif isinstance(a, Checker):   # This action is a checker.
                data_new = data
                my_selectionsDone = selectionsDone

                # determine cache directory for the current query
                selstr = '.'.join(list(map(lambda s: repr(s), selectionsDone)))
                c_dir = join_path(self.w_dir, pathify(self.url), pathify(selstr), pathify(repr(a))) 

                if exists(c_dir):
                    a.check(self.name, self.url, data, c_dir)

                else:
                    print("New website added: " + self.name)
                    makedirs(c_dir)
                    a.check(self.name, self.url, data, c_dir, silent=True)

            self.__iterate__(data_new, my_selectionsDone, actionsPending[1:])
