#
# issue #34
#
import json
import powerlineusertest
import unittest
import MySQLdb

class FriendFinderTest(powerlineusertest.PowerlineUserTests):

    email_hash = None

    @classmethod
    def setUpClass(cls):
        """ class execution """
        super(FriendFinderTest, cls).setUpClass()

        # TODO:
        #   Insert a test user
        db = MySQLdb.connect(
            host=cls.myhost,
            user=cls.myuser,
            passwd=cls.mypass,
            db=cls.mydbname)
        sql = """ SELECT email_hash FROM user WHERE username = '{}' """.format(cls.username)
        cur = db.cursor()
        cur.execute(sql)
        cls.email_hash = cur.fetchone()[0]

    def test_getFriends(self):
        """ Assert provided email hash is linked to existing
            email account"""
        compare = [{u'username': u'austin', u'first_name': u'Austin', u'last_name': u'Papp', u'birth': u'09/27/1982', u'country': u'usa', u'avatar_file_name': u'https://52.5.45.80/bundles/civixfront/img/default_user.png', u'full_name': u'Austin Papp', u'id': 50}]
        params = {'emails[]' : self.email_hash, 'limit':10, 'page':1}
        resp = self.api.get('/search/friends', params=params)
        d = resp.json()
        self.assertEqual(d, compare)

if __name__ == "__main__":
    unittest.main()
