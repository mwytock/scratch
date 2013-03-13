import json
import webapp2

from google.appengine.ext import db

class QueryLogEntry(db.Model):
    query = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

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
        
        

app = webapp2.WSGIApplication([('/api/log', LogApi),
                               ('/api/recent', RecentApi)])
