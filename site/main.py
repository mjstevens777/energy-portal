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

import mimetypes

class StaticFileHandler(webapp2.RequestHandler):
    def get(self, path):
        abs_path = os.path.abspath(os.path.join('static', path))
        if os.path.isdir(abs_path) or abs_path.find(os.getcwd()) != 0:
            self.response.set_status(403)
            return
        try:
            f = open(abs_path, 'rb')
            self.response.content_type = mimetypes.guess_type(abs_path)[0]
            self.response.out.write(f.read())
            f.close()
        except Exception as e:
            print(e)
            self.response.set_status(404)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/report', ReportPage),
    ('/backup', BackupPage),
    ('/static/(.+)', StaticFileHandler)
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
