#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
from collections import defaultdict
training_file=open(sys.argv[1],"r")

context_counts=defaultdict(lambda: 0)
counts=defaultdict(lambda: 0)

for line in training_file:
	words=line.strip().split()
	words.insert(0,"<s>")
	words.append("</s>")
	for i in range(1,len(words)):
		counts[" ".join(words[i-1:i+1])]+=1
		context_counts[words[i-1]]+=1
		counts[words[i]]+=1
		context_counts[""]+=1

model=open("the_model_bigram.txt","w")

for ngram, count in counts.items():
	words = ngram.strip().split()
	words.pop()
	context="".join(words)
	probability=float(counts[ngram])/(context_counts[context])
	model.write(ngram+"\t"+str(probability)+"\n")
	print ngram+"\t"+str(probability)+"\n",
