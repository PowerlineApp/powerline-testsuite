
import sys

try:
    import requests
except ImportError:
    print "requests mod is necessary for mailgun use"
    sys.exit(1)

class MailGunApi(object):

    url = "https://api.mailgun.net/v3"

    def __init__(self, key):
        self.key  = key
        self.auth = ("api",self.key)

    def is_mail_list(self, mglist):
        r = requests.get(
            "https://api.mailgun.net/v3/lists/{mglist:s}".format(mglist=mglist),
            auth=self.auth)
        if r.status_code != 200:
            return False
        return True

    def delete_mail_list(self, mglist):
        """ Delete a mailgun mail list """
        r = requests.delete(
            "https://api.mailgun.net/v3/lists/{mglist:s}".format(mglist=mglist),
            auth=self.auth)
        if r.status_code != 200:
            raise Exception("Could not delete list {l:s}".format(l=mglist))
        return

    def create_mail_list(self, mglist):
        """ Create a mailgun mail list """
        r = requests.post(
            "{url:s}/lists".format(url=self.url),
            auth=self.auth,
            data={"address" : mglist,
                  "description" : "test"} )
        if r.status_code != 200:
            raise Exception("Could not create list {l:s}".format(l=mglist))
        return

    def add_list_member(self, mglist, email):
        """ Add a member to the list """
        r = requests.post(
            "{url:s}/lists/{mglist:s}/members".format(url=self.url, mglist=mglist),
            auth = self.auth,
            data = { "subscribed" : True,
                     "address" : email,
                     "name" : "",
                     "description" : "idk"} )
        if r.status_code != 200:
            raise Exception("Could not add {e:s} to list {l:s}".format(e=email, l=mglist))
        return

    def delete_list_member(self, mglist, email):
        """ Delete a member from a list """
        r = requests.delete(
            "{url:s}/lists/{mglist:s}/members/{email:s}".format(url=self.url, mglist=mglist, email=email),
            auth = self.auth )
        if r.status_code != 200:
            raise Exception("Could not delete {e:s} to list {l:s}".format(e=email, l=mglist))
        return

