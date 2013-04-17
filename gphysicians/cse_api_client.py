#!/usr/bin/env python
#
# Client for unofficial CSE API.

import cookielib
import json
import logging
import urllib 
import urllib2
import urlparse

obf_gaia_id = "015533284649053097143"
cse_id = "eyct-samxvy"
cx = obf_gaia_id + ":" + cse_id

cookie_jar = cookielib.CookieJar()

class AuthRedirectHandler(urllib2.HTTPRedirectHandler):
    def requires_auth(self, headers):
        if not "location" in headers:
            return False
        return headers.getheaders("location")[0].startswith(
            "http://www.google.com/accounts/ServiceLogin")
    
    def http_error_302(self, req, fp, code, msg, headers):
        if self.requires_auth(headers):
            response = self.authenticate(req.get_full_url())
            logging.info("Completed 3 step auth")
            return response

        return urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)

    def authenticate(self, redirect_url):
        """Three step process to authenticate as a real user."""
        # Step 1 - ClientLogin
        fields = {
            "Email": "sumedsearch@gmail.com",
            "Passwd": "plyCEC01",
            "service": "cprose"
            }
        response = self.parent.open(urllib2.Request(
            url="https://www.google.com/accounts/ClientLogin",
            data=urllib.urlencode(fields)))
        
        # Step 2 - IssueAuthToken
        target_fields = [ "SID", "LSID" ]
        fields = { 
            "service": "gaia"
        }
        for line in response.read().split():
            k, v = line.split("=")
            if k in ["SID", "LSID"]:
                fields[k] = v

        response = self.parent.open(urllib2.Request(
            url="https://www.google.com/accounts/IssueAuthToken",
            data=urllib.urlencode(fields)))

        # Step 3 - TokenAuth
        fields = { 
            "auth": response.read().rstrip(),
            "service": "cprose",
            "continue": redirect_url
        }

        return self.parent.open(urllib2.Request(
            url="https://www.google.com/accounts/TokenAuth",
            data=urllib.urlencode(fields)))


opener = urllib2.build_opener(AuthRedirectHandler,
                              urllib2.HTTPCookieProcessor(cookie_jar))
xsrf_token = None
def clear_xsrf_token():
    global xsrf_token
    xsrf_token = None

def get_xsrf_token():
    global xsrf_token
    if xsrf_token:
        return xsrf_token

    xsrf_url = "http://www.google.com/cse/setup/basic?cx=" + cx
    response = opener.open(xsrf_url)
    
    # This is hack and should go in AuthRedirectHandler 
    if response.geturl().startswith("https://accounts.google.com/CheckCookie"):
        response = opener.open(xsrf_url)

    # ugly hack parsing
    html = response.read()    
    magic = "var annotationsXsrf='"
    index_a = html.find(magic)
    if index_a == -1:
        raise Exception("magic string for XSRF parsing not found")

    index_a += len(magic)
    index_b = html.find("'", index_a)
    xsrf_token = html[index_a:index_b]
    logging.info("Got XSRF token: " + xsrf_token)
    return xsrf_token    

def label_request(label):
    print label.mode

    url = ("http://www.google.com/cse/api/%s/annotations/%s?xsrf=%s"
           % (obf_gaia_id, cse_id, get_xsrf_token()))

    headers = {"Content-type": "application/json"}
    if label.mode == "site":
        headers["X-MakeUrlPattern"] = "true"
        about = urlparse.urlparse(label.url).netloc
    else:
        about = label.url

    data = json.dumps({
        "Add": { 
            "Annotations": {
                "Annotation": [{
                    "about": about,
                    "label": [{"name": "_cse_" + cse_id},
                              {"name": label.label}]
                }]
            }
        }
    })

    return urllib2.Request(url, data, headers)

def add_label(label):
    num_tries = 2
    for i in range(num_tries):
        try: 
            result = opener.open(label_request(label))
            # Success
            return
        except urllib2.HTTPError as e:
            # On a 400, try to refresh the XSRF token and retry
            if e.code == 400 and i != num_tries - 1:
                logging.info("Got 400 when POSTing label, retrying")
                clear_xsrf_token()
                continue

            # On any other error give up
            raise e
    

                      
        
        

                
                
                            
