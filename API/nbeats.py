import pandas as pd
from matplotlib import pyplot
import numpy as np
import logging
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from nbeats_forecast import NBeats






#NBEATS Forecasting class
class NBeatsForecast():


    def detectDataFrequency(self,timeinformation_df):

        timeinformation_df['DATE']=pd.to_datetime(timeinformation_df['DATE'])
        timeinformation_df['DIFF'] = pd.to_datetime(timeinformation_df['DATE'].astype(str)).diff(-1).dt.total_seconds().div(60)
        avg_diff = timeinformation_df['DIFF'].mean()

        #MONTHS
        if(avg_diff >= -45000 and avg_diff <= -40000):      
            return "months", timeinformation_df
        
        #WEEKS
        if(avg_diff <= -6000 and avg_diff >= -8000):    
            return "weeks", timeinformation_df

        #DAYS
        if(avg_diff <= -1600 and avg_diff >= -2000):     
            return "days", timeinformation_df

        #YEARS
        if(avg_diff <= -15000000 and avg_diff >= -17000000):            
            return "years", timeinformation_df
    


    def addForecastedTimedata(self,frequency, timeinformation_df,steps):
        
        if(frequency=="months"):
            for i in range(steps):
                newdate = timeinformation_df['DATE'].iloc[-1] + relativedelta(months=+1)
                timeinformation_df = timeinformation_df.append({'DATE': newdate},  ignore_index=True)

        if(frequency=="weeks"):
            for i in range(steps):
                newdate = timeinformation_df['DATE'].iloc[-1] + relativedelta(weeks=+1)
                timeinformation_df = timeinformation_df.append({'DATE': newdate},  ignore_index=True)
        
        if(frequency=="days"):
            for i in range(steps):
                newdate = timeinformation_df['DATE'].iloc[-1] + relativedelta(days=+1)
                timeinformation_df = timeinformation_df.append({'DATE': newdate},  ignore_index=True)
        
        if(frequency=="years"):
            for i in range(steps):
                newdate = timeinformation_df['DATE'].iloc[-1] + relativedelta(years=+1)
                timeinformation_df = timeinformation_df.append({'DATE': newdate},  ignore_index=True)

        print(timeinformation_df)
        return timeinformation_df['DATE']



    def makeForecast(self,nbeats_df,nbeats_steps):
        

        logging.info("Starting NBeats forecast...")
        logging.info("Forecasting Steps: " + str(nbeats_steps))

        logging.info(nbeats_df)
        # Extract time series to pandas data frame
        #df = pd.read_json(data["data"])

        #Change Datatypes
        nbeats_df.columns = ['DATE','SALES']
        nbeats_df = nbeats_df.astype({"SALES": float})
        nbeats_df['DATE'] =  pd.to_datetime(nbeats_df['DATE'], format='%Y-%m-%d')

        
        # Copy time column
        timeinformation = nbeats_df[["DATE"]].copy()
        

        #Change panadas dataframe to numpy nx1 rray
        nbeats_df = nbeats_df.set_index('DATE')
        nbeats_df = nbeats_df.squeeze()
        nbeats_data = np.array([nbeats_df.values]).T
        #logging.info("Forecasting Data: ")
        #logging.info(nbeats_data)
        
        # Create Model
        #model = NBeats(data=nbeats_data, period_to_forecast=nbeats_steps) #91s #103s #107s #72s #127s #101s
        #model = NBeats(data=nbeats_data, period_to_forecast=nbeats_steps, stack = [1])   #73s #70s #76 #88s #121s
        model = NBeats(data=nbeats_data, period_to_forecast=nbeats_steps,nb_blocks_per_stack=2,thetas_dims=[2,8]) #78s #75s #75s 
        model.fit()

        # Create forecast
        forecast = model.predict()
        alldata = np.append(nbeats_data,forecast)
        numpyarray_length = alldata.shape[0]

        # Change numpy array back to pandas dataframe
        alldata = alldata.reshape([numpyarray_length, 1])
        alldata.flatten()
        alldata_df = pd.DataFrame(alldata)

        frequency,timeinformation_df = NBeatsForecast.detectDataFrequency(self,timeinformation)
        alldata_df['DATE'] = NBeatsForecast.addForecastedTimedata(self,frequency,timeinformation_df, nbeats_steps)

        # Restructure final Dataframe
        alldata_df = alldata_df[['DATE', 0]]
        alldata_df.rename(columns={0: 'SALES'}, inplace=True)
        #print(df.tail(10)) 

        # Respond to the client
        logging.info("Prediction completed")

        # Return the response as a json
        return alldata_df
       
