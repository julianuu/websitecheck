class Selector:
    # Select something from the given data, which is a list of
    # BeautifulSoup's. Must not modify the argument, but return
    # a NEW list.
    def select(data):
        raise NotImplementedError("Please implement this method")

    # Return a string which will be used to compose the directory
    # name associated to a query.
    def __repr__(self):
        raise NotImplementedError("Please implement this method")


# Passes on arguments to soup.findAll, i.e. you can call the constructor with the same arguments as you would call soup.findAll
class FindAll(Selector):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def select(self, data):
        for soup in data:
            els = soup.findAll(*self.args,**self.kwargs)
            return els

    def __repr__(self):
        arguments=''
        for arg in self.args:
            arguments = arguments+', '+arg
        for kw in self.kwargs:
            arguments = arguments+', '+kw+':'+self.kwargs[kw]
        return 'findAll(' + arguments + ')'
