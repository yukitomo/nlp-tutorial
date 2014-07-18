#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
import math
model=open(sys.argv[1],"r")
test=open(sys.argv[2],"r")
lambda1=0.95
lambdaunk=1-lambda1
V=1000000
W=0
H=0
unk=0

probabilities={}
P={}

for line in model:
	item = line.strip().split("	")
	probabilities[item[0]]=item[1]

print probabilities

for line in test:
	words = line.strip().split(" ")
	words.append("</s>")
	for w in words:
		W+=1
		P[w]=lambdaunk/V
		if w in probabilities:
			P[w] += float(lambda1)*float(probabilities[w])
		else:
			unk += 1
		H += -math.log(P[w],2)
print "entropy = "+str(H/float(W))
print "coverage = "+str(float(W-unk)/float(W))		