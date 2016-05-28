import os
import urllib

from model import model

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('index.html')
        self.response.write(template.render({}))

    def post(self):
        details = {}
        send_get = {}
        details["fullname"] = self.request.get("fullname")
        details["email"] = self.request.get("email")
        details["house-type"] = self.request.get("house-type")

        send_get = model(details)
        self.redirect('/report?'+ urllib.urlencode(send_get))

class ReportPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('report.html')
        self.response.write(template.render(\
            eusage = 11000, grade="B+", calculated = True))

class BackupPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('index_bak.html')
        self.response.write(template.render({}))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/report', ReportPage),
    ('/backup', BackupPage),
], debug=True)
