#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
from collections import defaultdict
f1=open(sys.argv[1],"r")

counts=defaultdict(lambda: 0)
total_count=0

for line in f1:
	words = line.strip().split()
	words.append("</s>")
	for word in words:
		counts[word]+=1
		total_count+=1
f1.close()

f2=open("the_model_unigram.txt","w")

for key in counts:
	probability = float(counts[key])/float(total_count)
	f2.write(key+"\t"+str(probability)+"\n")

f2.close()
