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
  	template_values = { }
  	path = os.path.join(os.path.dirname(__file__), 'index.html')
  	with open(path, 'rb') as f:
  		self.response.out.write(f.read())

class TableView(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    start = datetime.datetime.strptime('2012-10-11T11:45:00', "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime.strptime('2012-10-11T15:30:00', "%Y-%m-%dT%H:%M:%S")
    route = '10'
    arrivals = VehicleArrival.all().filter("arrival > ", start).filter("arrival < ", end).filter("route = ", route)
    processed_arrivals = query.query(arrivals)
    template_values = {
      'worst_arrivals': processed_arrivals['stop_stats'],
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
    if arrivals.count() == 0:
        self.response.out.write("[]")
        return
        
    processed_arrivals = query.query(arrivals)
    
    response_data = {
    	'route': route
    	, 'start': start.isoformat()
    	, 'end': end.isoformat()
    	, 'route_aggregate': processed_arrivals['route_aggregate']
    	, 'stop_stats': processed_arrivals['stop_stats']
    }
    
    response_data = json.dumps(response_data)

    # wrap as JSONP if callback is specified
    if callback:
        response_data = '%s(%s);' % (callback, response_data)

    self.response.out.write(response_data)



class DeleteRoute(webapp2.RequestHandler):
  def get(self):
  	route = self.request.get('route')
  	self.response.out.write("Deleted route %s (not really, just a placeholder for a database cleanup method)" % route )


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/table', TableView),
                              ('/delete', DeleteRoute),
                              ('/api', API)],
                              debug=True)
