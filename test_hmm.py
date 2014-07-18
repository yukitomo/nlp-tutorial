#!/usr/bin/python
#-*-coding:utf-8-*-

import sys 
from collections import defaultdict
import math

model_file = open(sys.argv[1],"r") 
test=open(sys.argv[2],"r")

transition=defaultdict(lambda :0) #logの中身に0を入れるとエラーになるため
emission=defaultdict(lambda :0) 
possible_tags={}

#モデル読み込み
for line in model_file:
	models=line.strip().split() #type,context(previous),word(next),prob
	type_=models[0]
	context=models[1]
	word=models[2]
	prob=float(models[3])
	possible_tags[context]=1 #可能なタグとして保存
	if type_=="T":
		transition[context+" "+word]=prob #品詞の遷移(context=previous,word=next)
	else:
		emission[context+" "+word]=prob #品詞に対する単語の確率


for line in test:
	#前向きステップ
	words=line.strip().split()
	l=len(words)
	best_score={}
	best_edge={}
	best_score["0 <s>"]=0 #文頭はスコア0
	best_edge["0 <s>"]=None #文頭にくるエッジはなし
	for i in range(l):
		for prev in possible_tags.keys():
			for next_ in possible_tags.keys():
				if str(i)+" "+prev in best_score.keys() and prev+" "+next_ in transition.keys():
					#print str(i)+" "+prev
					#スコア=前のノードまでの合計スコア＋次の品詞への遷移のスコア＋次の品詞への単語の確率
					if emission[next_+" "+words[i]]==0:
						emission[next_+" "+words[i]]=10**(-10)
					score = best_score[str(i)+" "+prev] - math.log(transition[prev+" "+next_]) - math.log(emission[next_+" "+words[i]])
                    #nextのベストスコアがscoreより大きいとき(より小さくしたい)scoreで更新
					if not str(i+1)+" "+next_ in best_score.keys() or best_score[str(i+1)+" "+next_] > score:
						best_score[str(i+1)+" "+next_]=score
						best_edge[str(i+1)+" "+next_]=str(i)+" "+prev
					#文末記号を考える
					if i == l-1:
						if transition[next_+" "+"</s>"]==0:
							transition[next_+" "+"</s>"]=10**(-10)
						last_score= best_score[str(i+1)+" "+next_] + -math.log(transition[next_+" "+"</s>"]) 
						if not str(i+2)+" "+"</s>" in best_score.keys() or best_score[str(i+2)+" "+"</s>"] > last_score:
							best_score[str(i+2)+" "+"</s>"] = last_score
							best_edge[str(i+2)+" "+"</s>"]=str(i+1)+" "+next_
	#後ろ向きステップ
	tags=[]
	next_edge = best_edge[str(l+1)+" "+"</s>"] #最後のノードにつながるエッジ"l+1 品詞"
	while next_edge != "0 <s>":
		edges=next_edge.split()
		position = edges[0]
		tag = edges[1]
		tags.append(tag)
		next_edge = best_edge[next_edge]
	tags.reverse()
	print " ".join(tags)




