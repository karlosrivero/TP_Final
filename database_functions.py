from datetime import datetime
from datetime import timedelta

import pandas as pd
import yfinance as yf
import sqlite3
import json

import plotly.graph_objects as go


## -- PLOT TICKER -- ##

def plot_ticker(ticker_name):
    error_code = 0

    try:
        conn = sqlite3.connect("ticker_data.db")
    except:
        error_code = 4

    if error_code == 0:
        data_to_plot = pd.read_sql("SELECT Date, Open, High, Low, Close FROM " + ticker_name, conn)
        fig = go.Figure(data=[go.Candlestick(x=data_to_plot['Date'],
                                             open=data_to_plot['Open'],
                                             high=data_to_plot['High'],
                                             low=data_to_plot['Low'],
                                             close=data_to_plot['Close'])])
        fig.show()

    return error_code


## -- SAVE TICKER DATA -- ##

def save_ticker_data(ticker_name, hist):
    conn = None
    error_code = 0

    try:
        conn = sqlite3.connect("ticker_data.db")
    except:
        error_code = 4

    if error_code == 0:
        hist.to_sql(ticker_name, conn, if_exists="replace")

    return error_code


## --  SAVE TICKER METADATA -- ##

def save_ticker_metadata(ticker, st_date, fn_date):
    error_code = 0

    with open("metadata.json", 'r+') as metadata_file:
        metadata = json.load(metadata_file)

        ticker_exists = False
        for i in metadata["ticker_records"]:
            if i["ticker"] == ticker:
                ticker_exists = True
                i.update({"start_date": st_date, "end_date": fn_date})

        if not ticker_exists:
            new_entry = {"ticker": ticker,
                         "start_date": st_date,
                         "end_date": fn_date}
            metadata["ticker_records"].append(new_entry)

        metadata_file.seek(0)
        json.dump(metadata, metadata_file, indent=4)

    return error_code


## -- CHECK TICKER DATA -- ##

def check_ticker_data(ticker):
    with open("metadata.json", 'r+') as metadata_file:
        metadata = json.load(metadata_file)

        for i in metadata["ticker_records"]:
            if i["ticker"] == ticker:
                return i

        return None


## -- GET TICKER DATA -- ##

def get_ticker_data(ticker, st_date, fn_date):
    error_code = 0

    date_format = "%Y-%m-%d"
    max_years = timedelta(days=365 * 20)

    try:
        start = datetime.strptime(st_date, date_format)
        end = datetime.strptime(fn_date, date_format)
        period = end - start
    except:
        error_code = 2

    if error_code == 0:
        if start >= end or end > datetime.now():
            error_code = 2
        elif period > max_years:
            error_code = 3
        else:
            print("Fetching data...")
            api_data = yf.Ticker(ticker)
            ticker_data = api_data.history(start=st_date, end=fn_date, debug=False)
            if len(ticker_data) == 0:
                error_code = 1

    if error_code == 0:
        print("Updating database...")

        error_code = save_ticker_data(ticker, ticker_data)
        if error_code == 0:
            error_code = save_ticker_metadata(ticker, st_date, fn_date)

    return error_code
