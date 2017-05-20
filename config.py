from os.path import expanduser
from tracker import Tracker
import selectors

target_address = ""
cache_dir = expanduser("~/.websitecheck")

wi = Tracker("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [FindAll(id="col1_content")])
aae = Tracker("app_alg_exercise", "http://www.or.uni-bonn.de/lectures/ss17/appr_ss17_ex.html", [FindAll("body")])

sites = [ wi, aae ]
