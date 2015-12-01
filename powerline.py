import urllib, urllib2
import requests
import json

class powerline(object):

    def __init__(self, username, password, base_url):
        self.token = None
        self.group_id = None

        self.username = username
        self.password = password
        self.base_url = base_url + "/api"

    def post(self, route, data=None, h=None):
        headers = {'Content-Type': 'application/json', 'Token' : self.token}
        if h:
            headers.update(h)
        if data:
            return requests.post(self.base_url + route, headers=headers, data=data, verify=False)
        return requests.post(self.base_url + route, headers=headers, verify=False)

    def get(self, route, h=None):
        headers = {'Content-Type': 'application/json', 'Token' : self.token}
        if h: headers.update(h)
        return requests.get(self.base_url + route, headers=headers, verify=False)

    def delete(self, route, h=None):
        headers = {'Content-Type': 'application/json', 'Token' : self.token}
        if h: headers.update(h)
        return requests.delete(self.base_url + route, headers=headers, verify=False)

    def login(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth = urllib.urlencode({ 'username': self.username, 'password' : self.password })
        req = self.post("/secure/login", auth, headers)
        self.token = req.json()['token']
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
                'first_name': '',
                'last_name':'',
                'password': self.passwd,
                'confirm': self.passwd,
                'address1':'7 Faith Ln',
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

    def list_groups(self):
        r = self.get("/groups/")
        return r.json()

    def create_group(self, group_data):
        r = self.post("/groups/", group_data)
        #self.group_id = r.json()['id']
        print r.json()
        print "Create group status: ",r.status_code
        print
        return self.group_id

    def join_group(self, gid, data=None):
        r = self.post("/groups/join/{gid:d}".format(gid=gid), data )
        print r.json()

    def unjoin_group(self, gid):
        r = self.delete("/groups/join/{gid:d}".format(gid=gid))
        print r.json()

    def create_micropetition(self, d):
        r = self.post("/micro-petitions", json.dumps(d) )
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

