'''
    Right now this is just a sample configuration:
    It tracks the course website of Pavel's Weighted inequalities
    while ignoring Peter Scholze's newest awards.
'''

def path_to_data_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "data")

data_dir = path_to_data_dir()
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

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
    

class Tag(Check):
    _tag_id
    def __init__(self, tag_id):
        self._tag_id = tag_id

    def compare():

        soup_old = BeautifulSoup(_html_doc_old, 'html.parser')
        soup_new = BeautifulSoup(_html_doc, 'html.parser')
        text_old = soup_old.find(id=_tag_id).prettify()
        text_new = soup_new.find(id=_tag_id).prettify()

#diff would be nicer
        if text_old != tex_old
        return text_new

class Pdf_links(Check):
    _tag_id
    def __init__(self, tag_id):
        self._tag_id = tag_id

class Website:
    def __init__(self, name, url, checks):
        self.name = name
        self.url = url
        self.checks = checks
        self._dir = path_to_file(name)
        self._filename = os.path.join(dir,name)

    def store_data():
        f = open(filename, "w")
        f.write(html_doc)
        f.close()

    def _fetch_old_data():
        try:
            f = open(filename)
            _html_doc_old = f.read()
            f.close()
        except FileNotFoundError: 


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
