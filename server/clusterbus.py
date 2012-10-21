import cgi
import json
import webapp2
import os
import datetime
from google.appengine.ext.webapp import template
from models import VehicleArrival

class MainPage(webapp2.RequestHandler):
  def get(self):
  	self.response.headers['Content-Type'] = 'text/html'
  	self.response.out.write("""
          <html>
            <body>
              <h1>Hello, clusterbus!</h1>
            </body>
          </html>""")

def query_headways():
  """hello"""

class TableView(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    worst_arrivals = VehicleArrival.all().order('-headway').run(limit=10)
    template_values = {
      'worst_arrivals': worst_arrivals,
	}
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
    

class API(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/json'
    
    #current defaults are based on sample data
    #to do: change to intelligent defaults e.g. today, all routes
    start = self.request.get('start', '2012-10-11T06:30:00' )
    end = self.request.get('end', '2012-10-11T09:30:00')
    route = self.request.get('route', '10')
    callback = self.request.get('callback', None)
    
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(path) as f:
        response_data = json.dumps(f.read())

    # wrap as JSONP if callback is specified
    if callback:
        response_data = '%s(%s);' % (callback, response_data)

    self.response.out.write(response_data)
    

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/table', TableView),
                              ('/api', API)],
                              debug=True)
