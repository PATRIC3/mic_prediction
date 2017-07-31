'''
python testXGBoost.py [pkl] [libsvm] [matOrd] [threads] [model accuracy]
'''

from sys import argv,stderr
import xgboost as xgb

def toStr(arr):
	s = ""
	for i in arr:
		s += i + '\t'

	return s[0:-1]

dtest = xgb.DMatrix(argv[2])
mod = xgb.Booster({'nthread':int(argv[4])})
mod.load_model(argv[1])

pred = mod.predict(dtest)

antiHsh = {}
f = open(argv[5])
f.readline()

for i in f:
	i = i.strip('\n').split('\t')
	if i[0] not in antiHsh:
		antiHsh[i[0]] = {}

	antiHsh[i[0]][i[1]] = toStr(i[2:])
	stderr.write(str(i) + '\n')

f.close()

f = open(argv[3])

count = 0
print "Antibiotic\tMIC Test Method\tPrediction\tAverage W1 antibiotic\t95-conf low antibiotic\t95-conf high antibiotic\tNumber of Antibiotic Samples\tAvg	95-Conf Low\t95-Conf High\t95-Conf Size	Number of Samples"
for i in f:
	i = i.strip()
	keys = i.split('\t')

	pred[count] = round(pred[count])
	# stderr.write(keys[0])
	try:
		stats = antiHsh[keys[0]][str(2**pred[count])]
	except:
		stats = "prediction out of range"

	print i + '\t' + str(2**pred[count]) + '\t' + stats

	count += 1

f.close()
