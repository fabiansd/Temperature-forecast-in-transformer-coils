import sklearn
import pandas as pd
import numpy as np
import csv
import string
import sys

#Dette programmet krever at CSV filene har en header fil
temp =sys.argv[1]
mal = sys.argv[2]
finaldata = sys.argv[3]

temperature=open(temp,'rb')
measurements=open(mal,'rb')
finaldata=open(finaldata,'wb')

#Konstruerer hashtabell av temperaturdataen med tidsstempel som nøkkel og temperatur som verdi
temp_hash = {}
tempreader = csv.reader(temperature, delimiter=";")
tempheader = ''
first = True
for row in tempreader:
	if first:
		first = False
		tempheader = row
	else:
		temp_hash[row[0]] = row[1]


#Les måledata og lag endelig datafil som skal skrives til
inreader = csv.reader(measurements, delimiter=";")
datawrite = csv.writer(finaldata, delimiter=',')
malheader = ''


#Iterer gjennom måledataen og match den opp med tilsvarende tidsstempel i hashtabellen. Om nøkelen ikke finnes forkastes raden
#fordi temperaturdata mangler.
first = True
counter = 0
for row in inreader:
	counter += 1
	if first:
		first = False
		malheader = row
		for i,a in enumerate(malheader):
				malheader[i]=a.replace(',','.')

		malheader.append(tempheader[1])
		datawrite.writerow(malheader)
	else:

		temp = [temp_hash.get(str(row[0]),None)]

		if temp[0] != None:
			#Skriv målerad hvis temperaturdata finnes
			temp[0] = temp[0].replace(',','.')
			for i,a in enumerate(row):
				row[i]=a.replace(',','.')
			
			datawrite.writerow(row + temp)

	if counter % 1000 == 0: print("%.d rows has been processed" % counter)

#Lukk lese og skriveobjektene
temperature.close()
measurements.close()
finaldata.close()

