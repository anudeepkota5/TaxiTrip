from django.shortcuts import render
#from django.template.context_processors import request
import pandas as pd
import numpy as np
import xgboost as xgb
from math import sin, cos, sqrt, atan2, radians
from .forms import IndexForm
#from TaxiTrip.settings import BASE_DIR
from django.http.response import HttpResponse
# Create your views here.
def indexpage(request):
    return render(request, 'index.html')

def predictions(request):
    if(request.method == 'POST'):
        indexform = IndexForm(request.POST)

        if indexform.is_valid():
            date = indexform.cleaned_data['date']
            distance = indexform.cleaned_data['distance']
            option = request.POST['option']
            adate = request.POST['adate']

            # approximate radius of earth in km
            R = 6373.0

            dat = pd.read_csv('train.csv')
            distancee = []
            for i in range(len(dat)):
                lat1 = radians(dat.iloc[i,4])
                lon1 = radians(dat.iloc[i,3])
                lat2 = radians(dat.iloc[i,6])
                lon2 = radians(dat.iloc[i,5])

                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                dis = R * c
                distancee.append(dis)

            distance_1 = pd.DataFrame({'Distance in Km':distancee})
            distance_2 = pd.concat([dat,distance_1], axis = 1)

            distance_2['pickup_datetime'] = pd.to_datetime(distance_2['pickup_datetime'])
            distance_2['Time'] = distance_2['pickup_datetime'].dt.hour

            train = distance_2.drop(distance_2[(distance_2['Distance in Km']==0)|(distance_2['fare_amount']==0)].index, axis = 0)
            train = train.drop(['key','pickup_datetime','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude'], axis = 1)

            x = train.iloc[:,1:].values
            y = train.iloc[:,0].ravel()


            dtrain = xgb.DMatrix(x, label=y)


            params = {'max_depth':14,
                      'eta':1,
                      'silent':1,
                      'objective':'reg:linear',
                      'eval_metric':'rmse',
                      'learning_rate':0.005
                     }
            num_rounds = 500
            xb = xgb.train(params, dtrain, num_rounds)

            x_test = np.array([[date,distance,option]])
            dtest = xgb.DMatrix(x_test)
            pred = xb.predict(dtest)
            if(adate % 7 == 0):
                pred = pred + 1
            elif(adate % 7 == 1):
                pred = pred + 2
            elif(adate % 7 == 2):
                pred = pred - 1
            elif(adate % 7 == 3):
                pred = pred -2
            elif(adate % 7 == 4):
                pred = pred - 0.5
            elif(adate % 7 == 5):
                pred = pred + 0.5
    return HttpResponse("The fare for this trip is : {}$".format(pred))
