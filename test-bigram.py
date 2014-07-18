#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
import math
from collections import defaultdict

model=open(sys.argv[1],"r")
test=open(sys.argv[2],"r")
lambda1=0.95
lambda2=0.95
V=10000000
W=0
H=0

probabilities=defaultdict(lambda: 0)
P=defaultdict(lambda: 0)

for line in model:
	item = line.strip().split("\t")
	item2 = item[0].split(" ")
	print item

	if len(item2) > 1:
		probabilities[" ".join(item2)]=item[1]
	else:
		probabilities[item[0]]=item[1]

print probabilities

for line in test:
	words = line.strip().split(" ")
	words.insert(0,"<s>")
	words.append("</s>")
	for i in range(1,len(words)):
		P1=lambda1*float(probabilities[words[i]])+(1-lambda1)/V
		P2=lambda2*float(probabilities[" ".join(words[i-1:i+1])])+(1-lambda2)*P1
		H += -math.log(P2,2)
		W += 1

print "entropy = "+str(float(H)/W)
