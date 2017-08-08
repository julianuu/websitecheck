import os.path
from tracker import Tracker
from selectors import FindAll
from checkers import Diff, Filechange

target_address = ""
home = os.path.dirname(os.path.abspath(__file__))
#cache_dir = os.path.expanduser("~/.websitecheck")
cache_dir = os.path.join(home,'.websitecheck')

wi = Tracker("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [FindAll(id="col1_content"),Diff(),Filechange('pdf'),Filechange('djvu')])
ha = Tracker("harmonic_analysis", "http://www.math.uni-bonn.de/people/wrobel/S4B1_WS_1718.html", [FindAll(id="col1_content"),Diff(),Filechange('pdf')])
#ss = Tracker("summer_school", "http://www.math.uni-bonn.de/people/thiele/workshop19/", [Diff(),Filechange('pdf')])
ss = Tracker("summer_school", "http://www.math.uni-bonn.de/people/thiele/workshop19/", [Diff()])
st = Tracker("models_of_set_theory", "http://www.math.uni-bonn.de/ag/logik/teaching/2017SS/Models_of_set_theory_1.shtml", [FindAll(id="content"),Diff(),Filechange('pdf')])
ba = Tracker("Bäder", "http://www.bonn.de/tourismus_kultur_sport_freizeit/baeder/aktuelles/index.html?lang=de", [FindAll(id="inhaltRechtsUnten"),Diff()])
sp = Tracker("Sport", "https://www.sport.uni-bonn.de/", [FindAll(id="portal-column-content"),Diff()])

sites = [ wi, ha, ss, st, ba, sp ]
