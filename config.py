import os.path
from tracker import Tracker
from selectors import FindAll
from notifiers import Diff

target_address = ""
home = os.path.dirname(os.path.abspath(__file__))
#cache_dir = os.path.expanduser("~/.websitecheck")
cache_dir = os.path.join(home,'.websitecheck')

wi = Tracker("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [FindAll(id="col1_content"),Diff()])
aae = Tracker("app_alg_exercise", "http://www.or.uni-bonn.de/lectures/ss17/appr_ss17_ex.html", [FindAll("body"),Diff()])

sites = [ wi, aae ]
