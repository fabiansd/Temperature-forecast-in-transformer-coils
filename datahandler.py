import csv
import string
import sys
import numpy as np
import scipy.io as sio

def isFloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def getdata(inname,x,y,samples,step_size,inlist,input_length):

	#Les CSV fil og lag et leseobject
	infile=open(inname,'r')
	inreader = csv.reader(infile, delimiter=",")

	#Støttevariabler
	input_dim = len(inlist)
	output_length = input_length
	output_dim = 1
	lengthcounter = 0
	timestep = 0
	first = True


	tempx = np.zeros(( input_length, input_dim),dtype='float')
	tempy = np.zeros(( output_length, output_dim),dtype='float')

	#En hashtabell blir laget ut av måledataen
	mes_dict = {}
	key = 0
	count = 0
	for row in inreader:
		if first:
			first = False
		else:
			if count % step_size == 0:
				mes_dict[key]=row
				key += 1
			count += 1

	#print('Len dict: ',len(mes_dict))
	#itererer gjennom alle datapunktene i hashtabellen, og lager chunks ut ifra disse som strekker seg
	#n step tilbake og n step frem
	for key in range(samples):
		for step in range(input_length):
			for i,p in enumerate(inlist): #appends the elements picked out from the key list
				if isFloat(mes_dict[key+step][p]):
					tempx[step,i] = mes_dict[key+step][p] 
				else:
					tempx[step,i] = 0
			if isFloat(mes_dict[key+input_length+step-1][inlist[-1]]):
				tempy[step] = float(mes_dict[key+input_length+step-1][inlist[-1]])
			else:
				tempy[step] = 0

		x[timestep] = tempx
		y[timestep] = tempy
		timestep +=1

		#break hvis key er lik antall samples
		if key == samples:
			print('Datahandler STOPPED, (x,y): (', str(x.shape), ' ', str(y.shape),')', ' key: ', key)
			return x, y

	#Returner når hele hashtabellen er iterert gjennom
	print('Datahandler FINISHED, (x,y): (', str(x.shape), ' ', str(y.shape),')', ' key: ', key)
	return x, y


