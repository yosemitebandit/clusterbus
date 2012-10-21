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


class TableView(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    testitems = [ 'test_item1', 'test_item2' ]
    worst_arrivals = VehicleArrival.all().order('-headway').run(limit=10)
	
    """testvehicle = VehicleArrival(
	  route = '38',
	  stop_id = '1234',
	  stop_name = 'Geary-Fillmore',
	  lat = 123.456,
	  lon = 789.321,
	  arrival = datetime.datetime.now(),
	  headway = 3600,
    )"""
    
    template_values = {
      'worst_arrivals': worst_arrivals,
	}
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
    

class API(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/json'
    
    # add intelligent defaults
    start = self.request.get('start', 2012)
    end = self.request.get('end', 2011)  # 2012-10-09T14:24:34
    
    # if route is None, return data for all routes
    route = self.request.get('route', 'all')
    
    stop_id = self.request.get('stop_id', 'all')
    
    
    
    self.response.out.write(json.dumps({'start': start, 'end': end}))
    

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/table', TableView),
                              ('/api', API)],
                              debug=True)