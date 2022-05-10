from django.shortcuts import render
import requests
import numpy as np
import pandas as pd
from datetime import date
from datetime import datetime
from nsepy import get_history
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import plot
from .models import CompanyFundamentals
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    all_objects = list(CompanyFundamentals.objects.all())
    if request.method == "POST":

        company = CompanyFundamentals.objects.get(symbol=request.POST['name'])

        dataset = get_history(symbol=request.POST["name"],
                    start=date(int(request.POST['syear']),int(request.POST['smonth']),int(request.POST['sday'])),
                    end=date(int(request.POST['eyear']),int(request.POST['emonth']),int(request.POST['eday'])))
        
        
        fig_rev = go.Figure(
            data=[go.Bar(x=[2018, 2019, 2020, 2021], y=[company.rev2018, company.rev2019, company.rev2020, company.rev2021])],
        )
        fig_rev.update_layout(
            width=800, height=400,
            title = "Revenue of "+request.POST['name'],
            yaxis_title='Rs. in Cr.', xaxis_title='Year',
            paper_bgcolor='rgba(0,0,0,0)')
        plot_div_rev = plot({'data': fig_rev},
                        output_type='div')

        candlestick = go.Candlestick(x=dataset.index,
                            open=dataset['Open'],
                            high=dataset['High'],
                            low=dataset['Low'],
                            close=dataset['Close'])
        fig = go.Figure(data=[candlestick])

        fig.update_layout(
            width=800, height=600,
            title = "Candlestick graph of "+request.POST['name'],
            yaxis_title='Stock Price', xaxis_title='Date',
            paper_bgcolor='rgba(0,0,0,0)')
            # plot_bgcolor='rgba(0,0,0,0)')

        plot_div = plot({'data': fig}, 
                    output_type='div')


        stockcode = company.symbol
        stock_url  = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+str(stockcode)
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        response = requests.get(stock_url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data_array = soup.find(id='responseDiv').getText().strip().split(":")

        for item in data_array:
            if 'lastPrice' in item:
                lastPrice_index = data_array.index(item)+1
                lastPrice=data_array[lastPrice_index].split('"')[1]
                
                
        for item in data_array:
            if 'change' in item:
                change_index = data_array.index(item)+1
                change=data_array[change_index].split('"')[1]
                
                
        for item in data_array:
            if 'pChange' in item:
                pChange_index = data_array.index(item)+1
                pChange=data_array[pChange_index].split('"')[1]
                
        for item in data_array:
            if 'previousClose' in item:
                previousClose_index = data_array.index(item)+1
                previousClose=data_array[previousClose_index].split('"')[1]
                
        for item in data_array:
            if 'open' in item:
                open_index = data_array.index(item)+1
                open=data_array[open_index].split('"')[1]
                
        for item in data_array:
            if 'dayHigh' in item:
                dayHigh_index = data_array.index(item)+1
                dayHigh=data_array[dayHigh_index].split('"')[1]
                
        for item in data_array:
            if 'dayLow' in item:
                dayLow_index = data_array.index(item)+1
                dayLow=data_array[dayLow_index].split('"')[1]
                
        for item in data_array:
            if 'closePrice' in item:
                closePrice_index = data_array.index(item)+1
                closePrice=data_array[closePrice_index].split('"')[1]

        live_sit = [lastPrice, change,pChange,previousClose,open,dayHigh,dayLow,closePrice]
        
        Date = datetime.now()

        return render(request, 'visualize.html', context={'data':company, 'plot_div': plot_div, 'plot_div_rev':plot_div_rev, 'live_sit':live_sit, 'Date':Date, 'objects':all_objects} )
    
    
    else:
        return render(request, 'visualize.html', context={'objects':all_objects})
