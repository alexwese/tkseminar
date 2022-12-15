FROM python:3.7


RUN pip3 install --upgrade pip
RUN pip3 install  --no-cache-dir pandas
RUN pip3 install  --no-cache-dir flask




COPY Node.py Node.py
COPY api.py api.py

CMD ["python", "forecast_api.py"]







