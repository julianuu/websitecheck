import os.path
from tracker import Tracker
from selectors import FindAll
from checkers import Diff, Filechange

target_address = ""
home = os.path.dirname(os.path.abspath(__file__))
#cache_dir = os.path.expanduser("~/.websitecheck")
cache_dir = os.path.join(home,'.websitecheck')

ha = Tracker("harmonic_analysis", "http://www.math.uni-bonn.de/people/wrobel/S4B1_WS_1718.html", [FindAll(id="col1_content"),Diff(),Filechange('pdf')])
re = Tracker("regularity", "http://www.math.uni-bonn.de/ag/ana/WiSe1718/reg-max/", [FindAll(id="col1_content"),Diff()])
sa = Tracker("stochastic_analysis", "https://wt.iam.uni-bonn.de/kaveh-bashiri/teaching/introduction-to-stochastic-analysis/", [FindAll(id="c2144"),Diff(),Filechange('pdf')])
ss = Tracker("summer_school", "http://www.math.uni-bonn.de/people/thiele/workshop19/", [Diff()])
ba = Tracker("Bäder", "http://www.bonn.de/tourismus_kultur_sport_freizeit/baeder/aktuelles/index.html?lang=de", [FindAll(id="inhaltRechtsUnten"),Diff()])
sp = Tracker("Sport", "https://www.sport.uni-bonn.de/", [FindAll(id="portal-column-content"),Diff()])

sites = [ ha, re, sp , ss, ba, sa]
