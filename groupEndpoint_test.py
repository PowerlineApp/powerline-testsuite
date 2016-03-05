#
# -------------------------------
#   Group API functional tests
# -------------------------------
#
#   This tests the full group API
#
#   TODO:
#       Write a mailgun api to delete lists
#


from pprint import pprint
import unittest
import powerlineusertest
import MySQLdb

class CreateGroupApiTest(powerlineusertest.PowerlineUserTests):

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
        cur.execute(sql,("foo",))
        self.db.commit()

        # TODO: delete group from mailgun

    def test_createGroup(self):
        """ Create a group """
        group = {
            "manager_first_name"  : "Foo",
            "manager_last_name"   : "Bar",
            "manager_email"       : "foo@example.com",
            "manager_phone"       : "99999",
            "username"            : "foo",
            "official_description" : "foo yourself",
            "official_type"       : "Educational",
            "official_title"      : "Foo Bar" }

        resp = self.api.create_group( group )
        if 'official_title' not in resp:
            self.fail("official title is not in the resp: {r:s}".format(r=resp))
        self.assertEqual( resp["official_title"], "Foo Bar")

class GroupApiTests(powerlineusertest.PowerlineUserTests):

    @classmethod
    def setUpClass(cls):
        super(GroupApiTests, cls).setUpClass()
        cls.db = MySQLdb.connect(
            host=cls.myhost,
            user=cls.myuser,
            passwd=cls.mypass,
            db=cls.mydbname)

    def setUp(self):
        sql = """ INSERT INTO groups (group_type, username, password, salt, created_at, official_name)
                  VALUES (%s, %s, %s, %s, NOW(), %s) """

        cur = self.db.cursor()
        cur.execute(sql,(0, "unittestGroup", "pass", "salt", "unittest group" ) )
        self.db.commit()

        cur.execute("SELECT id FROM groups WHERE username = 'unittestGroup'" )
        self.gid = int(cur.fetchone()[0])
        print self.gid

    def tearDown(self):
        sql = "DELETE FROM groups WHERE username = %s"
        cur = self.db.cursor()
        cur.execute(sql,("unittestGroup",))
        self.db.commit()

    def test_listGroups(self):
        self.assertTrue(self.api.list_groups())

    def test_popularGroups(self):
        self.assertTrue(self.api.popular_groups())

    def test_newGroups(self):
        self.assertTrue(self.api.new_groups())

    def test_userGroup(self):
        pass

    def test_groupInfo(self):
        pass

    def test_groupInvites(self):
        pass

    def test_invitesApproval(self):
        pass

    def test_groupRequiredFields(self):
        pass

    def test_groupUsers(self):
        pass

    def test_joinGroup(self):
        """
        tests:
            1. test join no password on group
            2. test join password on group
                1. adjust membership control to be private
            3. test join approval on group
                1. ajust memberhsip control to be private w/ approval
            3. test join with required field """
        pass

    def test_unjoinGroup(self):
        pass

if __name__ == "__main__":

    suite = unittest.TestSuite()

    #suite.addTest(CreateGroupApiTest("test_createGroup"))

    #suite.addTest(GroupApiTests("test_listGroups"))
    #suite.addTest(GroupApiTests("test_popularGroups"))
    #suite.addTest(GroupApiTests("test_newGroups"))
    #suite.addTest(GroupApiTests("test_userGroup"))
    #suite.addTest(GroupApiTests("test_groupInfo"))
    #suite.addTest(GroupApiTests("test_groupInvites"))
    #suite.addTest(GroupApiTests("test_invitesApproval"))
    #suite.addTest(GroupApiTests("test_groupRequiredFields"))
    #suite.addTest(GroupApiTests("test_groupUsers"))
    #suite.addTest(GroupApiTests("test_joinGroup"))
    #suite.addTest(GroupApiTests("test_unjoinGroup"))

    unittest.TextTestRunner(verbosity=2).run(suite)
