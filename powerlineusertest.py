# -----------------------------------
#   USER TEST SUITE
# -----------------------------------
#
#   This is the base class for all tests. This should be boiler plate
#   stuff that all tests could use.
#
#   All test cases should extend this class

import powerline
import unittest
import ConfigParser
import os
import sys
import mailgun

try:
    import requests
except ImportError:
    print "requests mod is needed to use the powerline user testsuite "
    sys.exit(1)

PLCFG       = os.path.join( os.getcwd(), "powerline.cfg")
USER_SEC    = "user"
MYSQL_SEC   = "mysql"
MAILGUN_SEC = "mailgun"

class PowerlineUserTests(unittest.TestCase):

    config   = None
    username = None
    password = None
    url      = None
    api      = None

    myuser   = None
    mypass   = None
    mydbname = None
    myhost   = None

    mailgun  = None

    @classmethod
    def setUpClass(cls):
        """ Pre class execution """
        cls.config = ConfigParser.ConfigParser()
        cls.config.read(PLCFG)

        cls.username    = cls.config.get(USER_SEC, 'username')
        cls.password    = cls.config.get(USER_SEC, 'password')
        cls.url         = cls.config.get(USER_SEC, 'url')

        if cls.config.has_section(MYSQL_SEC):
            cls.myuser      = cls.config.get(MYSQL_SEC, 'user')
            cls.mypass      = cls.config.get(MYSQL_SEC, 'password')
            cls.mydbname    = cls.config.get(MYSQL_SEC, 'dbname')
            cls.myhost      = cls.config.get(MYSQL_SEC, 'host')

        if cls.config.has_section(MAILGUN_SEC):
            cls.mg_key  = cls.config.get(MAILGUN_SEC, 'private')
            cls.mailgun = mailgun.MailGunApi(cls.mg_key)

        cls.api = powerline.powerline(cls.username, cls.password, cls.url)
        cls.api.login()



