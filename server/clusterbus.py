import cgi
import json
import webapp2
import os
import datetime
from google.appengine.ext.webapp import template
from models import VehicleArrival
import query

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
    start = datetime.datetime.strptime('2012-10-11T11:45:00', "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime.strptime('2012-10-11T15:30:00', "%Y-%m-%dT%H:%M:%S")
    route = '10'
    arrivals = VehicleArrival.all().filter("arrival > ", start).filter("arrival < ", end).filter("route = ", route)
    processed_arrivals = query.query(arrivals)
    template_values = {
      'worst_arrivals': processed_arrivals,
	}
    path = os.path.join(os.path.dirname(__file__), 'tabletest.html')
    self.response.out.write(template.render(path, template_values))
    

class API(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/json'
    
    #current defaults are based on sample data
    #to do: change to intelligent defaults e.g. today, all routes
    start = datetime.datetime.strptime(self.request.get('start', '2012-10-11T06:30:00' ), "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime.strptime(self.request.get('end', '2012-10-11T09:30:00' ), "%Y-%m-%dT%H:%M:%S")
    route = self.request.get('route', '10')
    callback = self.request.get('callback', None)

    arrivals = VehicleArrival.all().filter("arrival > ", start).filter("arrival < ", end).filter("route = ", route)
    processed_arrivals = query.query(arrivals)
    
    response_data = {
    	'route': route
    	, 'start': start.isoformat()
    	, 'end': end.isoformat()
    	, 'route_aggregate': {}
    	, 'stop_stats': processed_arrivals
    }
    
    response_data = json.dumps(response_data)

    # wrap as JSONP if callback is specified
    if callback:
        response_data = '%s(%s);' % (callback, response_data)

    self.response.out.write(response_data)



class APItest(webapp2.RequestHandler):
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
        response_data = f.read()

    # wrap as JSONP if callback is specified
    if callback:
        response_data = '%s(%s);' % (callback, response_data)

    self.response.out.write(response_data)


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/table', TableView),
                              ('/api', API)],
                              debug=True)
