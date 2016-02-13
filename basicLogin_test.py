
# BASIC USER LOGIN TEST

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
        api = powerline.powerline(self.username, self.password, self.url)
        self.assertTrue( api.login() )
