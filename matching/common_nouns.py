import re
#import CMUTweetTagger
#import cPickle
from collections import defaultdict
import pickle
from nltk.corpus import wordnet as wn
from itertools import product
import spacy
from spacy.symbols import *
from nltk import Tree
import nltk


nlp=spacy.load('en')
np_labels=set(['nsubj','dobj','pobj','iobj','conj','nsubjpass','appos','nmod','poss','parataxis','advmod','advcl'])
subj_labels=set(['nsubj','nsubjpass'])
need_verb_list=['need','require','want','lack']
send_verb_list=['send','give','donate','transfer','distribute','aid','help','procure']
common_resource=['food','water','medicine','tent','clothes','communication','transport','infrastructure','shelter','internet','sanitation','hospital','donations']
modifiers=['nummod','compound','amod','punct']
after_clause_modifier=['relcl','acl','ccomp','xcomp','acomp','punct']#,'nn','quantmod','nmod','hmod','infmod']
verb_count={}
resource_array=[]
modified_array=[]
# nepal_stop_list=['nepal','earthquake','quake','nepalese']
nepal_stop_list=[]
tel_no="([+]?[0]?[1-9][0-9\s]*[-]?[0-9\s]+)"
email="([a-zA-Z0-9]?[a-zA-Z0-9_.]+[@][a-zA-Z]*[.](com|net|edu|in|org|en))"
web_url="http:[a-zA-Z._0-9/]+[a-zA-Z0-9]"
entity_type_list=['NORP','ORG','GPE','PERSON']
quant_no="([0-9]*[,.]?[0-9]+[k]?)"

need_send_verb_list=['need','require','want','lack','send','give','donate','transfer','distribute','aid','help','support','procure']
# def quant_no(resource):
# 	return [i for re.findall(quant_no,resource)]

def modifier_word(word):
	modified_word=word.orth_
	while word.n_lefts+word.n_rights==1 and word.dep_.lower() in modifiers:
		word=[child for child in word.children][0]
		modified_word=word.orth_+" "+modified_word
	return modified_word	



def tok_format(tok):
	return "_".join([tok.orth_, tok.dep_,tok.ent_type_])

def to_nltk_tree(node):
	if node.n_lefts + node.n_rights > 0:
		return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
	else:
		return tok_format(node)

def get_children(word,resource_array,modified_array):
	#print(word,word.dep_)
	for child in word.children:
		if child.dep_.lower() in modifiers:
			get_word=modifier_word(child)+" "+word.orth_+"<_>"+word.dep_
			modified_array.append(get_word)
		if child.dep_.lower()=='prep' or child.dep_.lower()=='punct':
			get_children(child,resource_array,modified_array)	
		if child.dep_.lower() in after_clause_modifier:	
			#print(child, child.dep_)
			get_children(child,resource_array,modified_array)	
		if child.dep_.lower() in np_labels:			
			get_children(child,resource_array,modified_array)
			resource_array.append(child.orth_+"<_>"+child.dep_)		
		else:
			if get_verb_similarity_score(child.orth_,common_resource)>0.7 :
				get_children(child,resource_array,modified_array)

def get_verb_similarity_score(word,given_list):
	max_verb_similarity=0
	if word.lower() in given_list:
		max_verb_similarity=1
	else:	
		current_verb_list=wn.synsets(word.lower())
		for verb in given_list:
			related_verbs=wn.synsets(verb)
			for a,b in product(related_verbs,current_verb_list):
				d=wn.wup_similarity(a,b)
				try:
					if d> max_verb_similarity:
						max_verb_similarity=d
				except:
					continue
	return max_verb_similarity				
		
def resource_in_list(resource):
	related_resources=wn.synsets(resource)
	max_similarity=0
	chosen_word=""
	if resource.lower() in common_resource:
		return 1,resource
	for word in common_resource:
		related_words=wn.synsets(word)
		#print(word,related_words)
		for a,b in product(related_words,related_resources):
			d=wn.wup_similarity(a,b)
			try:
				if d> max_similarity:
					max_similarity=d
					chosen_word=word
			except:
				continue
	return max_similarity,chosen_word




def get_resource(text):
	doc=nlp(text)
	# try:
	# 	[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
	# except:
	# 	print("Exception here")
	org_list=[]
	prev_word=""
	prev_word_type=""
	for word in doc:
		if word.ent_type_ in entity_type_list:
			org_list.append(word.orth_+"<_>"+word.ent_type_)
		else:
			org_list.append("<_>")

	resource_array=[]
	modified_array=[]
	for word in doc:
		if  get_verb_similarity_score(word.orth_,need_send_verb_list)>0.8 or word.dep_=='ROOT':
			get_children(word,resource_array,modified_array)

		if word.dep_=='cc' and word.n_lefts+word.n_rights==0:
			ancestor=word.head.orth_
			#print(ancestor)
			if get_verb_similarity_score(ancestor,common_resource)>0.6:
				get_children(word.head,resource_array,modified_array)

	#print(resource_array)		
	#print(modified_array)
	last_word=[]
	# for resource in modified_array:
	# 	print(resource)
	# 	print(resource, resource_in_list(resource.lower()))
	# for word in modified_array:
	# 	last_word.append(word.split(' ')[-1])

	final_resource={}
	modified_array_2=[]
	resource_array_2=[]
	n_subj_list=[]

	for i in modified_array:
		modified_array_2.append(i[:(i.index("<_>"))])

	for i in resource_array:
		resource_array_2.append(i[:(i.index("<_>"))])


	for resources in modified_array_2:
		max_val_resource=0
		val_type=""
		resource_list=resources.rstrip().split(" ")
		for resource in resource_list:
			pres_res_val,pres_res_type=resource_in_list(resource)
			if pres_res_val> max_val_resource:
				val_type=pres_res_type
				max_val_resource=pres_res_val			
		if max_val_resource > 0.6:
			final_resource[resources]=val_type

	for resource in resource_array_2:
		#print(resource)
		pres_res_val,pres_res_type=resource_in_list(resource)
		if pres_res_val> 0.6:
			if resource not in final_resource:
				final_resource[resource]=pres_res_type
	

	final_resource_keys=list(final_resource.keys())

	
	prev_word_type=""
	prev_word=""
	org_list_2=[]
	poss_places=[]
	for i in org_list:
		index=i.index("<_>")
		if i[index+3:]=='GPE' and i[:index] in final_resource_keys:

			#final_resource_keys.remove(i[:index])
			poss_places.append(i[:index])

		if i[index+3:]=="ORG" and prev_word_type=="ORG":
			prev_word=prev_word+" "+i[:index]
		elif i[index+3:]=="PERSON" and prev_word_type=="PERSON":	
			prev_word=prev_word+" "+i[:index]

		else:
			if prev_word !='':
				org_list_2.append(prev_word+"<_>"+prev_word_type)
			prev_word_type=i[index+3:]
			prev_word=i[:index]

	quantity_dict={}
	for i in final_resource:
		for j in re.findall(quant_no,i):
			quantity_dict[i]=j

	source_list=[]
	org_person_list=[]
	
	for i in org_list_2:
		tag=i[i.index("<_>")+3:]
		j=i[:i.index("<_>")]

		if tag=="ORG" or tag=="PERSON":
			if j.lower() not in nepal_stop_list:
				org_person_list.append(j)
		elif j.lower() not in nepal_stop_list and j not in quantity_dict.keys():
			source_list.append(j)
		else:
			continue	
	
	for i in modified_array:
		pos_res=i[:i.index("<_>")]
		pos_tag=i[i.index("<_>")+3:]
		if pos_tag in subj_labels:
			if pos_res not in source_list and pos_res not in final_resource_keys and pos_res.lower() not in  nepal_stop_list:
				#print(pos_tag,pos_res)
				source_list.append(pos_res)

	for i in resource_array:
		pos_res=i[:i.index("<_>")]
		pos_tag=i[i.index("<_>")+3:]
		if pos_tag in subj_labels:
			if pos_res not in source_list and pos_res not in final_resource_keys and pos_res.lower() not in  nepal_stop_list:
				#print(pos_tag,pos_res)
				source_list.append(pos_res)				



	return quantity_dict,final_resource_keys,source_list,poss_places,org_person_list

		


def get_contact(text):
	numbers=re.findall(tel_no,text)
	print("Contact Information")
	for i in numbers:
		if len(i)>=7:
			print(i)
			#test_file.write(str(i)+",")

	#test_file.write('\nMail:')		
	mails= re.findall(email,text)
	for i in mails:
		print("Mail: "+i)	
		#test_file.write(str(i)+",")
