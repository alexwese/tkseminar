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
#df = pd.to_datetime(df['Date'], format='%m/%d/%y')

print(df)
r = restcall.forecast(365,df)

r = r.rename(columns={'DATE': 'Date', 'SALES': 'Price'})
r['Date'] = pd.to_datetime(r['Date'], format='%y-%m-%d')
#r = pd.to_datetime(r['Date'], format='%m/%d/%y')

logging.info(r)
print(r.dtypes)

# vizualize forecast
#df_merged.plot(x='Date', y='Price', style='o')

outputURL = "output_series.xlsx"

with pd.ExcelWriter(outputURL) as writer:
            
    r.to_excel(writer,"name")
    writer.save()


plt.plot(r['Date'],r['Price'], color="blue")
plt.show()

