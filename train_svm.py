#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
from perceptron_module import *
from collections import defaultdict

def SIGN(value):
	if value > 0:
		return +1
	else:
		return -1

def ABS(value):
	if value < 0:
		return -value
	else:
		return value 


def UPDATE_WEIGHTS_new(w,phi,y,c):
	for name,value in w.items():
		if ABS(float(value)) < c:
			w[name] = 0
		else:
			w[name] -= SIGN(float(value))*c
	for name,value in phi.items():
		w[name] += float(value) * float(y)

def VAL(w,phi,y):
	score = 0
	for name, value in phi.items():
		if name in w.keys():
			score += value*float(w[name])*float(y)
	return score


if __name__ == '__main__':
	c = 0.0001
	margin =  0.1
	w = defaultdict(lambda :0)
	avg = defaultdict(lambda :0)
	updates = 0
	model=open("the_model_svn.txt","w")
	for i in range(1):
		for line in open(sys.argv[1]):
			words = line.strip().split("	")
			x = words[1]
			y = words[0] #ラベル
			phi = CREATE_FEATURES(x)
			val = VAL(w,phi,y)
			if val <= margin:
				UPDATE_WEIGHTS_new(w,phi,y,c)
			updates += 1

	for name in sorted(w.keys()):
		model.write(name+"	"+str(w[name])+"\n")


