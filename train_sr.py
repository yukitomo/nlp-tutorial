#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
from collections import defaultdict
from collections import deque
import random


#queue = deque([(1,word1,POS1),(2,word2,POS2)...])未処理の単語のリスト dequeオブジェクト


def CAL_SCORE(weight,feats):
	score = 0
	for k in feats.keys():
		score += weight[k] * feats[k]
	return score

def UPDATE_WEIGHT(w_ans,w_corr,feats):
	for k in feats.keys():
		w_ans[k] -= 1
		w_corr[k] += 1


def SHIFTREDUCE(queue,weight): 
	heads = [-1] #各単語の親のIDを格納 heads = [-1,head1,head2,...]
	stack = [(0,"ROOT","ROOT")] #stack = [(0,"ROOT","ROOT"),(1,"word",POS)]初期のスタック、処理中の単語

	while len(queue) > 0 or len(stack) > 1: #キューが空ではないorスタックが１個以上存在
		feats = MAKEFEATS(stack,queue) #現在のstack,queueから素性を作成
		s_s = CAL_SCORE(weight["SHIFT"],feats) #shiftのスコア
		s_l = CAL_SCORE(weight["LEFT"],feats) #reduce leftのスコア
		s_r = CAL_SCORE(weight["RIGHT"],feats) #reduce rightのスコア
		#print "queue",queue
		#print "stack", stack
		#print "heads", heads
		try:
			if s_s >= s_l and s_s >= s_r and len(queue) >0: #シフトのスコアが一番高くてキューが残っているとき
				#print "SHIFT"
				stack.append(queue.popleft()) #キューの１番目を除去して、stackにアペンドする
				heads.append(0) #スタックに新しい単語が入ってきたら0をアペンド
			elif s_l >= s_r: #reduce left を実行 stack[-2]の親をstack[-1]にする
				#print "LEFT"
				heads[stack[-2][0]] = stack[-1][0]
				stack.pop(-2)
			else: #reduce right を実行 stack[-1]の親をstack[-2]にする
				#print "RIGHT"
				heads[stack[-1][0]] = stack[-2][0]
				stack.pop(-1)
		except:
			#print "SHIFT"
			stack.append(queue.popleft()) #キューの１番目を除去して、stackにアペンドする
			heads.append(0) #スタックに新しい単語が入ってきたら0をアペンド

	return heads




def MAKEFEATS(stack,queue): #素性phiはスタックの最後の2項目,キューの最初の項目をカバー
	phi = {}
	if len(stack) > 1:
		Wneg2 = stack[-2][1] #スタックの最後から2番目の単語
		Pneg2 = stack[-2][2] #スタックの最後から2番目の品詞
	else:
		Wneg2 = "NONE" #スタックの最後から2番目の単語
		Pneg2 = "NONE" #スタックの最後から2番目の品詞

	Wneg1 = stack[-1][1] #スタックの最後から1番目の単語
	Pneg1 = stack[-1][2] #スタックの最後から1番目の品詞
	if len(queue) > 1:
		W0 = queue[0][1] #キューの最初の単語
		P0 = queue[0][2] #キューの最初の品詞
	else:
		W0 = "NONE"
		P0 = "NONE"
	phi[("W-2",Wneg2,"W-1",Wneg1)] = 1
	phi[("W-1",Wneg1,"W0",W0)] = 1
	phi[("W-2",Wneg2,"P-1",Pneg1)] = 1
	phi[("W-1",Wneg1,"P0",P0)] = 1
	phi[("P-2",Pneg2,"W-1",Wneg1)] = 1
	phi[("P-1",Pneg1,"W0",W0)] = 1
	phi[("P-2",Pneg2,"P-1",Pneg1)] = 1
	phi[("P-1",Pneg1,"P0",P0)] = 1
	
	return phi

def SHIFT_ANSWER(queue,corr_heads,unproc):
	heads = corr_heads
	heads.insert(0,-1) #ROOTのヘッドとして-1を先頭にもってくる
	stack = [(0,"ROOT","ROOT")]
	while len(queue) > 0 or len(stack) > 1: #キューが空ではないorスタック1より大きい(リデュースできる)
		print "heads",heads
		print "stack",stack
		print "queue",queue
		#正解の行動 corr
		try: #一番はじめはスタックが１個なのでキーエラーを避けるためにshiftに誘導
			if heads[stack[-1][0]] == stack[-2][0] and unproc[stack[-1][0]] == 0:
				corr = "RIGHT"
			elif heads[stack[-2][0]] == stack[-1][0] and unproc[stack[-2][0]] == 0:
				corr = "LEFT"
			else:
				corr = "SHIFT"
		except:
			corr = "SHIFT"

		if corr == "SHIFT": #シフトのスコアが一番高くてキューが残っているとき
			#print "SHIFT"
			#print "queue",queue
			stack.append(queue.popleft()) #キューの１番目を除去して、stackにアペンドする
				
		elif corr == "LEFT": #reduce left を実行 stack[-2]の親をstack[-1]にする
			#print "LEFT"
			stack.pop(-2)
			unproc[stack[-1][0]] -= 1
		else: #reduce right を実行 stack[-1]の親をstack[-2]にする
			#print "RIGHT"
			stack.pop(-1)
			unproc[stack[-1][0]] -= 1
	"""
	print "heads",heads
	print "stack",stack
	print "queue",queue
	"""





def SHIFTREDUCE_TRAIN(queue,corr_heads,unproc,weight):
	heads = corr_heads
	heads.insert(0,-1)
	stack = [(0,"ROOT","ROOT")]
	while len(queue) > 0 or len(stack) > 1: #キューが空ではないorスタックが2個以上存在

		#行動の予測 ans 
		feats = MAKEFEATS(stack,queue) #現在のstack,queueから素性を作成
		s_s = CAL_SCORE(weight["SHIFT"],feats) #shiftのスコア
		s_l = CAL_SCORE(weight["LEFT"],feats) #reduce leftのスコア
		s_r = CAL_SCORE(weight["RIGHT"],feats) #reduce rightのスコア
		if s_s >= s_l and s_s >= s_r and len(queue) >0:
			ans = "SHIFT"
		elif s_l >= s_r:
			ans = "LEFT"
		else:
			ans = "RIGHT"

		#行動の正解 corr
		try: #一番はじめはスタックが１個なのでキーエラーを避けるためにshiftに誘導
			if heads[stack[-1][0]] == stack[-2][0] and unproc[stack[-1][0]] == 0:
				corr = "RIGHT"
			elif heads[stack[-2][0]] == stack[-1][0] and unproc[stack[-2][0]] == 0:
				corr = "LEFT"
			else:
				corr = "SHIFT"
		except:
			corr = "SHIFT"

		#予測と正解が異なったとき重みの更新
		w_ans = weight[ans]
		w_corr = weight[corr] 
		if ans != corr:
			UPDATE_WEIGHT(w_ans,w_corr,feats)

		#正解データの行動
		if corr == "SHIFT": #シフトのスコアが一番高くてキューが残っているとき
			#print "SHIFT"
			#print "queue",queue
			stack.append(queue.popleft()) #キューの１番目を除去して、stackにアペンドする
				
		elif corr == "LEFT": #reduce left を実行 stack[-2]の親をstack[-1]にする
			#print "LEFT"
			stack.pop(-2)
			unproc[stack[-1][0]] -= 1
		else: #reduce right を実行 stack[-1]の親をstack[-2]にする
			#print "RIGHT"
			stack.pop(-1)
			unproc[stack[-1][0]] -= 1


def main():
	#学習
	weight = {"SHIFT":defaultdict(lambda :0),"RIGHT":defaultdict(lambda :0),"LEFT":defaultdict(lambda :0)}
	queue = deque()
	corr_heads = []
	unproc = defaultdict(lambda :0)
	for i in range(30):
		for line in open(sys.argv[1]): #学習データ
			if not line == "\n":
				line = line.strip().split("\t")
				queue.append((int(line[0]),line[1],line[3])) #ID,word,POS
				corr_heads.append(int(line[6])) #正解の親番号
				unproc[int(line[6])] += 1
			else:
				#SHIFT_ANSWER(queue, corr_heads, unproc)
				SHIFTREDUCE_TRAIN(queue,corr_heads,unproc,weight)
				#初期化
				queue = deque()
				corr_heads = []
				unproc = defaultdict(lambda :0)

	#テスト
	for line in open(sys.argv[2]):
		if not line == "\n":
			line = line.strip().split("\t")
			queue.append((int(line[0]),line[1],line[3])) #ID,word,POS
		else:
			heads = SHIFTREDUCE(queue,weight)
			#print heads
			#初期化
			queue = deque()
			for head in heads[1:]:
				print "\t".join(["*","*","*","*","*","*",str(head),"*"])
			print ""




			
			

	



if __name__ == '__main__':
	main()
