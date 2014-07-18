#!/usr/bin/python
#-*-coding:utf-8-*-

import sys 
from collections import defaultdict
import math

test = open(sys.argv[1],"r") 
model = open(sys.argv[2],"r") 
lambda1=0.95
lambdaunk=1-lambda1
N=1000000

def modelinput(model):
	from collections import defaultdict
	probabilities=defaultdict(lambda: 0)
	for line in model:
		item = line.split("\t")
		uniword=unicode(item[0],"utf-8")
		#print uniword
		probabilities[uniword]=item[1]
	return probabilities

unigram = modelinput(model)

#前向きステップのアルゴリズム
best_edge=defaultdict(lambda: 0)
best_score=defaultdict(lambda: 0)
for line in test:
	line=unicode(line.strip(),"utf-8")
	best_edge[0]=None  #初期ノードのedgeはなし、スコアは0 
	best_score[0]=0
	for word_end in range(1,(len(line)+1)): #node1~(文字数)までのインデックスとなる
		best_score[word_end]=10**10   #各ノードのスコアを無限で初期化 
		for word_begin in range(word_end): #edge1~(文字数)までのインデックス、edge(1)=word_end(0)に対応
			word = line[word_begin:word_end]
			if word in unigram.keys() or len(word)==1:
				prob=lambda1*float(unigram[word])+lambdaunk/N
				my_score=best_score[word_begin] - math.log(prob) #一つ前のノードのスコア＋エッジのスコアの対数値
				if my_score < best_score[word_end]:
					best_score[word_end]=my_score
					best_edge[word_end]=(word_begin, word_end)
	#後ろ向きステップのアルゴリズム
	words=[]
	next_edge=best_edge[len(best_edge)-1] #最後のノードに入るエッジ、best_edge[n]はノードnに入る最もベストなエッジ
	while next_edge != None:
		word=line[next_edge[0]:next_edge[1]]
		word=word.encode("utf-8")
		if word != "":
			words.append(word)
		else:pass
		next_edge=best_edge[next_edge[0]] #next_edge[0]というのは前のノードの位置
	words.reverse()
	print " ".join(words),

