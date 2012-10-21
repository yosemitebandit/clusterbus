import datetime
from models import VehicleArrival
from google.appengine.ext import db
from google.appengine.tools import bulkloader

class VehicleArrivalLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'VehicleArrival',
                                   [('route', str),
                                    ('stop_id', str),
                                    ('stop_name', str),
                                    ('lat', float),
                                    ('lon', float),
                                    ('arrival',
                                     lambda x: datetime.datetime.fromtimestamp(float(x))),
                                    ('headway', int)
                                   ])

loaders = [VehicleArrivalLoader]