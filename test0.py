#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
f=open(sys.argv[1],"r")
counts={}
words=[]

for line in f:
	words = line[:-1].split()
	for w in words:
		if w in counts:
			counts[w]+=1
		else:
			counts[w]=1


f.close()

print u"異なり数="+str(len(counts))
print u"the = "+str(counts["the"])
print u"a = "+str(counts["a"])
print u"in = "+str(counts["in"])
