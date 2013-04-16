
import logging
import urllib 
import urllib2
import cookielib

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
            return self.authenticate(req.get_full_url())

        return urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)

    def authenticate(self, redirect_url):
        """Three step process to authenticate as a real user."""
        # Step 1 - ClientLogin
        fields = {
            "Email": "sumedsearch@gmail.com",
            "Passwd": # fill in password
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
def get_xsrf_token():
    global xsrf_token
    if xsrf_token:
        return xsrf_token

    xsrf_url = "http://www.google.com/cse/setup/advanced?cx=" + cx
    response = opener.open(xsrf_url)
    
    # This is hack and should go in AuthRedirectHandler 
    if response.geturl().startswith("https://accounts.google.com/CheckCookie"):
        response = opener.open(xsrf_url)

    # ugly hack parsing
    html = response.read()    
    magic = "var annotationsXsrf='"
    index_a = html.find(magic)
    if index_a == -1:
        raise Exception("magic string not found")

    index_a += len(magic)
    index_b = html.find("'", index_a)
    xsrf_token = html[index_a:index_b]
    logging.info("Got XSRF token: " + xsrf_token)
    return xsrf_token    


def label_payload(url, label):
    return ""

def add_label(label):
    url = ("http://www.google.com/cse/api/%s/annotations/%s?xsrf=%s"
           % (obf_gaia_id, cse_id, get_xsrf_token()))
    global auth_cookie

    headers = {
        "Cookie": auth_cookie,
        "Content-type": "application/json",
        "X-MakeUrlPattern": label.mode == "site"}

    result = urlfetch.fetch(url=cse_api_url(),
                            payload=label_payload(label),
                            method=urlfetch.POST,
                            headers=headers)
    
    # TODO(mwytock): Handle failures (need new XSRF token or new SID cookie)
                
                
                            
