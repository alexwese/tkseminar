import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot
import numpy as np
import tornado.web
import logging
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error





# Prophet forecasting class
class ProphetForecast():
    
    def makeForecast(self, prophet_df, steps):
        
        # Logging: start
        logging.info("Starting Prophet forecast ...")
        logging.info("Forecasting Steps: " + str(steps))
        
        # set column names for 
        prophet_df.columns = ['ds','y']
        
        
        logging.info("Forecasting Data: ")
        logging.info(prophet_df.head(5))

        try:
        # initialize prophet and build a model
            logging.info("Fitting prophet model ...")
            m = Prophet(yearly_seasonality=10)
            m.fit(prophet_df)

            # predict n steps
            logging.info("Predicting next "+ str(steps)+" steps ...")
            future = m.make_future_dataframe(periods=steps,freq="M")
            forecast = m.predict(future)
            prophet_df2 = pd.DataFrame(forecast[['ds', 'yhat']])
            logging.info(prophet_df2)
            prophet_df2.columns = ['DATE','SALES']

            new_values = prophet_df2.tail(steps)
            #new_values['DATE'] = datetime.strptime(new_values['DATE'], "%y-%m-%d")
            #new_values['DATE'] = new_values['DATE'] + timedelta(days=1)
            logging.info(new_values)

            
        except Exception as e:
            logging.error(e)
        
        # respond to the client
        logging.info("Prediction completed")
        #response = df2.to_json(orient='records')

        return new_values



