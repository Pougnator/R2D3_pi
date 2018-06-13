import urllib
import json
from urllib.request import urlopen

def main():
	trainItalie = closestCatchableTrain("Porte d'Italie")
	trainKB = closestCatchableTrain("Kremlin Bicetre")
	if trainItalie < trainKB:
		print(trainItalie)
		print('Porte d\'Italie')
		return trainItalie, "Porte d'Italie"
		
	
	else:
		
		print(trainKB)
		print('Kremlin Bicetre')
		return trainKB, "Kremlin Bicetre"
   	
def getNextTrain(x_json, train_number):
	if train_number >3:
		print("error: train number too high")
	x = x_json["result"]["schedules"][train_number]["message"]
	first_train = x[0]
	i=1
	while x[i]!=' ':
		#print(x[i])
		first_train = first_train+x[i]
		i=i+1
	if 'Train' in first_train:
		first_train = 0
	#print (first_train)
	return(float(first_train))

def closestCatchableTrain(station):
	url = 'https://api-ratp.pierre-grimaud.fr/v3/schedules/metros/7/'
	if station == "Kremlin Bicetre":
		url = url + 'le+kremlin+bicetre' + '/R'
	elif station == "Porte d'Italie":
		url = url + 'porte+d\'italie' + '/R'
	x_json = json.loads(urllib.request.urlopen(url).read())
	#print(x_json)
	j=0
	while getNextTrain(x_json,j) < 7 :
		j = j+1
	return getNextTrain(x_json,j)

	
if __name__ == '__main__':
    main()