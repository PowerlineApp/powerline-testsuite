import urllib, urllib2
import json

class powerline(object):

    #base_url = "http://192.168.10.100/api"
    base_url = "https://api-staging.powerli.ne/api"
    username = None
    passwd = None
    fb_token = None     # use if facebook login test
    fb_id = None        # use if facebook login test

    def __init__(self):
        self.token = None
        self.group_id = None

    def request(self, url, data=None):
        return urllib2.Request(self.base_url + url, data)

    def login(self):
        auth = { 'username': self.username, 'password' : self.passwd }
        req = self.request("/secure/login", urllib.urlencode(auth))
        req.add_header('Content-Type','application/x-www-form-urlencoded')
        rsp = urllib2.urlopen(req)
        d = rsp.read()
        self.token = json.loads(d)['token']
        rsp.close()
        print "logged in"

    def fb_login(self):
        auth = { 'facebook_token': self.fb_token, 'facebook_id' : self.fb_id }
        req = self.request("/secure/facebook/login", urllib.urlencode(auth))
        req.add_header('Content-Type','application/x-www-form-urlencoded')
        rsp = urllib2.urlopen(req)
        d = rsp.read()
        self.token = json.loads(d)['token']
        rsp.close()
        print "logged in"

    def create_user(self):
        d = {
                'username': self.username,
                'first_name': 'Herbie',
                'last_name':'Hancock',
                'password': self.passwd,
                'confirm': self.passwd,
                'address1':'7 Yup  Ln',
                'city':'Ardsley',
                'state':'NY',
                'country':'US',
                'zip':10502,
                'email':'sample@example.com',
                'phone':'999SAMPLE' }
        r = self.request("/secure/registration", urllib.urlencode(d))
        r.add_header('Content-Type','application/x-www-form-urlencoded')
        rsp = urllib2.urlopen(r)
        d = rsp.read()
        self.token = json.loads(d)['token']
        rsp.close()
        print "created user"

    def create_group(self, d):
        r = self.request("/groups/", json.dumps(d) )
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)

        print rsp
        print "create group code: ",rsp.getcode()
        group = rsp.read()
        self.group_id = group['id']
        rsp.close()
        return self.group_id

    def join_group(self, gid, data):
        r = self.request("/groups/join/{gid:d}".format(gid=gid), json.dumps(data) )
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)
        print "join group code: ",rsp.getcode()

    def create_micropetition(self, d):
        r = self.request("/micro-petitions", json.dumps(d) )
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)
        j = rsp.read()
        rsp.close()
        return json.loads(j)

    def delete_micropetition(self, id):
        r = self.request("/micro-petitions/{0}".format(id) )
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        r.get_method = lambda: 'DELETE'
        rsp = urllib2.urlopen(r)
        rsp.close()
        print "delete micro code: ",rsp.getcode()

    def get_micropetition(self, id):
        r = self.request("/micro-petitions/{0}".format(id) )
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)
        j = rsp.read()
        rsp.close()
        return json.loads(j)

    def get_social_activities(self):
        r = self.request("/social-activities/")
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)
        j = rsp.read()
        rsp.close()
        return json.loads(j)

    def get_activities(self):
        r = self.request("/activities/")
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)
        j = rsp.read()
        rsp.close()
        return json.loads(j)

    def get_page_activities(self, d):
        url = "/activities?offset={0}&limit={1}".format(d['offset'], d['limit'])
        r = self.request(url)
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)
        j = rsp.read()
        rsp.close()
        return json.loads(j)

    def follow(self, id):
        r = self.request("/activities/")
        r.add_header('Content-Type', 'application/json')
        r.add_header("Token", self.token)
        rsp = urllib2.urlopen(r)

