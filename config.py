from os.path import abspath, dirname, join
from tracker import Tracker
from selectors import FindAll
from checkers import Diff, Filechange

target_address = ""
home = dirname(abspath(__file__))
cache_dir = join(home,'.websitecheck')

wi = Tracker("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [FindAll(id="col1_content"),Diff(),Filechange('pdf'),Filechange('djvu')])
aae = Tracker("app_alg_exercise", "http://www.or.uni-bonn.de/lectures/ss17/appr_ss17_ex.html", [FindAll(["body","ul"]),Diff(),Filechange('pdf')])
aa = Tracker("app_alg", "http://www.or.uni-bonn.de/lectures/ss17/appr_ss17.html", [FindAll("body"),Diff()])
st = Tracker("models_of_set_theory", "http://www.math.uni-bonn.de/ag/logik/teaching/2017SS/Models_of_set_theory_1.shtml", [FindAll(id="content"),Diff(),Filechange('pdf')])

sites = [ wi, aae, aa, st ]
