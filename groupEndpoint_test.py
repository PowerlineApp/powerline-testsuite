#!/usr/bin/env python
#
# -------------------------------
#   Group API functional tests
# -------------------------------
#
#   This tests the full group API
#
#


from pprint import pprint
import unittest
import powerlineusertest
import MySQLdb

class CreateGroupApiTest(powerlineusertest.PowerlineUserTests):

    mailgun_list    = "foobar@powerlinegroups.com"
    user            = "foo"

    @classmethod
    def setUpClass(cls):
        super(CreateGroupApiTest, cls).setUpClass()
        cls.db = MySQLdb.connect(
            host=cls.myhost,
            user=cls.myuser,
            passwd=cls.mypass,
            db=cls.mydbname)

    def setUp(self):
        sql = "DELETE FROM groups WHERE username = %s"
        cur = self.db.cursor()
        cur.execute(sql,(self.user,))
        self.db.commit()

        try:
            self.mailgun.delete_mail_list(self.mailgun_list)
        except:
            pass

    def tearDown(self):
        sql = "DELETE FROM groups WHERE username = %s"
        cur = self.db.cursor()
        cur.execute(sql,(self.user,))
        self.db.commit()

    def test_createGroup(self):
        """ Create a group """
        group = {
            "manager_first_name"   : "Foo",
            "manager_last_name"    : "Bar",
            "manager_email"        : "foo@example.com",
            "manager_phone"        : "99999",
            "username"             : "foo",
            "official_description" : "foo yourself",
            "official_type"        : "Educational",
            "official_title"       : "Foo Bar" }
        resp = self.api.create_group( group )
        self.assertEqual( resp.status_code, 201)

class GroupApiTests(powerlineusertest.PowerlineUserTests):

    gid         = None
    db          = None
    fail_me     = None
    field       = "testField"
    group_user  = "unittestGroup"
    mglist      = "unittestGroup@powerlinegroups.com"
    email       = "austin@powerli.ne"

    @classmethod
    def setUpClass(cls):
        super(GroupApiTests, cls).setUpClass()
        cls.db = MySQLdb.connect(
            host=cls.myhost,
            user=cls.myuser,
            passwd=cls.mypass,
            db=cls.mydbname)

        try:
            c.delete_group()
        except:
            # Skip if can't delete
            pass

        try:
            cls.insert_group()
            if not cls.mailgun.is_mail_list(cls.mglist):
                print "craeting list"
                cls.mailgun.create_mail_list(cls.mglist)
            cls.set_group_id()
        except Exception as e:
            print e
            cls.fail_me = e

        print "test is using group ",cls.gid

    @classmethod
    def tearDownClass(cls):
        try:
            cls.delete_group()
            if cls.mailgun.is_mail_list(cls.mglist):
                cls.mailgun.delete_mail_list(cls.mglist)
        except Exception as e:
            print e
            cls.fail_me = e

    @classmethod
    def insert_group(cls):
        """ Insert a test group """
        sql = """ INSERT INTO groups (group_type, username, password, salt, created_at, official_name)
                  VALUES (%s, %s, %s, %s, NOW(), %s) """
        cur = cls.db.cursor()
        cur.execute(sql,(0, cls.group_user, "pass", "salt", "unittest group" ) )
        cls.db.commit()

    @classmethod
    def delete_group(cls):
        """ Delete the group """
        sql = "DELETE FROM groups WHERE username = %s"
        cur = cls.db.cursor()
        try:
            cur.execute(sql,(cls.group_user,))
        except:
            pass
        cls.db.commit()

    @classmethod
    def set_group_id(cls):
        """ Set the group id """
        cur = cls.db.cursor()
        cur.execute("SELECT id FROM groups WHERE username = '{g:s}'".format(g=cls.group_user) )
        cls.gid = int(cur.fetchone()[0])

    def setUp(self):
        """ Setup """
        if self.fail_me:
            self.fail(self.fail_me)

    def tearDown(self):
        self.delete_join()
        self.delete_required_field()

        try:
            self.mailgun.delete_list_member(self.mglist, self.email)
        except:
            pass

    def delete_join(self):
        sql = "DELETE FROM users_groups WHERE group_id = {g:d}".format(g=self.gid)
        cur = self.db.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print e
        self.db.commit()

    def add_join(self, status=1):
        sql = """ INSERT INTO users_groups ( user_id, group_id, created_at, status)
                  VALUES (%s, %s, NOW(), %s)"""
        uid = self.get_username_id()
        cur = self.db.cursor()
        cur.execute(sql, (uid, self.gid, status) )
        self.db.commit()

    def get_username_id(self):
        sql = "SELECT id FROM user WHERE username = '{u:s}'".format(u=self.username)
        cur = self.db.cursor()
        cur.execute(sql)
        return int(cur.fetchone()[0])

    def add_required_field(self):
        sql = "INSERT INTO groups_fields ( group_id, field_name ) VALUES ( %s, %s ) "
        cur = self.db.cursor()
        cur.execute(sql, (self.gid, self.field) )
        self.db.commit()

    def delete_required_field(self):
        sql = "DELETE FROM groups_fields WHERE field_name = '{rf:s}'".format(rf=self.field)
        cur = self.db.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print e
        self.db.commit()

    def test_listGroups(self):
        """ list of groups """
        self.assertTrue(self.api.list_groups())

    def test_popularGroups(self):
        """ popular groups """
        self.assertTrue(self.api.popular_groups())

    def test_newGroups(self):
        """ new groups """
        self.assertTrue(self.api.new_groups())

    def test_userGroup(self):
        """ User groups"""
        self.assertTrue(self.api.user_groups())

    def test_groupInfo(self):
        """ Group Info """
        self.assertTrue(self.api.group_info(self.gid))

    def test_groupInvites(self):
        """ Group invites """
        self.assertTrue(self.api.group_info(self.gid))

    def test_invitesApproval(self):
        """ Group Invites """
        pass

    def test_groupRequiredFields(self):
        """ Group Required Fields """
        self.add_required_field()
        self.assertTrue(self.api.group_required_fields(self.gid))

    def test_groupUsers(self):
        """ Group users """
        self.add_join()
        self.assertTrue( self.api.group_users(self.gid) )

    def test_joinGroupNoPassword(self):
        """ join group with no password """
        r = self.api.join_group(self.gid)
        self.assertEqual( r['status'], 1 )

    def test_joinGroupWithPassword(self):
        """ Joing group with a password """
        pass

    def test_joinGroupWithApproval(self):
        """ Join group pending approval """
        pass

    def test_joinGroupWithRequiredField(self):
        """ Join group with required fields """
        pass

    def test_unjoinGroup(self):
        """ Unjoin group """
        self.add_join()
        self.mailgun.add_list_member(self.mglist, self.email)
        r = self.api.unjoin_group(self.gid)
        self.assertEqual( r["success"], "ok")

if __name__ == "__main__":

    suite = unittest.TestSuite()

    suite.addTest(CreateGroupApiTest("test_createGroup"))

    suite.addTest(GroupApiTests("test_listGroups"))
    suite.addTest(GroupApiTests("test_popularGroups"))
    suite.addTest(GroupApiTests("test_newGroups"))
    suite.addTest(GroupApiTests("test_userGroup"))
    suite.addTest(GroupApiTests("test_groupInfo"))
    #suite.addTest(GroupApiTests("test_groupInvites"))
    #suite.addTest(GroupApiTests("test_invitesApproval"))
    suite.addTest(GroupApiTests("test_groupRequiredFields"))
    suite.addTest(GroupApiTests("test_groupUsers"))
    suite.addTest(GroupApiTests("test_joinGroupNoPassword"))
    #suite.addTest(GroupApiTests("test_joinGroupWithPassword"))
    #suite.addTest(GroupApiTests("test_joinGroupWithApproval"))
    #suite.addTest(GroupApiTests("test_joinGroupWithRequiredField"))
    suite.addTest(GroupApiTests("test_unjoinGroup"))

    unittest.TextTestRunner(verbosity=2).run(suite)
