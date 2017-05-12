from os.path import expanduser
from website import Website, Check, Check_tag_name, Pdfs_check, Notifier, Mail_notifier

cache_dir = expanduser("~/.websitecheck")

wi = Website("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [Check("col1_content")], [Notifier()])
aae = Website("app_alg_exercise", "http://www.or.uni-bonn.de/lectures/ss17/appr_ss17_ex.html", [Check_tag_name("body")], [Notifier()])

sites = [ wi, aae ]
