from django.shortcuts import render
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
from visualize.models import CompanyFundamentals
from bs4 import BeautifulSoup
from keras.models import Sequential,load_model
from sklearn.preprocessing import MinMaxScaler

# Create your views here.
def index(request):
    all_objects = list(CompanyFundamentals.objects.all())
    if request.method == "POST":
        company = CompanyFundamentals.objects.get(symbol=request.POST['name'])

        data = get_history(symbol=request.POST['name'], start=date(2021,1,1), end=date.today())
        df = pd.DataFrame(data)
        df2 = df.reset_index()['Close']
        scaler =  MinMaxScaler(feature_range = (0,1))
        df2 = scaler.fit_transform(np.array(df2).reshape(-1,1))

        lstm_model = load_model('./saved_model/LSTM_'+request.POST['name'])

        x_input = df2[len(df2)-100:].reshape(1,-1)
        temp_input = list(x_input)
        temp_input = temp_input[0].tolist()

        lstm_output = []
        n_steps = 100
        i = 0
        while(i<int(request.POST['day'])) :
            if(len(temp_input)>100):
                x_input = np.array(temp_input[1:])
                x_input = x_input.reshape(1,-1)
                yhat= lstm_model.predict(x_input,verbose = 0)
                temp_input.extend(yhat[0].tolist())
                temp_input=temp_input[1:]
                lstm_output.extend(yhat.tolist())
                i=i+1
            else:
                x_input = x_input.reshape((1,n_steps,1))
                yhat = lstm_model.predict(x_input, verbose = 0)
                temp_input.extend(yhat[0].tolist())
                lstm_output.extend(yhat.tolist())
                i=i+1

        predicted = list(scaler.inverse_transform(lstm_output))

        pred_data = pd.DataFrame(predicted)
        # Graph
        fig = go.Figure(data=go.Scatter(x=pred_data.index,y=pred_data[0], mode='lines'))
        fig.update_layout(
            width=800, height=500,
            title = "Graph of "+request.POST['name'],
            yaxis_title='Stock Price', xaxis_title='Date',
            paper_bgcolor='rgba(0,0,0,0)')
        plot_div = plot({'data': fig}, 
                    output_type='div')

        return render(request, 'prediction.html', context={'objects':all_objects,'plot_div': plot_div, 'data':predicted, 'name':request.POST['name'], 'days':request.POST['day']})
    else:    
        return render(request, 'prediction.html', context={'objects':all_objects})