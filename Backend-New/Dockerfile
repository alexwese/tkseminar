FROM python:3.7


RUN pip3 install --upgrade pip
RUN pip3 install  --no-cache-dir pandas
RUN pip3 install  --no-cache-dir flask
RUN pip3 install  --no-cache-dir flask-cors
RUN pip3 install  --no-cache-dir scipy


COPY Node.py Node.py
COPY api.py api.py
COPY new_risk_data.json new_risk_data.json 
COPY risk_data_user1.json risk_data_user1.json 

CMD ["python", "api.py"]







