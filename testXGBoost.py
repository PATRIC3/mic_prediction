'''
python testXGBoost.py [pkl] [libsvm] [matOrd] [threads]
'''

from sys import argv
import xgboost as xgb

dtest = xgb.DMatrix(argv[2])
mod = xgb.Booster({'nthread':int(argv[4])})
mod.load_model(argv[1])

pred = mod.predict(dtest)

f = open(argv[3])

count = 0
print "Antibiotic\tMIC Test Method\tLow Bound (within 1)\tPrediction\tHigh Bound (within 1)"
for i in f:
	i = i.strip()
	pred[count] = round(pred[count])
	print i + '\t' + str(2**(pred[count]-1)) + '\t' + str(2**pred[count]) + '\t' + str(2**(pred[count]+1))

	count += 1

f.close()
