import pandas as pd
import requests
import logging
from logging import log, INFO, ERROR, WARN, DEBUG
import json
from matplotlib import pyplot as plt

class restcall():
    steps = 0
    training = False
    def forecast(steps,df):     
        logging.basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Number of chosen forecast steps: "  + str(steps))

        ### Parameters ###
        # REST url
        #algorithm = 'getNBeatsForecast'
        algorithm = 'getProphetForecast'
        #algorithm = 'sarima_forecast'

        url = 'http://localhost:8061/' + algorithm

        # read time series from xlsx to pandas data frame
        logging.info("Read data ...")

        
        # post request
        logging.info("POST request startet ...")

        jsn = {
            "steps": steps,
            "data": df.to_json(orient='records')
        }
        response = json.dumps(jsn)
        logging.info("Ready for POST ...")



        req = requests.post(url,response)
        logging.info(req)
        # read output from request to data frame
        output = pd.read_json(req._content)
        #plt.plot(data[i]["SALES"], color="blue")
        #plt.plot(df_list[-1]["SALES"], color="orange")
        #df_list.append(output)
            #except:
            #    df_list.append(data[i])

            # vizualize forecast
            #plt.plot(data[i]["SALES"], color="blue")
            #plt.plot(df_list[-1]["SALES"], color="orange")
            #plt.show()
        #outputURL = "output_series_" + algorithm[3:] + ".xlsx"
        return output







df = pd.read_csv("aluminium.csv",thousands='.', decimal=',')
df = df[['Date', 'Price']]

print(df)
r = restcall.forecast(10,df)

r = r.rename(columns={'DATE': 'Date', 'SALES': 'Price'})




# vizualize forecast
#df_merged.plot(x='Date', y='Price', style='o')


plt.figure() 
plt.plot(r["Price"], color="blue")
plt.gcf().autofmt_xdate() 
plt.show()


#plt.plot(df_merged["Price"], color="blue")
#plt.show()

