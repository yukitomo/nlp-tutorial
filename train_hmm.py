 #!/usr/bin/python
#-*-coding:utf-8-*-

import sys 
from collections import defaultdict
import math

learnig_file=open(sys.argv[1],"r")
f=open("the_model_hmm.txt","w")

def learning_HMM(learnig_file):
	from collections import defaultdict
	emit=defaultdict(lambda: 0) #{"tag word":回数}
	transition=defaultdict(lambda: 0) #{"tag1 tag2":回数,.....,}
	context=defaultdict(lambda: 0) #{"tag":回数}

	for line in learnig_file: #入力形式は「natural_JJ のように単語＿品詞タグ」
		previous="<s>" #文頭のtag
		context[previous] += 1
		wordtags = line.split(" ")
		for wordtag in wordtags:
			word_tag=wordtag.split("_")
			word=word_tag[0].strip()
			tag=word_tag[1].strip()
			transition[previous+" "+tag] += 1 #品詞tag→品詞tagへの遷移回数
			context[tag] += 1 #品詞の回数
			emit[tag+" "+word] += 1 #品詞と単語の対応の回数
			previous = tag #次のtagの考慮のためにpreviousに現在のtagを入れる
		transition[previous+" </s>"] += 1 #1文終了のタグ
	"""
	print transition
	print context
	print emit
	"""
	
	for key, value in transition.items():
		previous_next = key.split(" ")
		previous=previous_next[0]
		next=previous_next[1]
		print "T "+key+" "+str(float(value)/context[previous])
		f.write("T "+key+" "+str(float(value)/context[previous])+"\n")

	for key, value in emit.items():
		tag_word = key.split(" ")
		tag=tag_word[0]
		word=tag_word[1]
		print "E "+key+" "+str(float(value)/context[tag])
		f.write("E "+key+" "+str(float(value)/context[tag])+"\n")



learning_HMM(learnig_file)