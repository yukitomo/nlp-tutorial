#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
from collections import defaultdict
import math

nonterm=[]
preterm=defaultdict(lambda :[]) #preterm={単語:[(lhs,prob),(lhs,prob).....]}

def PRINT_TREE(S,best_edge,words): #S=(sym,i,j)
	if S in best_edge.keys(): #終端記号のとき
		return "("+S[0]+" "+PRINT_TREE(best_edge[S][0],best_edge,words)+" "+PRINT_TREE(best_edge[S][1],best_edge,words)+")"
	else:
		return "("+S[0]+" "+words[S[1]]+")"





#文法読み込み “lhs \t rhs \t prob \n”
for rule in open(sys.argv[1]):
	rule = rule.strip().split("\t") #lhs,rhs,prob
	lhs=rule[0]
	rhs=rule[1]
	prob=float(rule[2])
	#print rule
	rhs_symbols=rhs.split(" ") #rhsの中身をspaceでスプリット
	if len(rhs_symbols) == 1: #rhsが一個のみのときは終端記号 rhs=単語
		preterm[rhs_symbols[0]].append((lhs,-math.log(prob))) #preterm[単語]=[(lhs,prob),(lhs,prob).....]
	else:
		nonterm.append((lhs,rhs_symbols[0],rhs_symbols[1],-math.log(prob))) #nonterm=[(遷移元,遷移先1,遷移先2,確率),(),....]
#print "preterm", preterm
#print "nonterm", nonterm

#テスト文の読み込み
for line in open(sys.argv[2]):
	words=line.strip().split()
	#best_score=defaultdict(lambda :0) #={(sym,i,i+1):score,....}
	best_score={}
	best_edge={}
	
	#文の各単語に対して前終端記号を付加
	for i in range(len(words)):
		pretermlist = preterm[words[i]] #インデックスiの単語に対する前集単語記号のリスト
		#print pretermlist
		for lhs_prob in pretermlist: #lhs_probs=(lhs,probs)
			#print lhs_prob
			best_score[(lhs_prob[0],i,i+1)]=lhs_prob[1]
	"""
	print "best_score_preterm"
	for k,v in best_score.items():
		print k,v
	('DT', 2, 3) 0.510825623766
	('NN', 6, 7) 3.91202300543
	('NN', 3, 4) 3.21887582487
	('NN', 1, 2) 4.60517018599
	('NP_PRP', 0, 1) 0.916290731874
	('VBD', 1, 2) 2.99573227355
	('IN', 4, 5) 3.50655789732
	('DT', 5, 6) 0.510825623766
	"""

	#非終端記号の組み合わせ
	for j in range(len(words)+1)[2:]: #スパンの右側 j=2,3,...len(words)
		for i in range(j-1)[::-1]:#スパンの左側 i=j-2,j-3,...0
			for k in range(i+1,j): #kはlsymの終了点でrsymの開始点
				for sym_lsym_rsym_prob in nonterm:
					sym=sym_lsym_rsym_prob[0]
					lsym=sym_lsym_rsym_prob[1]
					rsym=sym_lsym_rsym_prob[2]
					logprob=sym_lsym_rsym_prob[3]
					if (lsym,i,k) in best_score.keys() and (rsym,k,j) in best_score.keys():
						my_lp = best_score[(lsym,i,k)] + best_score[(rsym,k,j)] + logprob
						if not (sym,i,j) in best_score.keys() or my_lp < best_score[(sym,i,j)]:
							best_score[(sym,i,j)]=my_lp
							best_edge[(sym,i,j)]=((lsym,i,k),(rsym,k,j))
	"""
	print "best_score"
	for k,v in best_score.items():
		print k,v

	print "best_edge"
	for k,v in best_edge.items():
		print k,v
	"""
	print PRINT_TREE(('S',0,len(words)),best_edge,words)







