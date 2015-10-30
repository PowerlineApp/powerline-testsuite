#!/usr/bin/python
#
# simple script i use to work with the powerline api

import powerline
p = powerline.powerline()
p.login()

# offset test
page = { 'offset' : 1, 'limit':2}
a = p.get_page_activities(page)
for x in a:
    for k,v in x.iteritems():
        print "%s   : %s"%(k, v)

# activities
a = p.get_activities()
for x in a:
    print
    for k,v in x.iteritems():
        print "%s   : %s"%(k, v)
