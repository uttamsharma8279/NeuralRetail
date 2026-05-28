from fastapi import FastAPI

import pandas as pd

app=FastAPI()

# load forecast
forecast=pd.read_csv(

"Data/processed/optimized_prophet_forecast.csv"

)
# root end point
@app.get("/")

def root():

    return {

    "message":

    "NeuralRetail API"

    }
# forecast endpoint
@app.get("/forecast")

def get_forecast():

    return forecast.tail(
    30
    ).to_dict(
    orient='records'
    )
# customer segment end point
segments=pd.read_csv(

"Data/processed/customer_segments.csv"

)
@app.get("/segments")

def get_segments():

    return segments[
    'Persona'
    ].value_counts().to_dict()
