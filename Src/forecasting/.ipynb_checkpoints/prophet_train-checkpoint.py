import pandas as pd

from prophet import Prophet

from prophet.serialize import model_to_json

print(

"Loading Data"

)

daily = pd.read_csv(

"Data/processed/daily_sales_features.csv"

)

daily = (

daily.groupby(

'InvoiceDate'

)['Quantity']

.sum()

.reset_index()

)

daily.columns=[

'ds',

'y'

]

daily['ds']=pd.to_datetime(

daily['ds']

)

print(

"Training Prophet"

)

model = Prophet(

weekly_seasonality=True,

yearly_seasonality=True

)

model.fit(

daily

)

print(

"Saving Model"

)

with open(

"models/saved_models/prophet_model.json",

"w"

) as f:

    f.write(

        model_to_json(

            model

        )

    )

print(

"Done"

)