from google.appengine.ext import db

class VehicleArrival(db.Model):
  """Ex: 38-Geary inbound @ Geary&Fillmore at 10/20/12 9:01am."""
  route = db.StringProperty() #ex: 38
  stop_id = db.StringProperty() #ex: 1234
  stop_name = db.StringProperty() #ex: Geary&Fillmore
  lat = db.FloatProperty()
  lon = db.FloatProperty()
  arrival = db.DateTimeProperty()
  headway = db.IntegerProperty() #seconds until next vehicle
