#!/usr/bin/env python

#
# issue #33
#

import json
import unittest
import powerlineusertest
import ConfigParser
import os
import MySQLdb

class GroupMembershipTest(powerlineusertest.PowerlineUserTests):

    gid = None
    uid = None

    @classmethod
    def insertJoin(cls):
        insert_join= """ INSERT INTO users_groups (user_id, group_id, created_at, status)
                         VALUES (%s, %s, NOW(), %s) """
        uid_sql = """ SELECT id FROM user WHERE username = '{}' """.format(cls.username)
        join_sql = """ SELECT id FROM users_groups WHERE user_id = {} and group_id = {}"""

        # get the uid
        cur = cls.db.cursor()
        cur.execute(uid_sql)
        cls.uid = int(cur.fetchone()[0])

        # make sure i join the right group
        cur.execute(join_sql.format(cls.uid, cls.gid))
        c = cur.fetchone()
        if c is None:
            cur.execute(insert_join,( cls.uid,cls.gid,1) )
            cls.db.commit()
        cur.close()

    @classmethod
    def insertGroup(cls):

        insert_group = """ INSERT INTO groups (group_type, username, password, salt, created_at)
                           VALUES ( %s, %s, %s, %s, NOW() ) """
        delete = """ DELETE FROM groups where username = 'testmembership' """
        select_group = """ SELECT id FROM groups WHERE username = 'testmembership'"""

        cur = cls.db.cursor()
        cur.execute(select_group)
        c = cur.fetchone()
        if c is None:
            cur.execute(insert_group,( 0,'testmembership',0,0) )
            cls.db.commit()
            cls.gid = cur.lastrowid
        else:
            cls.gid = int(c[0])
        cur.close()

    @classmethod
    def setUpClass(cls):
        """ Pre class execution """
        super(GroupMembershipTest, cls).setUpClass()
        cls.db = MySQLdb.connect(
            host=cls.myhost,
            user=cls.myuser,
            passwd=cls.mypass,
            db=cls.mydbname)
        cls.insertGroup()
        cls.insertJoin()

    def test_getMembership(self):
        """ Get the user membership of a group """
        compare = [{u'username': u'austin', u'first_name': u'Austin', u'last_name': u'Papp', u'id': self.uid}]
        resp = self.api.get('/groups/{group}/users'.format(group=self.gid))
        d = resp.json()
        self.assertEqual(d , compare)

if __name__ == "__main__":
    unittest.main()
