'''
python makeMatrix.py [kmcOut] [arrInd] [antibioList] [micMethods] [out1] [out2] [contigs]
'''

from sys import argv,stderr

f = open(argv[7])

contigs = []

for i in f:
	i = i.split('\t')[0]
	contigs.append(i)

f.close()

f = open(argv[2])

featureHash = {}

for i in f:
	i = i.strip().split('\t')
	if len(i) < 2:
		continue
	featureHash[i[1]] = i[0]

f.close()

f = open(argv[1])

kmcContigs = {}
for i in f:
	i = i.strip().split('\t')
	kmcContigs[i[0]] = i[1]

kmcLine = ''
for i in contigs:
	if i in kmcContigs:
		kmcLine += featureHash[i] + ':' + kmcContigs[i] + ' '
	# else:
	# 	kmcLine += featureHash[i] + ':' + '0 '

f.close()

f = open(argv[3])

antibioList = []
for i in f:
	i = i.strip()
	if i in featureHash:
		antibioList.append(i)

f.close()

f = open(argv[4])

micMethods = []
for i in f:
	i = i.strip()
	if i in featureHash:
		micMethods.append(i)

f.close()

f = [open(argv[5], 'w'), open(argv[6], 'w')]
for i in antibioList:
	for j in micMethods:
		line = kmcLine + featureHash[i] + ':1 ' + featureHash[i] + ':1\n'
		f[0].write(line)
		f[1].write(i + '\t' + j + '\n')
