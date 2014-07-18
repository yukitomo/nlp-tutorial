#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
from collections import defaultdict
train=open(sys.argv[1],"r")
from perceptron_module import *

w=defaultdict(lambda: 0)
model=open("the_model_perceotron.txt","w")

def train_perceptron(train,w):
	for line in train: #学習ファイルの各行
		words = line.strip().split("	")
		x = words[1] #センテンス
		y = words[0] #ラベル
		phi = CREATE_FEATURES(x) #各単語の回数を数え、phi={"UNI:COP3":-2.0, "UNI:Cabinet":-15.0, "UNI:Cable":-6.0....}
		ydash = PREDICT_ONE(w,phi) #素性*重みのスコア
		#print phi 
		#print ydash
		if ydash != y: #スコアが学習データのラベルと異なったら(y=負の値,ydash=正の値だとすると、重みは負に更新される)
			UPDATE_WEIGHTS(w,phi,y)
		
if __name__ == '__main__':	
	for i in range(5):
		train_perceptron(train,w)
	for name in sorted(w.keys()):
		print name+"	"+str(w[name])
		model.write(name+"	"+str(w[name])+"\n")

