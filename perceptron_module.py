#!/usr/bin/python
#-*-coding:utf-8-*-
from collections import defaultdict

def CREATE_FEATURES(x): #センテンスを受け取り、各単語(素性)の回数を返す
	phi=defaultdict(lambda: 0) #各素性の辞書
	words = x.strip().split() #センテンスを単語で区切る
	for word in words: #各単語の回数を数える
		phi["UNI:"+word] += 1
	return phi #phi={"UNI:COP3":2.0, "UNI:Cabinet":15.0, "UNI:Cable":6.0,....}


def PREDICT_ONE(w,phi): #w={}, 
	score=0
	for name, value in phi.items(): #phi={"UNI:COP3":2.0, "UNI:Cabinet":15.0, "UNI:Cable":6.0,....}
		if name in w.keys(): #w(重み)のキーにバリューがあれば
			score += value*float(w[name]) #素性の回数*重みをスコアに足し込む
	if score >= 0:
		return 1
	else:
		return -1

def UPDATE_WEIGHTS(w,phi,y):
	for name, value in phi.items():
		w[name]+=float(value)*float(y)

def PREDICT_ALL(model_file,input_file):
	w=defaultdict(lambda: 0)
	phi=defaultdict(lambda: 0)
	count=0
	y=[]
	for line in model_file:
		words = line.strip().split("	")
		w[words[0]]=words[1]
	for x in input_file:
		count += 1
		phi=CREATE_FEATURES(x)
		ydash = PREDICT_ONE(w,phi)
		#print "No."+str(count)+": "+str(ydash)
		print ydash

def train_perceptron(train,w):
	for line in train: #学習ファイルの各行
		words = line.strip().split("	")
		x = words[1] #センテンス
		y = words[0] #ラベル
		phi = CREATE_FEATURES(x) #各単語の回数を数え、phi={"UNI:COP3":-2.0, "UNI:Cabinet":-15.0, "UNI:Cable":-6.0....}
		ydash = PREDICT_ONE(w,phi) #素性*重みのスコア
		if ydash != y: #スコアが学習データのラベルと異なったら(y=負の値,ydash=正の値だとすると、重みは負に更新される)
			UPDATE_WEIGHTS(w,phi,y)


	
