import json
import webapp2

import cse_api_client

from google.appengine.ext import db

# models
class QueryLogEntry(db.Model):
    query = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class Label(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add=True)
    url = db.StringProperty()
    label = db.CategoryProperty(choices=("blue", "green"))
    mode = db.CategoryProperty(choices=("page", "site"))

# handlers
class LogApi(webapp2.RequestHandler):
    def post(self):        
        log_entry = QueryLogEntry(query=self.request.get("q"))
        log_entry.put()

class RecentApi(webapp2.RequestHandler):
    def get(self):
        q = db.Query(QueryLogEntry).order("-date")

        seen_queries = {}
        recent = []
        for log_entry in q.run(limit=30):
            if log_entry.query in seen_queries:
                continue
            recent.append({"query": log_entry.query})
            seen_queries[log_entry.query] = True

        self.response.headers["Cache-control"] = "no-store"
        self.response.headers["Content-type"] = "application/json"
        self.response.out.write(json.dumps({"recent": recent}))

class LabelApi(webapp2.RequestHandler):
    def post(self):
        label = Label(url=self.request.get("url"),
                      label=self.request.get("label"),
                      mode=self.request.get("mode"))
        label.put()
        cse_api_client.add_label(label)
        
app = webapp2.WSGIApplication([("/api/log", LogApi),
                               ("/api/recent", RecentApi),
                               ("/api/label", LabelApi)])
