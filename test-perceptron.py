#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
from collections import defaultdict
from perceptron_module import *

model=open(sys.argv[1],"r")
inputfile=open(sys.argv[2],"r")
answer=open("answer_perceptron.txt","w")


PREDICT_ALL(model,inputfile)



