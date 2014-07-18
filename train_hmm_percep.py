#!/usr/bin/python
#-*-coding:utf-8-*-
import math
from collections import defaultdict
from perceptron_module import *
import sys
import random

def CREATE_TRANCE(phi,first_tag,next_tag):
	phi["T"+" "+first_tag+" "+next_tag] += 1
	return phi

def CREATE_EMIT(phi,y,x):
	phi["E"+" "+y+" "+x] += 1
	if not x.islower(): #xがすべて小文字でないとき
		phi["CAPS"+" "+y] += 1
	return phi

def CREATE_FEATURES_tag(X,Y): #X=単語列, Y=品詞列
	phi = defaultdict(lambda:0)
	for i in range(len(Y)+1):
		#インデックスiの品詞の前の品詞がfirst_tag、次の品詞がnext_tag
		if i == 0: 
			first_tag = "<s>" 
		else:
			first_tag = Y[i-1]
		if i == len(Y):
			next_tag = "</s>"
		else:
			next_tag = Y[i]
		phi = CREATE_TRANCE(phi,first_tag,next_tag) #遷移の素性を追加 
	for i in range(len(Y)):
		phi = CREATE_EMIT(phi,Y[i],X[i]) #生成の素性を追加 (大文字の素性も)
	return phi

def HMM_VITERBI(w,X,possible_tags): #wは重み,X:単語列1
	l = len(X) 
	best_score={}
	best_edge={}
	best_score["0 <s>"]=0 #文頭<s>はスコア0
	best_edge["0 <s>"]=None #文頭にくるエッジはなし
	for i in range(l):
		for prev in possible_tags.keys():
			for next_ in possible_tags.keys():
				if (str(i)+" "+prev in best_score.keys())and ("T"+" "+prev+" "+next_ in w.keys()):
					feature_score = float(w["T"+" "+prev+" "+next_] + w["E"+" "+next_+" "+X[i]])
					score =best_score[str(i)+" "+prev] + feature_score
					if not str(i+1)+" "+next_ in best_score.keys() or best_score[str(i+1)+" "+next_] < score:
						best_score[str(i+1)+" "+next_] = score
						best_edge[str(i+1)+" "+next_] = str(i)+" "+prev
					#文末記号を考える
					if i == l-1:
						feature_score = float(w["T"+" "+next_+" "+"</s>"]) #生成確率はなし
						last_score= best_score[str(i+1)+" "+next_] + feature_score
						if not str(i+2)+" "+"</s>" in best_score.keys() or best_score[str(i+2)+" "+"</s>"] < last_score:
							best_score[str(i+2)+" "+"</s>"] = last_score
							best_edge[str(i+2)+" "+"</s>"]=str(i+1)+" "+next_
	#print "best_score",best_score
	"""
	print "best_edge"
	for k,v in sorted(best_edge.items()):
		print k,v
	"""
	#後ろ向きステップ
	Y_hat=[]
	next_edge = best_edge[str(l+1)+" "+"</s>"] #最後のノードにつながるエッジ"l+1 品詞"
	while next_edge != "0 <s>":
		edges=next_edge.split()
		position = edges[0]
		y_hat = edges[1]
		Y_hat.append(y_hat)
		next_edge = best_edge[next_edge]
	Y_hat.reverse()
	return Y_hat




if __name__ == '__main__':
	output_file = open("hmm_percep_myanswer.pos","w")
	w = defaultdict(lambda: random.random()) #重み初期化
	possible_tags = {"<s>":1,"</s>":1} #予めありうるタグを格納
	for line in open(sys.argv[1]): #学習データに登場しうる品詞タグをすべて格納
		x_ys = line.strip().split(" ")
		Y = ["<s>"]
		for x_y in x_ys:
			x_y = x_y.split("_")
			#print x_y
			possible_tags[x_y[1]] = 1
			Y.append(x_y[1])
		Y.append("</s>")
		for i in range(len(Y)-1):
			w["T"+" "+Y[i]+" "+Y[i+1]] = random.random()
	#print w
	#print possible_tags

	#train
	for i in range(2): #イテレーション
		print "iteration" ,i 
		k = 0
		for line in open(sys.argv[1]): #学習データline = "a_X b_Y a_Z" の読み込み
			k += 1
			print "sent",k
			X=[] #単語列
			Y_prime=[] #品詞列
			x_ys = line.strip().split(" ")
			for x_y in x_ys:
				x_y = x_y.split("_")
				X.append(x_y[0])
				Y_prime.append(x_y[1])
			#print X,Y
			Y_hat = HMM_VITERBI(w,X,possible_tags)
			#予測の確認
			"""
			print "X", X
			print "Y_prime", Y_prime
			print "Y_hat", Y_hat
			"""
			"""
			print "Y_prime"
			for i in range(len(X)):
				print X[i]+"_" +Y_prime[i],
			print ""
			
			print "Y_hat"
			for i in range(len(X)):
				print X[i]+"_" +Y_hat[i],
				#output_file.write(X[i]+"_" +Y_hat[i]+" ")
			print ""
			#output_file.write("\n")
			"""
			

		
			phi_prime = CREATE_FEATURES_tag(X, Y_prime) #学習データ
			phi_hat = CREATE_FEATURES_tag(X, Y_hat) #予測データ
			#w += phi_prime - phi_hat
			for key in phi_prime.keys():
				w[key] += phi_prime[key]
			for key in phi_hat.keys():
				w[key] -= phi_hat[key]

	#print w
	#test
	for line in open(sys.argv[2]): #テストデータ
		X = [x for x in line.strip().split()]
		Y_hat = HMM_VITERBI(w,X,possible_tags) 
		#print " ".join(Y_hat)
		for i in range(len(X)):
			print X[i]+"_" +Y_hat[i],
			output_file.write(X[i]+"_" +Y_hat[i]+" ")
		print ""
		output_file.write("\n")

	


 




