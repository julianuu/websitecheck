import os.path
from tracker import Tracker
from selectors import FindAll
from checkers import Diff

target_address = ""
home = os.path.dirname(os.path.abspath(__file__))
#cache_dir = os.path.expanduser("~/.websitecheck")
cache_dir = os.path.join(home,'.websitecheck')

wi = Tracker("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [FindAll(id="col1_content"),Diff()])
aae = Tracker("app_alg_exercise", "http://www.or.uni-bonn.de/lectures/ss17/appr_ss17_ex.html", [FindAll("body"),Diff()])
aa = Tracker("app_alg", "http://www.or.uni-bonn.de/lectures/ss17/appr_ss17.html", [FindAll("body"),Diff()])
st = Tracker("models_of_set_theory", "http://www.math.uni-bonn.de/ag/logik/teaching/2017SS/Models_of_set_theory_1.shtml", [FindAll(id="content"),Diff()])



sites = [ wi, aae, aa, st ]
