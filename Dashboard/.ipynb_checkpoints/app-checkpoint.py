import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

with open(
    "dashboard/stylees.css"
) as f:

    st.markdown(

        f"<style>{f.read()}</style>",

        unsafe_allow_html=True

    )

st.set_page_config(
    page_title="NeuralRetail Intelligence",
    page_icon="📊",
    layout="wide"
)

# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():

    sales = pd.read_csv(
        "Data/processed/daily_sales_features.csv"
    )

    segments = pd.read_csv(
        "Data/processed/customer_segments.csv"
    )

    forecast = pd.read_csv(
        "Data/processed/optimized_prophet_forecast.csv"
    )

    sales['InvoiceDate']=pd.to_datetime(
        sales['InvoiceDate']
    )

    forecast['ds']=pd.to_datetime(
        forecast['ds']
    )

    return sales,segments,forecast


sales,segments,forecast = load_data()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title(
    "NeuralRetail"
)

page = st.sidebar.radio(

"Navigation",

[
"Overview",
"Forecasting",
"Customer Analytics",
"Product Analytics",
"Segmentation",
"Data Explorer"
]

)

# ==========================
# OVERVIEW
# ==========================

if page=="Overview":

    st.title(
        "Retail Intelligence Dashboard"
    )

    total_sales = round(
        sales['Quantity'].sum()
    )

    total_products = sales[
        'StockCode'
    ].nunique()

    total_customers = segments.shape[0]

    col1,col2,col3=st.columns(3)

    col1.metric(
        "Units Sold",
        total_sales
    )

    col2.metric(
        "Customers",
        total_customers
    )

    col3.metric(
        "Products",
        total_products
    )

    trend = sales.groupby(
        'InvoiceDate'
    )['Quantity'].sum().reset_index()

    fig = px.line(

        trend,

        x='InvoiceDate',

        y='Quantity',

        title="Demand Trend"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# FORECASTING
# ==========================

elif page=="Forecasting":

    st.title(
        "Demand Forecasting"
    )

    fig=px.line(

        forecast,

        x='ds',

        y='yhat',

        title='Forecast'

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        forecast.tail(30)
    )

# ==========================
# CUSTOMER ANALYTICS
# ==========================

elif page=="Customer Analytics":

    st.title(
        "Customer Insights"
    )

    persona_counts = (

        segments[
            'Persona'
        ]

        .value_counts()

        .reset_index()

    )

    fig=px.pie(

        persona_counts,

        values='count',

        names='Persona'

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        segments.head()
    )

# ==========================
# PRODUCT ANALYTICS
# ==========================

elif page=="Product Analytics":

    st.title(
        "Product Analytics"
    )

    products=(

        sales.groupby(
            'StockCode'
        )['Quantity']

        .sum()

        .sort_values(
            ascending=False
        )

        .head(20)

        .reset_index()

    )

    fig=px.bar(

        products,

        x='StockCode',

        y='Quantity',

        title="Top Products"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# SEGMENTATION
# ==========================

elif page=="Segmentation":

    st.title(
        "Customer Segments"
    )

    fig=px.scatter(

        segments,

        x='Frequency',

        y='Monetary',

        color='Persona',

        hover_data=[
            'Recency'
        ]

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================
# DATA EXPLORER
# ==========================

else:

    st.title(
        "Data Explorer"
    )

    dataset = st.selectbox(

        "Select Dataset",

        [

            "Sales",

            "Segments",

            "Forecast"

        ]

    )

    if dataset=="Sales":

        st.dataframe(
            sales
        )

    elif dataset=="Segments":

        st.dataframe(
            segments
        )

    else:

        st.dataframe(
            forecast
        )

    csv = sales.to_csv(
        index=False
    )

    st.download_button(

        "Download CSV",

        csv,

        "dataset.csv"

    )