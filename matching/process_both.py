import csv
import io
import pickle
import proper_noun 
import os
import subprocess
import common_nouns
import location
import re
from stop_words import get_stop_words
from nltk.tokenize import TweetTokenizer
from collections import defaultdict
import pickle
from nltk.corpus import wordnet as wn
from itertools import product
import spacy
from spacy.symbols import *
from nltk import Tree
import nltk
from nltk.stem import *
import spacy
nlp=spacy.load('en')
import math
import sys
from gensim.models import *
import numpy as np
import sys 
from nltk.stem import *
import spacy
import time
import CMUTweetTagger
stop_words=get_stop_words('en')

stop_words_2=['i','me','we','us','you','u','she','her','his','he','him','it','they','them','who','which','whom','whose','that','this','these','those','anyone','someone','some','all','most','himself','herself','myself','itself','hers','ours','yours','theirs','to','in','at','for','from','etc',' ',',']

for i in stop_words_2:
	if i not in stop_words:
		stop_words.append(i)

nepal_stop_list=['nepal','earthquake','quake','nepalese','italy']
nepal_re="(nepal|quake|earthquake|nepalese|Earthquake|Nepal|NEPAL|Quake|Earth|Italy|italy)+"
		
web_url="http[s]?:[a-zA-Z._0-9/]+[a-zA-Z0-9]"
replacables="RT\s|-\s|\s-|#|@"
prop_name="([A-Z][a-z]+)"
num="([0-9]+)"
name="([A-Za-z]+)"
and_rate="([&][a][m][p][;])"
ellipses="([A-Za-z0-9]+[…])"
mentions="([a-zA-z\s0-9]+[:])"



nlp=spacy.load('en')
model=KeyedVectors.load_word2vec_format('/media/hdd/hdd/crisisNLP_word2vec_model/crisisNLP_word_vector.bin',binary=True)

dict_file=open('built_dict_italy.txt','r')
prannay_dict={}
for line in dict_file:
	line=line.rstrip().split(',')
	prannay_dict[line[0]]=line[1]

from nltk.stem.lancaster import LancasterStemmer
stem2=LancasterStemmer()
import numpy as np


wc2_vector_array=np.load('/media/hdd/hdd/data_backup/results/nepal/Need/wc2_nepal_2_word_embeddings.npy')

global_offer_resource_list=[]
global_need_resource_list=[]
id_need_list=[]
offer_text=[]
need_text=[]
id_offer_list=[]

import pickle


with open('nepal_global_offer_resource_list.p','rb') as handle:
	global_offer_resource_list=pickle.load(handle)

with open('nepal_global_need_resource_list.p','rb') as handle:
	global_need_resource_list= pickle.load(handle)	

with open('nepal_need_text.p','rb') as handle:
	need_text=pickle.load(handle)	

with open('nepal_offer_text.p','rb') as handle:
	offer_text=	pickle.load(handle)		

with open('nepal_id_need_list.p','rb') as handle:
	id_need_list= pickle.load(handle)

with open('nepal_id_offer_list.p','rb')as handle:
	id_offer_list= pickle.load(handle)

# print(len(global_need_resource_list))
# print(len(global_offer_resource_list))
# print(len(offer_text))
# print(len(need_text))
# print(len(nepal_id_need_list))
# print(len(nepal_id_offer_list))


need_send_verb_list=['need','require','want','lack','send','give','donate','transfer','distribute','aid','help','earthquake','victims']

stemmer=PorterStemmer()
out_stem_list=[stemmer.stem(i.lower()) for  i in need_send_verb_list]
lanc_stem_list=[stem2.stem(i.lower()) for i in need_send_verb_list]


def euclidean_norm(u):
	prod=0
	for i in range(0,len(u)):
		prod=prod+u[i]*u[i]
	return math.sqrt(prod)	

def cosine_similarity(u,v):
	if len(u)==len(v):
		e1=euclidean_norm(u)
		e2=euclidean_norm(v)
		if e1==0 or e2==0:
			return 0
		length=len(u)
		scalar_product=0
		for i in range(length):
			scalar_product=scalar_product+u[i]*v[i]
		return scalar_product/(e1*e2)

def get_list_1(need_tweet_list):
	need_res_set=[]
	for i in need_tweet_list:
		for j in i.split():
			if stemmer.stem(j.lower()) not in out_stem_list:
				need_res_set.append(j.lower())
	return list(set(need_res_set))	

def get_list_2(need_tweet_list):
	need_res_set=[]
	for i in need_tweet_list:
		for j in i.split():
			if stem2.stem(j.lower()) not in lanc_stem_list:
				need_res_set.append(j.lower())
	return list(set(need_res_set))		


def get_set_1(need_tweet_list):
	need_res_set=set()
	for i in need_tweet_list:
		for j in i.split():
			if stemmer.stem(j.lower()) not in out_stem_list:
				need_res_set.add(stemmer.stem(j.lower()))
	return need_res_set		

def resource_similarity_score_via_exact_word_match_1(need_res_set,offer_tweet_list):
	if len(need_res_set)==0:
		return 0
	
	offer_res_set=set()
	for i in offer_tweet_list:
		for j in i.split():
			if j not in out_stem_list:
				offer_res_set.add(stemmer.stem(j.lower()))

	return(len(offer_res_set&need_res_set)/len(need_res_set))

def get_similarity_score_1(word,given_list):
	max_similarity=0
	if word.lower() in given_list:
		max_similarity=1
	else:	
		current_verb_list=wn.synsets(word.lower())
		for verb in given_list:
			related_verbs=wn.synsets(verb)
			for a,b in product(related_verbs,current_verb_list):
				d=wn.wup_similarity(a,b)
				try:
					if d> max_similarity:
						max_similarity=d
				except:
					continue
	return max_similarity	

def get_similarity_score_2(word,given_list):
	max_similarity=0
	flag1=0
	flag2=0
	if word.lower() in given_list:
		max_similarity=1
	else:
		try:
			u=model[word]
		except:
			u=model['unk']
			flag1=1
		for item in given_list:	
			try:
				v=model[item]
			except:
				v=model['unk']
				flag2=1

			if flag1==1 and flag2==1:
				d=0	
			else:		
				d=cosine_similarity(u,v)

			if d >max_similarity:
				max_similarity=d
		

	return max_similarity			

def get_similarity_score_3(word,given_list):
	max_similarity=0
	flag1=0
	flag2=0
	if word.lower() in given_list:
		max_similarity=1
	else:
		try:
			u=wc2_vector_array[int(prannay_dict[word])]
		except:
			u=wc2_vector_array[0]
			flag1=1

		for item in given_list:
			
			try:
				v=wc2_vector_array[int(prannay_dict[item])]
			except:
				v=wc2_vector_array[0]		
				flag2=1
			
			if flag1==1 and flag2==1:
				d=0
			else:		
				d=cosine_similarity(u,v)

			if d>max_similarity:
				max_similarity=d

	return max_similarity			

def resource_similarity_score_via_wc2_2(input_need_res_list,offer_tweet_list):
	offer_tweet_list=get_list_2(offer_tweet_list)
	l1=len(input_need_res_list)
	

	value=0
	for item in input_need_res_list:
		temp=get_similarity_score_3(item,offer_tweet_list)
		value=value+temp

	return value/l1	

def resource_similarity_score_via_wc2_1(need_vector,offer_tweet_list):
	offer_tweet_list_2=get_list_2(offer_tweet_list)
	l2=len(offer_tweet_list)	
	offer_vector=np.zeros(256)

	if l2 ==0:
		return 0

	for i in offer_tweet_list_2:
		try:
			v2=wc2_vector_array[int(prannay_dict[i.lower()])]
		except:
			v2=wc2_vector_array[0]

		for j in range(len(offer_vector)):
			offer_vector[j]+=v2[j]

	offer_vector=[i/l2 for i in offer_vector]
	
	return cosine_similarity(need_vector,offer_vector)	

def resource_similarity_score_via_word_net_1(need_res_set,offer_tweet_list):
	if len(need_res_set)==0:
		return 0
	value=0
	offer_res_list=[]
	for i in offer_tweet_list:
		for j in i.split():
			if stemmer.stem(j.lower()) not in out_stem_list:
				offer_res_list.append(stemmer.stem(j.lower()))

	for word in need_res_set:
		temp= get_similarity_score_1(word,offer_res_list)
		if temp > 0.6:
			value=value+temp

	return value/len(need_res_set)		

def resource_similarity_score_via_word_vec_1(need_vector,offer_tweet_list):
	offer_tweet_list_2=get_list_1(offer_tweet_list)
	l2=len(offer_tweet_list)	
	offer_vector=np.zeros(300)

	if l2 ==0:
		return 0

	for i in offer_tweet_list_2:
		try:
			v2=model[i.lower()]
		except:
			v2=model['unk']

		for j in range(len(offer_vector)):
			offer_vector[j]+=v2[j]

	offer_vector=[i/l2 for i in offer_vector]
	
	return cosine_similarity(need_vector,offer_vector)	
	
def resource_similarity_score_via_word_vec_2(input_need_res_list,offer_tweet_list):
	offer_tweet_list=get_list_1(offer_tweet_list)
	l1=len(input_need_res_list)
	#print(offer_tweet_list)

	value=0
	for item in input_need_res_list:
		temp=get_similarity_score_2(item,offer_tweet_list)
		value=value+temp

	return value/l1		

def get_top_k_searches_1(input_id,k,method,outfile,idfile):
		outfile.write('\n'+need_text[id_need_list.index(input_id)]+'\n')
		#print(need_text[id_need_list.index(input_id)])
		input_need_res_set=get_set_1(global_need_resource_list[id_need_list.index(input_id)])
		score_array={}
		if method==1:
			for item in id_offer_list:
				score_array[item]=resource_similarity_score_via_exact_word_match_1(input_need_res_set,global_offer_resource_list[id_offer_list.index(item)])

		if method==2:
			for item in id_offer_list:
				score_array[item]=resource_similarity_score_via_word_net_1(input_need_res_set,global_offer_resource_list[id_offer_list.index(item)])		

		if method==3:
			input_need_res_list=get_list_1(global_need_resource_list[id_need_list.index(input_id)])
			l1=len(input_need_res_list)		
			if l1==0:
				for item in id_offer_list:
					score_array[item]=0
			else:		
				need_vector=np.zeros(300)
				for i in input_need_res_list:
					try:
						v1=model[i.lower()]
					except:
						v1=model['unk']

					for j in range(300):
						need_vector[j]+=v1[j]

				need_vector=[i/l1 for i in need_vector]		
				for item in id_offer_list:
					score_array[item]=resource_similarity_score_via_word_vec_1(need_vector,global_offer_resource_list[id_offer_list.index(item)])	

		if method ==4:
			input_need_res_list=get_list_1(global_need_resource_list[id_need_list.index(input_id)])
			l1=len(input_need_res_list)	

			if l1==0:
				for item in id_offer_list:
					score_array[item]=0
			else:
				for item in id_offer_list:
					score_array[item]=resource_similarity_score_via_word_vec_2(input_need_res_list,global_offer_resource_list[id_offer_list.index(item)])	
										

		
		if method==5:
			input_need_res_list=get_list_2(global_need_resource_list[id_need_list.index(input_id)])
			l1=len(input_need_res_list)		
			if l1==0:
				for item in id_offer_list:
					score_array[item]=0
			else:		
				need_vector=np.zeros(256)
				for i in input_need_res_list:
					try:
						v1=wc2_vector_array[int(prannay_dict[i])]
					except:
						v1=wc2_vector_array[0]

					for j in range(256):
						need_vector[j]+=v1[j]

				need_vector=[i/l1 for i in need_vector]		
				for item in id_offer_list:
					score_array[item]=resource_similarity_score_via_wc2_1(need_vector,global_offer_resource_list[id_offer_list.index(item)])	


		if method==6:
			input_need_res_list=get_list_2(global_need_resource_list[id_need_list.index(input_id)])
			l1=len(input_need_res_list)	

			if l1==0:
				for item in id_offer_list:
					score_array[item]=0
			else:
				for item in id_offer_list:
					score_array[item]=resource_similarity_score_via_wc2_2(input_need_res_list,global_offer_resource_list[id_offer_list.index(item)])	
								

		score_array_sorted_keys=sorted(score_array,key=score_array.get,reverse=True)
		count=0
		
		for r in score_array_sorted_keys:
			outfile.write(str(score_array[r])+'\t'+offer_text[id_offer_list.index(r)]+'\n')
			# if method==5 or method ==6:
			print(str(score_array[r])+'\t'+offer_text[id_offer_list.index(r)])
			idfile.write(str(input_id)+'\t'+str(r)+'\n')
			if count==k:
				return
			count+=1	
	
def get_top_k_searches_2(resource_list,k,method,need_offer_flag):

		print('HERE I AM IN TOP SEARCHES')	

		input_need_res_set=get_set_1(resource_list)
		score_array={}
		print(need_offer_flag)
		print(k)
		print(method)



		if need_offer_flag==1:
			id_need_offer_list=id_offer_list
			global_need_offer_resource_list=global_offer_resource_list
			need_offer_text=offer_text
		else:
			id_need_offer_list=id_need_list
			global_need_offer_resource_list=global_need_resource_list
			need_offer_text=need_text	

		if method==1:
			for item in id_need_offer_list:
				score_array[item]=resource_similarity_score_via_exact_word_match_1(input_need_res_set,global_need_offer_resource_list[id_need_offer_list.index(item)])

		if method==2:
			for item in id_need_offer_list:
				score_array[item]=resource_similarity_score_via_word_net_1(input_need_res_set,global_need_offer_resource_list[id_need_offer_list.index(item)])		

		if method==3:
			input_need_res_list=get_list_1(resource_list)
			l1=len(input_need_res_list)		
			if l1==0:
				for item in id_need_offer_list:
					score_array[item]=0
			else:		
				need_vector=np.zeros(300)
				for i in input_need_res_list:
					try:
						v1=model[i.lower()]
					except:
						v1=model['unk']

					for j in range(300):
						need_vector[j]+=v1[j]

				need_vector=[i/l1 for i in need_vector]		
				for item in id_need_offer_list:
					score_array[item]=resource_similarity_score_via_word_vec_1(need_vector,global_need_offer_resource_list[id_need_offer_list.index(item)])	

		if method ==4:
			input_need_res_list=get_list_1(resource_list)
			l1=len(input_need_res_list)	

			if l1==0:
				for item in id_need_offer_list:
					score_array[item]=0
			else:
				for item in id_need_offer_list:
					score_array[item]=resource_similarity_score_via_word_vec_2(input_need_res_list,global_need_offer_resource_list[id_need_offer_list.index(item)])	
										

		
		if method==5:
			input_need_res_list=get_list_2(resource_list)
			l1=len(input_need_res_list)		
			if l1==0:
				for item in id_need_offer_list:
					score_array[item]=0
			else:		
				need_vector=np.zeros(256)
				for i in input_need_res_list:
					try:
						v1=wc2_vector_array[int(prannay_dict[i])]
					except:
						v1=wc2_vector_array[0]

					for j in range(256):
						need_vector[j]+=v1[j]

				need_vector=[i/l1 for i in need_vector]		
				for item in id_need_offer_list:
					score_array[item]=resource_similarity_score_via_wc2_1(need_vector,global_need_offer_resource_list[id_need_offer_list.index(item)])	


		if method==6:
			input_need_res_list=get_list_2(resource_list)
			l1=len(input_need_res_list)	

			if l1==0:
				for item in id_need_offer_list:
					score_array[item]=0
			else:
				for item in id_need_offer_list:
					score_array[item]=resource_similarity_score_via_wc2_2(input_need_res_list,global_need_offer_resource_list[id_need_offer_list.index(item)])	
								

		score_array_sorted_keys=sorted(score_array,key=score_array.get,reverse=True)
		count=0
		
		for r in score_array_sorted_keys:
			print(str(score_array[r])+'\t'+need_offer_text[id_need_offer_list.index(r)])
			if count==k:
				return
			count+=1	



tknzr=TweetTokenizer(strip_handles=True,reduce_len=True)


def tweet_preprocess(text):
	#text=" ".join(tknzr.tokenize(text))
	text=re.sub(web_url,'',text)
	text=re.sub(mentions,'',text)
	text=re.sub(ellipses,'',text)
	text=re.sub(and_rate,'and',text)
	text=re.sub(str(num)+''+name,"\\1 \\2",text)
	text=re.sub(name+''+str(num),"\\1 \\2",text)
	text=re.sub(prop_name+''+prop_name,"\\1 \\2",text)
	return text.lstrip().rstrip()

def tweet_preprocess2(text):
	#text=" ".join(tknzr.tokenize(text))
	text=re.sub(web_url,'',text)
	text=re.sub(mentions,'',text)
	text=re.sub(ellipses,'',text)
	text=re.sub(and_rate,'and',text)
	text=re.sub(replacables,'',text)
	#text=re.sub(mentions,'',text)
	text=" ".join(tknzr.tokenize(text))
	text=re.sub(str(num)+''+name,"\\1 \\2",text)
	text=re.sub(name+''+str(num),"\\1 \\2",text)
	text=re.sub(prop_name+''+prop_name,"\\1 \\2",text)
	return text.lstrip().rstrip()	

verb_dict={}
common_resource=['food','water','medicine','tent','clothes','communication','transport','infrastructure','shelter','internet','sanitation','hospital','donations','blood']

def post_preprocess(text,final_resource_keys,quantity_dict,loc_list,source_list,which_k,which_method,need_offer_flag):

	##########  Remove the  nepal stop list terns ###############

	final_resource_keys_2=[]
	for i in final_resource_keys:
		final_resource_keys_2.append(re.sub(nepal_re,'',i))

	source_list_2=[]	
	for i in source_list:
		source_list_2.append(re.sub(nepal_re,'',i))		

	loc_list_2=[]
	for i in loc_list:
		loc_list_2.append(re.sub(nepal_re,'',i))	
	
	source_list=list(source_list_2)
	loc_list=list(loc_list_2)
	final_resource_keys=list(final_resource_keys_2)

	#########################################################
	for i in source_list_2:
		if i.lower() in stop_words:
			try:
				source_list.remove(i)		
			except:
				continue	

	for j in loc_list:
		for i in source_list_2:
			if i in j:
				try:
					source_list.remove(i)	
				except:
					continue	

	
	#########  Remove the terms duplicates #############				
	source_list_2=list(source_list)

	for i in final_resource_keys_2:
		length=len(final_resource_keys)
		for j in range(length):
			if i in final_resource_keys[j] and len(i) < len(final_resource_keys[j]):
				try:
					final_resource_keys.remove(i)
					break
				except:
					continue	

	final_resource_keys_2=list(final_resource_keys)


	for i in source_list_2:
		length=len(source_list)
		for j in range(length):
			if i in source_list[j] and len(i) < len(source_list[j]):
				try:
					source_list.remove(i)
					break
				except:
					continue	

	source_list_2=list(source_list)
						
	for i in loc_list_2:
		length=len(loc_list)
		for j in range(length):
			if i in loc_list[j] and len(i)< len(loc_list[j]):
				try:
					loc_list.remove(i)
					break
				except:
					continue	

	loc_list_2=list(loc_list)

	######################################################

	source_list_2=list(source_list)
	for j in loc_list:
		for i in source_list_2:
			if j in i:
				try:	
					source_list.remove(j)
				except:
					continue				

	for i in final_resource_keys_2:
		for j in loc_list:
			if i in j:
				try:
					final_resource_keys.remove(i)
				except:
					continue	

	final_resource_keys_2=list(final_resource_keys)

	loc_list_2=list(loc_list)
	source_list_2=list(source_list)			
	

	##################################################				
	for i in final_resource_keys_2:
		if i.lower().rstrip().lstrip() in stop_words:
			try:
				final_resource_keys.remove(i)
			except:
				continue	

	for i in loc_list_2:
		i=re.sub('#','',i)
		if i.lower().rstrip().lstrip() in stop_words:
			try:
				loc_list.remove(i)
			except:
				continue	

	for i in source_list_2:
		if i.lower().rstrip().lstrip() in stop_words:
			try:
				source_list.remove(i)
			except:
				continue	


	if len(final_resource_keys)==0:
		doc=nlp(text)
		for word in doc:
			if word.pos_=='NOUN':
				final_resource_keys.append(word.orth_)


	#global_need_resource_list.append(final_resource_keys)
	print("Resource_list")
	print(final_resource_keys)
	print()
	print("Quantity dictionary")		
	print(quantity_dict)
	print()
	print("Location")
	print(loc_list)
	print()
	common_nouns.get_contact(text)
	print()
	print("Source list")
	print(source_list)

	get_top_k_searches_2(final_resource_keys,which_k,which_method,need_offer_flag)

def create_resource_list(need_text_2,which_k,which_method,need_offer_flag):
	count=0
	start_time=time.time()
	for text in need_text_2:
		source_list_3=[]

		urls=re.findall(web_url,text)		
		for i in urls:
			if len(i)>len('http://t.co'):
				source_list_3.append(i)	


		text2=tweet_preprocess(text)
		need_cmu_tags=CMUTweetTagger.runtagger_parse([text2])

		text=tweet_preprocess2(text)
		quantity_dict={}
		final_resource_keys=[]
		source_list=[]
		loc_list=[]
		poss_places=[]
		org_person_list=[]
		quantity_dict,final_resource_keys,source_list,poss_places,org_person_list= common_nouns.get_resource(text)	

		for i in source_list_3:
			source_list.append(i)

		# print(count)	
		print(text)
		doc=nlp(text)		
		#need_tag.append(CMUTweetTagger.runtagger_parse([text]))			

		loc_list=proper_noun.give_location(need_cmu_tags)

		
		for i in org_person_list:
			if i in loc_list:
				try:
					loc_list.remove(i)						
				except:
					continue	
			if i not in source_list:
				source_list.append(i)

		for i in loc_list:
			if i in source_list:
				try:
					source_list.remove(i)
				except:
					continue	

		for i in poss_places:
			if i not in loc_list and location.is_inside_Nepal(i)==1:
				loc_list.append(i)

		for i in org_person_list:
			if i in final_resource_keys:
				try:
					final_resource_keys.remove(i)
				except:
					continue	

		count=count+1
		final_resource_lists=[]	
		for key in final_resource_keys:
			if key in quantity_dict:
				final_resource_lists.append(key.split(' ')[-1])
				continue	
			if key in text:
				final_resource_lists.append(key)
		
		post_preprocess(text,final_resource_lists,quantity_dict,loc_list,source_list,which_k,which_method,need_offer_flag)

		print(time.time()-start_time)
		start_time=time.time()
		

need_text_2=[]
need_text_2.append('There are many people stranded in Kathmandu')
which_k=4
which_method=3
need_offer_flag=1		

create_resource_list(need_text_2,which_k,which_method,need_offer_flag)



		