#!/usr/bin/python
#-*-coding:utf-8-*-
import math
from collections import defaultdict
from perceptron_module import *
import sys
import random

def PREDICT_ONE_tanh(w,phi): #w={}, 
	score=0
	for name, value in phi.items(): #phi={"UNI:COP3":2.0, "UNI:Cabinet":15.0, "UNI:Cable":6.0,....}
		score += value*float(w[name]) #素性の回数*重みをスコアに足し込む
	return math.tanh(score)
	

def PREDICT_NN(network,phi): #networkが重みの[(1,w0),(1,w2),....],phiは素性
	y=[phi,{},{}] #各層の値
	for i in range(len(network)): #各ノードi=(0,1,2) network[i] = (1,w(i)) network =[(1,w0),(1,w1),(2,w2)]
		layer = network[i][0] #1,2
		weight = network[i][1] #w1,w2
		"""
		print "layer = ", layer
		print "weight = ", weight
		print "y[layer-1] = ", y[layer-1]
		"""
		answer = PREDICT_ONE_tanh(weight,y[layer-1]) #前の層の値にもとづいて計算
		#print "answer = ",answer
		y[layer][i] = answer #ノードiからの出力
	return y


def UPDATE_NN(network,phi,ydash):
	sigma = 0 #シグマの初期化
	lambda0 = 0.5
	delta = {} #エラーのリスト
	y = PREDICT_NN(network, phi) #現在のnetworkにおけるyの予想値
	"""
	print "phi = ",phi
	print "network = ",network
	print "y = ",y
	""" 
	for j in reversed(range(len(y))): #yのインデックスの逆順 j = 2,1,0
		#print "(layer,weight) = ",network[j]
		#print "delta = ",delta
		layer = network[j][0]
		#print "network[j][1] = ",network[j][1]
		w = network[j][1]
		if j == len(network)-1 : #jが最後のノードのとき
			delta[j] = ydash - y[j][2] #学習データのラベルydashと最後の層の予想値y(ノード2)との差
		else:
			for i in delta.keys(): #すべてのデルタの要素と重みの要素をかける
				"""
				print "(i,j) = ",i,j
				print "delta[i] = ",delta[i]
				print "w = ",w
				print "w[i] = ",w[i]
				"""
				sigma += delta[i]*w[i]
			delta[j] = (1-y[layer-1][j]*y[layer-1][j])*sigma
			sigma = 0 
	for j in range(len(network)):
		layer = network[j][0]
		w = network[j][1]
		for name, val in y[layer-1].items():
			w[name] += lambda0 * delta[j] *val

def make_network(): #network =[(1,w0),(1,w1),(2,w2)]
	#weight = defaultdict(lambda:random.random())
	network = [(1,defaultdict(lambda:random.random())),(1,defaultdict(lambda:random.random())),(2,defaultdict(lambda:random.random()))]
	return network

def predict_all_nn(network,testfile):
	for line in testfile:
		phi = CREATE_FEATURES(line)
		ydash = PREDICT_NN(network, phi)
		if ydash[-1][2] >= 0:
			print 1
		else:
			print -1
		



if __name__ == '__main__':
	network = make_network() #network =[(1,w0),(1,w1),(2,w2)]
	#train = open(sys.argv[1])
	test = open(sys.argv[2])
	#学習
	for i in range(1000): #イテレーション
		for line in open(sys.argv[1]): #trainにするとイテレーションがまわらなくなる
			words = line.strip().split("	")
			x = words[1]
			ydash = float(words[0]) #ラベル
			phi = CREATE_FEATURES(x) #素性の回数の辞書
			#phi = {'UNI:site': 1, 'UNI:Maizuru': 1, 'UNI:Kyoto': 1, 'UNI:located': 1, 'UNI:,': 2, 'UNI:in': 1, 'UNI:A': 1}
			UPDATE_NN(network,phi,ydash) #ydashは学習データのラベル

	#print network

	#テスト
	predict_all_nn(network,test)








