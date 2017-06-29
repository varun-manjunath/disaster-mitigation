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
import sys 
from nltk.stem import *
import spacy
nlp=spacy.load('en')

#

tknzr=TweetTokenizer(strip_handles=True,reduce_len=True)

import CMUTweetTagger
stop_words=get_stop_words('en')

stop_words_2=['i','me','we','us','you','u','she','her','his','he','him','it','they','them','who','which','whom','whose','that','this','these','those','anyone','someone','some','all','most','himself','herself','myself','itself','hers','ours','yours','theirs','to','in','at','for','from','etc',' ',',']

for i in stop_words_2:
	if i not in stop_words:
		stop_words.append(i)

nepal_stop_list=['nepal','earthquake','quake','nepalese','italy']
nepal_re="(nepal|quake|earthquake|nepalese|Earthquake|Nepal|NEPAL|Quake|Earth|Italy|italy)+"

count=0
need_text=[]
offer_text=[]
location_list=[]

id_need_list=[]
global_need_resource_list=[]
id_offer_list=[]
global_offer_resource_list=[]


count=0

need_file=open(sys.argv[1]+'_needs.txt','r')
for line in need_file:
	line=line.rstrip()
	index=line.find('<||>')
	given_id=line[:index]
	if given_id not in id_need_list:
		id_need_list.append(given_id)
		line=line[index+4:]
		need_text.append(line)

count=0
offer_file=open(sys.argv[1]+'_offers.txt','r')
for line in offer_file:
	line=line.rstrip()
	index=line.find('<||>')
	given_id=line[:index]
	if given_id not in id_offer_list:
		id_offer_list.append(given_id)
		line=line[index+4:]
		offer_text.append(line)

## CSV FILES 

# needfile=open('needs.csv','r',encoding='utf-8')
# offerfile=open('offers.csv','r',encoding='utf-8')
# for line in needfile:
# 	line=line.rstrip().split('\t')
# 	count+=1

# 	given_id=int(float(line[0]))
# 	if given_id not in id_need_list:
# 		id_need_list.append(int(float(line[0])))
# 		need_text.append(line[1])
# 		for j in range(len(line),9):
# 			line.append('')
# 	else:
# 		continue	
# count=0
# for line in offerfile:
# 	line=line.rstrip().split('\t')
# 	count+=1
# 	given_id=int(float(line[0]))
# 	if given_id not in id_offer_list:
# 		id_offer_list.append(int(float(line[0])))
# 		offer_text.append(line[1])
# 		for j in range(len(line),9):
# 			line.append('')
# 	else:
# 		continue			


		
web_url="http[s]?:[a-zA-Z._0-9/]+[a-zA-Z0-9]"
replacables="RT\s|-\s|\s-|#|@"
prop_name="([A-Z][a-z]+)"
num="([0-9]+)"
name="([A-Za-z]+)"
and_rate="([&][a][m][p][;])"
ellipses="([A-Za-z0-9]+[…])"
mentions="([a-zA-z\s0-9]+[:])"

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

def post_preprocess(text,global_need_resource_list,final_resource_keys,quantity_dict,loc_list,source_list):

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

	print(final_resource_keys)

	global_need_resource_list.append(final_resource_keys)

def create_resource_list(global_need_resource_list,need_text):
	count=0
	for text in need_text:
		#output_test_file.write(str(count+1)+": "+text+"\n")
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
			if i not in loc_list: #and location.is_inside_Nepal(i)==1:
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

		

		
		post_preprocess(text,global_need_resource_list,final_resource_lists,quantity_dict,loc_list,source_list)
			
create_resource_list(global_need_resource_list,need_text)
create_resource_list(global_offer_resource_list,offer_text)

print(global_offer_resource_list)
print(global_need_resource_list)
print(need_text)
print(offer_text)

import pickle
with open(sys.argv[1]+'_global_offer_resource_list.p','wb') as handle:
	pickle.dump(global_offer_resource_list,handle,2)

with open(sys.argv[1]+'_global_need_resource_list.p','wb') as handle:
	pickle.dump(global_need_resource_list,handle,2)	

with open(sys.argv[1]+'_need_text.p','wb') as handle:
	pickle.dump(need_text,handle,2)	

with open(sys.argv[1]+'_offer_text.p','wb') as handle:
	pickle.dump(offer_text,handle,2)		

with open(sys.argv[1]+'_id_need_list.p','wb') as handle:
	pickle.dump(id_need_list,handle,2)

with open(sys.argv[1]+'_id_offer_list.p','wb')as handle:
	pickle.dump(id_offer_list,handle,2)





	# print("Resource_list")
	# print(final_resource_keys)
	# print()
	# print("Quantity dictionary")		
	# print(quantity_dict)
	# print()
	# print("Location")
	# print(loc_list)
	# print()
	# common_nouns.get_contact(text,output_test_file)
	# print()
	# output_test_file.write("\nSource List:")
	# print("Source list")
	# for i in source_list:
	# 	output_test_file.write(str(i)+",")
	# 	if i not in global_source_dict:
	# 		global_source_dict[i]=1
	# 	else:
	# 		global_source_dict[i]+=1

	# print(source_list)
	# output_test_file.write("\n\n")
	# print()				