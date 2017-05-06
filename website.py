'''
    Right now this is just a sample configuration:
    It tracks the course website of Pavel's Weighted inequalities
    while ignoring Peter Scholze's newest awards.
'''

# Returns the absolute path of the directory in which snapshots of websites are stored.
# Right now this is "data/" relative to the path of the script.
def path_to_data_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "data")

data_dir = path_to_data_dir()
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Returns the absolute path of the file in which snapshots of the given website are stored.
def path_to_file(filename):
    return os.path.join(path_to_data_dir(), filename)

class Check:
    _html_doc
    _html_doc_old
    _dir
    def compare()
            
    def check(html_doc, html_doc_old, dir):
        self._html_doc = html_doc
        self._html_doc_old = html_doc_old
        self._dir = dir

        return compare()
    

class Tag_content(Check):
    _tag_id
    def __init__(self, tag_id):
        self._tag_id = tag_id

    def compare():

        soup_old = BeautifulSoup(_html_doc_old, 'html.parser')
        soup_new = BeautifulSoup(_html_doc, 'html.parser')
    # So far we can only extract tags that have an id. May change this later.
        soup_old.find(id=_tag_id).prettify()
        soup_new.find(id=_tag_id).prettify()


class Website:
    def __init__(self, name, url, checks):
        self.name = name
        self.url = url
        self.checks = checks
        self._dir = path_to_file(name)
        self._filename = os.path.join(dir,name)
# Fetches the website and returns the relevant part as a BeautifulSoup object.

    def store_data():
        f = open(filename, "w")
        f.write(html_doc)
        f.close()

    # Fetches the stored snapshot of a website.
    def _fetch_old_data():
        try:
            f = open(filename)
            _html_doc_old = f.read()
            f.close()
        except FileNotFoundError: 


            #data = BeautifulSoup(f.read(), 'html.parser').prettify()
    def check(self):
        html_doc = urllib.request.urlopen(url)
        fetch_old_data()

        notification=""

        i=0

        for check in checks:
            checkdir=os.path.join(dir,i)
            notification+=check.check(_html_doc,_html_doc_old,checkdir)
            i++

        if notification != "":
            store_data

        for notifier in notifiers:
            notifier.notify(notification)

# Saves the given data as the new snapshot of a website
