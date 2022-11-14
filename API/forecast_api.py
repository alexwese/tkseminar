"""
- Script to start the Service
- Initializes a Tornado Webapp listening an port 3000
- Initializes HTTP Endpoints for calling the different modelling-algorithms
- Handles the HTTP requests
"""

import logging
from numpy import empty
import tornado
import ProphetForecast
import sarima
import nbeats
import tornado.ioloop
import tornado.web
import json
import pandas as pd
import time
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from lib.metadata import getmetadata
from lib.verify import verify_token
from lib.base import BaseHandler


logging.Formatter.converter = time.gmtime
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)




class HelperClass():

    def getResponse(self,algorithm,totalled_df,steps):
        try:
            if algorithm == "prophet": 
                return  ProphetForecast.ProphetForecast.makeForecast(ProphetForecast,totalled_df,int(steps))
            if algorithm == "sarima":
                return sarima.SarimaForecast.makeForecast(sarima, totalled_df, int(steps))
            if algorithm ==  "nbeats":
                return nbeats.NBeatsForecast.makeForecast(nbeats,totalled_df,int(steps))
            if algorithm ==  "automatic":
                return OptimizedForecaster.makeForecast(self,totalled_df,int(steps))
            else: 
                return ProphetForecast.ProphetForecast.makeForecast(ProphetForecast,totalled_df,int(steps))
        except Exception as e:
            logging.error(e)






# 
#
class ProphetForecastHandler(BaseHandler):
    # get request handling
    
    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    
    def options(self):
        # no body
        self.set_status(204)
        self.finish()
    
    def get(self):
        self.write("<strong> Hello, this is the CLAAS Forecasting API.</strong> <br><br> You choosed Facebook Prophet as forecasting algorithm. <br>Please user HTTP POST with parameters 'steps' and 'data' to get a n step forecasting of your time series.")
    
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)

    # post request handling
    def post(self):

        helper = HelperClass()

        self.set_header("Content-Type", "application/json")
        data = json.loads(self.request.body)

        # extract forecasting steps
        steps = data["steps"]

        #Algorithm
        try:
            algorithm = data['algorithm']
        except:
            algorithm = "prophet"

        # extract df
        df = pd.read_json(data["data"])
        logging.info(df)

        
        #Get Response
        response = helper.getResponse(algorithm,df,steps)

        #Send response back        
        response = response.to_json(orient='records')
        self.write(response)
        self.finish()

       






# init the webserver and it's endpoints
# the endpoints represent the application programminig interfaces
# for the currently available forecasting algorithms
#
def make_app():
    logging.info("Forecasting API listening under Port 8081/tcp ...")
    return tornado.web.Application([
        (r"/", BaseHandler),
        (r"/getProphetForecast", ProphetForecastHandler) 
    ])

# main function
if __name__ == "__main__":
    logging.info("Starting forecasting API ...")
    hana = HANAConnector()
    app = make_app()
    app.listen(8081)
    tornado.ioloop.IOLoop.current().start()
