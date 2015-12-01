#!/usr/bin/python

# A quick example of how to use the powerline module
#
# This will simply login, join a group with a passcode
# and unjoin.
#
# ----------------------------------------------------
# Replace:
#   username = your client username
#   password = your password
#   url      = url of the powerline backend api
#

import powerline

username = 'test'
password = 'pass'
url = "https://api.localhost"

group_id = 101
passcode = { 'passcode' : 'passcode' }

p = powerline.powerline(username,password,url)
p.login()
p.join_group(group_id, passcode)
p.unjoin_group(group_id)
