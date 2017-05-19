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


# Selects the first tag with the given id.
# (Html id's should be unique in a document.)
class Id(Selector):
    def __init__(self, html_id):
        self.html_id = html_id

    def select(self, data):
        for soup in data:
            el = soup.find(id=self.html_id)
            if el != None:
                return [el]
        return []

    def __repr__(self):
        return 'id(' + self.html_id + ')'
