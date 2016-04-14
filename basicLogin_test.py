#!/usr/bin/env python

# BASIC USER LOGIN TEST
#
# This is also a quick example of how to handle
# a unit test and use the powerline test api

import powerline
import unittest
import ConfigParser
import os

PLCFG = "{path:s}/powerline.cfg".format(path=os.getcwd())
USER_SEC = 'user'

class BasicUserLoginTest(unittest.TestCase):

    def setUp(self):
        """ Pre class execution """
        config = ConfigParser.ConfigParser()
        config.read(PLCFG)
        self.username = config.get(USER_SEC, 'username')
        self.password = config.get(USER_SEC, 'password')
        self.url = config.get(USER_SEC, 'url')

    def test_login(self):
        """ Basic login test """
        api = powerline.powerline(self.username, self.password, self.url)
        token = api.login()
        self.assertTrue( token )

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(BasicUserLoginTest("test_login"))
    unittest.TextTestRunner(verbosity=2).run(suite)
