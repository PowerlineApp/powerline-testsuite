import urllib, urllib2
import requests
import json

class powerline(object):

    def __init__(self, username, password, base_url):
        self.token = None

        self.username = username
        self.password = password
        self.base_url = base_url + "/api"

    def post(self, route, data=None, h=None):
        """ POST request """
        kwargs = {}
        headers = {'Content-Type': 'application/json', 'Token' : self.token}
        if h:
            headers.update(h)
        if data:
            kwargs['data'] = data
            #return requests.post(self.base_url + route, headers=headers, data=data, verify=False)
        return requests.post(self.base_url + route, headers=headers, verify=False, **kwargs)

    def get(self, route, h=None, params=None):
        """ GET request """
        kwargs = {}
        headers = {'Content-Type': 'application/json', 'Token' : self.token}
        if h: headers.update(h)
        if params:
            kwargs['params'] = params
        return requests.get(self.base_url + route, headers=headers, verify=False, **kwargs)

    def delete(self, route, h=None):
        """ DELETE request """
        headers = {'Content-Type': 'application/json', 'Token' : self.token}
        if h: headers.update(h)
        return requests.delete(self.base_url + route, headers=headers, verify=False)

    def login(self):
        """ Primary login """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth = urllib.urlencode({ 'username': self.username, 'password' : self.password })
        req = self.post("/secure/login", auth, headers)
        self.token = req.json()['token']
        return self.token

    def fb_login(self):
        """ facebook login

            NEEDS UPDATE """

        auth = { 'facebook_token': self.fb_token, 'facebook_id' : self.fb_id }
        req = self.request("/secure/facebook/login", urllib.urlencode(auth))
        req.add_header('Content-Type','application/x-www-form-urlencoded')
        rsp = urllib2.urlopen(req)
        d = rsp.read()
        self.token = json.loads(d)['token']
        rsp.close()
        return d

    def user_info(self, uid):
        """ Get the user info """
        r = self.get("/profile/info/{uid:d}".format(uid=uid))
        return r.json()

    def user_group(self):
        r = self.get("/groups/user-groups/")
        return r.json()

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
        return d

    def list_groups(self):
        """ List all groups """
        r = self.get("/groups/")
        return r.json()

    def popular_groups(self):
        """ Return popular groups """
        r = self.get("/groups/popular")
        return r.json()

    def new_groups(self):
        """ Return new groups """
        r = self.get("/groups/new")
        return r.json()

    def create_group(self, group_data):
        """ Create a group """
        if not group_data:
            raise Exception("Group data must be given")
        r = self.post("/groups/", json.dumps(group_data) )
        return r

    def join_group(self, gid, data=None):
        """ Join a group by id """
        r = self.post("/groups/join/{gid:d}".format(gid=gid), data )
        return r.json()

    def unjoin_group(self, gid):
        """ Unjoin a group by id """
        r = self.delete("/groups/join/{gid:d}".format(gid=gid))
        return r.json()

    def get_group(self, gid):
        """ Get group data by id """
        if not gid:
            raise Exception("Group id must be given")
        r = self.get("/groups/info/{gid:d}".format(gid=gid))
        return r.json()

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

    def get_micropetition(self, mid):
        """ Get micropetition by id """
        r = self.get("/micro-petitions/{mid:d}".format(mid=mid) )
        return r.json()

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

