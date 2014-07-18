#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
from collections import defaultdict
import math

lm_file=open(sys.argv[1],"r")
tm_file=open(sys.argv[2],"r")
test_file=open(sys.argv[3],"r")
#test_file=open(sys.argv[3],"r") #test/06­pron.txt,data/wiki­ja­test.pron

lm=defaultdict(lambda: 0)
#tm={"かんじ":{"漢字":prob,"幹事":prob,....},.....} 
#tm["かんじ"]["漢字"]=prob ,tm["かんじ"]={"漢字":prob,"幹事":prob}
tm=defaultdict(lambda: {}) 
edge=defaultdict(lambda: {})
#edge={.....,5:{"漢字":(3,前の単語),}......}
score1=defaultdict(lambda: {})
#score1={"0":{"漢字":prob,"幹事":prob,....},1:{}}


for line in lm_file: #bigram,unigram 単語の遷移の確率
	models=line.strip().split("\t")
	#print models
	lm[unicode(models[0],"utf-8")]=float(models[1])

for line in tm_file: #
	models=line.strip().split() #(type_(EorT),word,pron,prob) かな漢字変換の確率
	pron=models[2]
	word=models[1]
	prob=models[3]
	if models[0]=="E":
		tm[unicode(pron,"utf-8")][unicode(word,"utf-8")]=float(prob)
	else:
		pass
#print tm[unicode("こうせい","utf-8")]

#bigramの平滑化
def prob_bigram(curr_word_prob,curr_prev_prob):
	lambda1=0.95
	lambda2=0.95
	N=10000000
	prob_uni=lambda1*float(curr_word_prob)+(1-lambda1)/N #unigramの平滑化
	prob_bi=lambda2*float(curr_prev_prob)+(1-lambda2)*prob_uni #bigram平滑化
	return prob_bi


	
for line in test_file:
	line=unicode(line.strip(),"utf-8")
	#前向きステップ
	edge[0]["<s>"]=None #最初のノードへのエッジはなし
	score1[0]["<s>"]=0 #[0:<s>]のスコアは0
	for end in range(1,len(line)+1): #単語の終了点
		#score1[end]={}
		#edge[end]={}
		#print end,"折り返し"
		for begin in range(0,end): #単語の開始点
			pron = "".join(line[begin:end]) #対象のひらがな列
			my_tm=tm[pron] #={}

			if len(tm[pron])==0 and len(pron)==1: #対象のひらがな列がtm中に存在するかどうか
				#tm["かんじ"]={"漢字":0.5,"感じ":0.3,...}
				#区切りの長さが１or 変換候補がないとき (意味の無いような区切り方)
				my_tm={pron:10**(-10)} #例えば「ご飯がない」だと,[がな],[な]などは候補が無さそう:確率0にする
			
			#print end
			#print score1[begin].items(),"socre.items"
			#curr_word=各変換候補("漢字","感じ") tm_prob=変換候補に対する確率
			for curr_word,tm_prob in my_tm.items():
				
				#print end,"end",begin,"begin"
				#print score1[begin].items(), "items"
				#print type(score1)
				
				for prev_word,prev_score in score1[begin].items():
					if prev_word == "</s>":
						pass
					else:
						#print end,"2",begin,"2"
						#prob_bigram(curr_word,prev_word) 遷移確率、別で関数定義
						bigram = prob_bigram(lm[curr_word],lm[prev_word+" "+curr_word])
						curr_score = prev_score + -math.log(tm_prob*bigram)

						if not curr_word in score1[end].keys() or curr_score < score1[end][curr_word]:
							if prev_word == "</s>":
								print "prev_word", prev_word, "prev_score",prev_score 
							score1[end][curr_word]=curr_score
							edge[end][curr_word]=(begin,prev_word)
							#print score1[end][curr_word]
						else:
							score1[end][curr_word]=10**10

						if end == len(line):
							#prob_bigram(curr_word,prev_word) 遷移確率、別で関数定義
							prob_bigram_last = prob_bigram(lm["</s>"],lm[curr_word+" "+"</s>"])
							last_score = curr_score + -math.log(prob_bigram_last,2)
							if not "</s>" in score1[end+1].keys() or last_score < score1[end+1]["</s>"]:
								score1[end+1]["</s>"]=last_score
								edge[end+1]["</s>"]=(end,curr_word)
					

	for i, j in edge.items(): #i=順番,j={"漢字":(3,前の単語),....}
		for a,b in j.items(): #a=word , b=(begin,前のワード)
			if b == None:
				print i, a, b 
			else:
				print i, a, b[0], b[1]
    

	#後ろ向きステップ
	words=[]
	next_edge = edge[len(line)+1]["</s>"] #最後のノードにつながるエッジ"l+1 品詞
	while next_edge != (0,"<s>"):
		position = next_edge[0]
		word = next_edge[1]
		words.append(word)
		next_edge = edge[next_edge[0]][next_edge[1]]
	words.reverse()
	print " ".join(words).encode("utf-8")









