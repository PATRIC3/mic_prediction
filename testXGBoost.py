'''
python testXGBoost.py [pkl] [libsvm] [matOrd] [threads] 
'''

from sys import argv,stderr
import xgboost as xgb

# convert array to string
def toStr(arr):
	# init string
	s = ""
	# for each element in array, append string
	# with element + tab
	for i in arr:
		s += i + '\t'

	# return string with last tab removed
	return s[0:-1]

# load the libsvm matrix
dtest = xgb.DMatrix(argv[2])
# load the model from memory
mod = xgb.Booster({'nthread':int(argv[4])})
mod.load_model(argv[1])

# make predictions
pred = mod.predict(dtest)

# # init antibiotic hash
# antiHsh = {}
# # open model accuracy file
# f = open(argv[5])
# # read header
# f.readline()

# # for each file, add to antibiotic hash
# for i in f:
# 	i = i.strip('\n').split('\t')
# 	if i[0] not in antiHsh:
# 		antiHsh[i[0]] = {}

# 	antiHsh[i[0]][i[1]] = toStr(i[2:])
# 	# stderr.write(str(i) + '\n')

# f.close()

# open up file that dictates matrix order
f = open(argv[3])

# init count
count = 0
# print header
print "Antibiotic\tMIC Test Method\tPrediction"#\tAverage W1 antibiotic\t95-conf low antibiotic\t95-conf high antibiotic\tNumber of Antibiotic Samples\tAvg	95-Conf Low\t95-Conf High\t95-Conf Size	Number of Samples"
# for each line in file
# get keys for antibiotic statistics
# search for antibiotic statistics
#   if none exists, set stats to prediction out of range
# print out line
for i in f:
	i = i.strip()
	keys = i.split('\t')

	pred[count] = round(pred[count])
	# stderr.write(keys[0])
	# try:
	# 	stats = antiHsh[keys[0]][str(2**pred[count])]
	# except:
	# 	stats = "prediction out of range"

	print i + '\t' + str(2**pred[count])# + '\t' + stats

	count += 1

f.close()
