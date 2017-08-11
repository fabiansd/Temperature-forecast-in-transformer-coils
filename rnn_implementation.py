#Recurrent Neural Network - implementasjon

from __future__ import print_function

import tensorflow as tf
from datahandler import getdata
import sys
import numpy as np

from keras.models import Sequential  
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras.layers.wrappers import TimeDistributed, Bidirectional#, AttentionSeq2Seq
from keras.layers.recurrent import LSTM, GRU

#from random import random
import scipy.io as sio


print('SRIPT START')

#Input for file name
inname =sys.argv[1]

#Lister for å hente ut og reorganisere målingskolonner fra CSV filen
inlist_borg = [1,6,3,4,5,9,8,10,12,11]
inlist_en=[12]
inlist_frogner = [0,6,3,4,5,9,10,11,2,8,13,14,12]
inlist_frogner_explained = ['Aktiv effekt 300','strøm L1 300','strøm L2 300','strøm L3 300','strøm L1 420','strøm L2 420','strøm L3 420','spenning 300','spenning 420','oljetemperaturæ','utetemperatur','viklingstemperatur']
inlist_borg_explained=['Aktiv effekt 300','Aktiv effekt 66', 'Strøm L1 300','Strøm L2 300','Strøm L3 300','Strøm 66','Spenning 66','Oljetemperatur','Utetemperatur','Viklingstemperatur']

#Hyperparametere
input_length = 10
step_size=20
epochs = 40
batch_size = 400#128
hidden_neurons = 200
split = 0.9
out_neurons = 1

#Tilleggvariabler
input_dim = len(inlist_frogner)
output_dim = 1
output_length = input_length
datalength = 1823680#540293 borgund #653180
datalength = int(datalength/step_size)
mod = datalength % step_size
datalength -= mod
datalength -= input_length*2

samples = datalength
no_of_batches = int(samples/batch_size)
in_neurons = input_dim

print('Samples: ', samples)

#Uthenting av data ved å kalle getdata

x_input = np.zeros((samples, input_length, input_dim), dtype='float') #(1000x20x8)
y_input = np.zeros((samples, output_length, output_dim),dtype='float') #(1000x20)

x_input, y_input = getdata(inname,x_input,y_input,samples,step_size,inlist_frogner,input_length) #works well. shape = (samples, timesteps, feature dim)


inspect = True

#Splitter opp dataen til test- og treningsdata
x_train, x_test = x_input[0:int(split*samples),:,:], x_input[int(split*samples):,:,:]
y_train, y_test = y_input[0:int(split*samples),:,:], y_input[int(split*samples):,:,:]

print('Model initializing')
#Nettverksarkitektur
model = Sequential()
model.add(LSTM(output_dim=200, input_dim=in_neurons, return_sequences=True))
model.add(BatchNormalization())
#Regularisering
model.add(Dropout(0.1))
model.add(TimeDistributed(Dense(output_dim=output_dim,input_dim=200)))
model.add(Activation("linear"))

#Definer tapsfunksjon, optimaliseringsalgoritme og valideringssplit. model.fit bruker 15% av 
#treningsdataen til å sjekke treffsikkerheten hver epoke
model.compile(loss="mean_squared_logarithmic_error", optimizer="adam")#"rmsprop")
print('Model compiled')
model.fit(x_train, y_train, batch_size=batch_size, nb_epoch=epochs, validation_split=0.15)
print('Model fitted')

#Test dataen blir her brukt til å generere prediksjoner for å teste den endelige treffsikkerheten
print('test data')
print(y_test)
predicted = model.predict(x_test)
print('predictions made')
print(predicted)
#Rmse er root mean square error
rmse = np.sqrt(((predicted - y_test) ** 2).mean(axis=0))
print('Rmse')
print(rmse)

#Test data, test label og prediksjon blir lagret som Matlab filer
sio.savemat('Feature labels',{'content':inlist_frogner_explained})
sio.savemat('x_test.mat',{'data_xtest':x_test})
sio.savemat('y_test.mat',{'data_ytest':y_test})
sio.savemat('y_pred.mat',{'data_pred':predicted})
sio.savemat('rmse',{'rmse':rmse})

#Script for å kunne inspisere prediksjonene tidssteg for tidssteg i kommando prompten
if inspect:
    for i,p in enumerate(x_test):
        #p is a matrix with the time chunk
        print('x_test')
        print(p)
        print('y_test')
        print(y_test[i])
        print('pred')
        print(predicted[i])
        s=input()


