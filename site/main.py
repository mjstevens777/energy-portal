import os
import urllib

import jinja2
import webapp2
from model import model

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
        details = dict(self.request.POST)

        send_get = model(details)
        self.redirect('/report?' + urllib.urlencode(send_get))


class ReportPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('report.html')
        output = dict(self.request.GET)
        self.response.write(template.render(output))


class BackupPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('index_bak.html')
        self.response.write(template.render({}))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/report', ReportPage),
    ('/backup', BackupPage),
], debug=True)
