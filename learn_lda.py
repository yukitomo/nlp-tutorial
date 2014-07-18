#!/usr/bin/python
#-*-coding:utf-8-*-
import random
import sys
from collections import defaultdict
import math

def SAMPLEONE(probs): #probs=[] リスト型 prob=[0.5,0.2,0.1,0.2]のような形
	z=sum(probs) #各確率の和、正規化項をつくる
	remaining=random.uniform(0,z) #float型
	for i in range(len(probs)): #i=0,1,2...
		remaining -=  probs[i]
		if remaining <= 0:
			return i
"""
確率が高いものをiでリターンしやすくなる関数
i=0,1,2
probs=[0.5,0.3,0.2]

SAMPLEONE(probs):
z=1.0
remaining=0.3 だとすると
	i=0:
	remaining = 0.3 - 0.5 =-0.2
	 return i=0
remaining=0.9 だとすると
	i=0:
	remaining=0.9-0.5=0.4
	i=1:
	rem
	aining=0.4-0.3=0.1
	i=2:
	remaining=0.1-0.2=-0.1
	return i=2
remaining=0.5　だとすると
	i=0:
	remaining=0.5-0.5=0
	return i=0
"""

def ADDCOUNTS(word,topic,docid,amount,xcounts,ycounts): 
	xcounts[str(topic)] += amount
	xcounts[word+"|"+str(topic)] += amount 
	ycounts[str(docid)] += amount
	ycounts[str(topic)+"|"+str(docid)] += amount

if __name__ == "__main__":
	NUM_TOPICS=2
	xcorpus=[] #各x,yの格納
	ycorpus=[] 
	xcounts=defaultdict(lambda: 0) #各x,yのカウントを格納
	ycounts=defaultdict(lambda: 0)
	alpha = 0.0001
	beta = 0.0001

	for line in open(sys.argv[1]):
		docid = len(xcorpus) #最初は空なので0,文のdocIDを取得.最後にxcorpusにリストがアペンドされるので毎回＋１となる
		words = line.strip().split()
		topics=[] #単語のトピックをランダム初期化
		for word in words: #各単語に対して一つのトピックをランダムに与える
			topic = random.randint(0,NUM_TOPICS) #0~NUM_TOPICSの値をint型でランダムに出力
			topics.append(topic) 
			ADDCOUNTS(word,topic,docid,1,xcounts,ycounts) #topic,docidは数値
		xcorpus.append(words) #lineの単語のリストを格納
		ycorpus.append(topics) #lineの各単語に対応したトピックのリストを格納
	for i in range(10):
		print i
		for i in range(len(xcorpus)): #各文,各トピックス
			II=0
			nx=len(set(xcorpus[i]))
			ny=len(set(ycorpus[i]))
			for j in range(len(xcorpus[i])): #各単語、各トピック
				x=xcorpus[i][j]
				y=ycorpus[i][j]
				ADDCOUNTS(x,y,i,-1,xcounts,ycounts) #各カウントの-1減算
				probs=[]
				for k in range(NUM_TOPICS): #トピックkの確率
					#x=単語,k=トピック,i=docID
					prob = float(xcounts[x+"|"+str(k)]+alpha)/(xcounts[str(k)]+alpha*nx)*float(ycounts[str(k)+"|"+str(i)]+beta)/(ycounts[str(i)]+beta*ny) #平滑化をいれたい
					probs.append(prob)
				new_y=SAMPLEONE(probs)
				#print probs
				#print probs[new_y]
				II += math.log(probs[new_y])
				ADDCOUNTS(x,new_y,i,1,xcounts,ycounts) #カウントの加算
				ycorpus[i][j]=new_y
			#print II
	"""
	for x in xcorpus:
		print x
	for y in ycorpus:
		print y
	"""
	dictyxs=defaultdict(lambda: [])
	for  i in range(len(xcorpus)):
		for j in range(len(xcorpus[i])):
			dictyxs[ycorpus[i][j]].append(xcorpus[i][j])

	for k,v in dictyxs.items():
		print k,set(v)








