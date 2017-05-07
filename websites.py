'''
    Right now this is just a sample configuration:
    It tracks the course website of Pavel's Weighted inequalities
    while ignoring Peter Scholze's newest awards.
'''

from website import Website, Check, Pdfs_check, Notifier, Mail_notifier


wi = Website("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [Check("col1_content")], [Notifier()])
#wi = Website("weighted_inequalities", "http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/", [Check("col1_content")], [Notifier(), Mail_notifier("julian.weigt@>mail.com")])

sites = [ wi ]
