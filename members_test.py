#!/usr/bin/env python

import json
import unittest
import powerlineusertest
import ConfigParser
import os
import MySQLdb

class MembersTest(powerlineusertest.PowerlineUserTests):

    def test_getMembers(self):
        """ Get the members of a group """
        compare = [{}]
        resp = self.api.get('/members')
        d = resp.json()
        self.assertEqual(d , compare)

if __name__ == "__main__":
    unittest.main()
