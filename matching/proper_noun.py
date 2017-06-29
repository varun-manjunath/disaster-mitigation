import re
#import CMUTweetTagger
#import cPickle
from collections import defaultdict
import pickle
from nltk.corpus import wordnet as wn
from itertools import product
import location
# need_tag=cPickle.load(open('need_cmu_tag.p','rb'))
# offer_tag= cPickle.load(open('offer_cmu_tag.p','rb'))
#print(need_tag)
# with open('need_cmu_tag.pickle', 'rb') as handle:
# 	need_tag= pickle.load(handle,encoding='latin1')

# with open('offer_cmu_tag.pickle', 'rb') as handle:
# 	offer_tag= pickle.load(handle,encoding='latin1')


loc_preposition_list=['in','from','at','on','to','from','for','near', 'nearby']
need_verb_list=['need','needs','require','requires','wants','want','lack','lacks']
send_verb_list=['send','give','donate','transfer']
after_place_list=['road','rd','street','hospital','park','town','lake','city','town','village','college','school','bank']
of_place_list=['village','town','city','region','outskirts']
of_people_list=['people','victims','survivors']
nepal_stop_list=['nepal','#nepal','nepalese',"nepal's",'earthquake','quake','Earthquake']
location_proper_list=defaultdict(list)
need_location_subject_list=defaultdict(list)
send_location_subject_list=defaultdict(list)

'''
def proper_noun(need_tag):
	proper_noun=defaultdict(list)
	for tags in need_tag:
		for tag in tags[0]:
			if tag[1]=='^':
				if tag[0] in proper_noun:
					proper_noun[tag[0]]+=1
				else:
					proper_noun[tag[0]]=1	


def need_location_dict(need_tag):
	location_proper_list=defaultdict(list)
	need_location_subject_list=defaultdict(list)
	send_location_subject_list=defaultdict(list)

	for tags in need_tag:
		for i in range(1,len(tags[0])-1):
			if tags[0][i][1]=='^':
				add_val=""
				if tags[0][i+1][0].lower() in street_list:
					add_val=" "+tags[0][i+1][0]

				j=i+1
				while j<(len(tags[0])-1):
					if tags[0][j][1]=='^' or tags[0][j][0]==',':
						add_val=add_val+" "+tags[0][j][0]
						j+=1
					else:
						break

				if tags[0][i+1][1]=='^':
					add_val=" "+tags[0][i+1][0]	
				if tags[0][i-1][0].lower() in loc_preposition_list:
					bigram=tags[0][i-1][0]+" "+tags[0][i][0]
					if bigram in location_proper_list:
						location_proper_list[bigram]+=1
					else:
						location_proper_list[bigram]=1

					bigram=tags[0][i-1][0]+" "+tags[0][i][0]+add_val
					if bigram in location_proper_list:
						location_proper_list[bigram]+=1
					else:
						location_proper_list[bigram]=1		
	
				elif tags[0][i+1][1]=='V':
					next_verb=tags[0][i+1][0].lower()
					next_verb_list=wn.synsets(next_verb)

					for verb in need_verb_list:
						need_verbs=wn.synsets(verb)
						for a,b in product(need_verbs,next_verb_list):
							d= wn.wup_similarity(a,b)
							try:
								if d>0.5:
									#print(a,b)
									bigram=tags[0][i][0]+" "+next_verb
									if bigram in need_location_subject_list:
										need_location_subject_list[bigram]+=1
									else:
										need_location_subject_list[bigram]=1	
							except:
								continue			
					for verb in send_verb_list:
						send_verbs=wn.synsets(verb)
						for a,b in product(send_verbs,next_verb_list):
							d= wn.wup_similarity(a,b)
							try:
								if d>0.5:
									#print(a,b)
									bigram=tags[0][i][0]+" "+next_verb
									if bigram in send_location_subject_list:
										send_location_subject_list[bigram]+=1
									else:
										send_location_subject_list[bigram]=1						
							except:
								continue							
				else:				
					continue

def offer_location_dict(offer_tag):
	location_proper_list=defaultdict(list)
	need_location_subject_list=defaultdict(list)
	send_location_subject_list=defaultdict(list)
	for tags in offer_tag:
		for i in range(1,len(tags[0])-1):
			if tags[0][i][1]=='^':
				add_val=""
				if tags[0][i+1][0].lower() in street_list:
					add_val=" "+tags[0][i+1][0]

				j=i+1
				while j<(len(tags[0])-1):
					if tags[0][j][1]=='^' or tags[0][j][0]==',':
						add_val=add_val+" "+tags[0][j][0]
						j+=1
					else:
						break

				if tags[0][i-1][0].lower() in loc_preposition_list:
					bigram=tags[0][i-1][0]+" "+tags[0][i][0]
					if bigram in location_proper_list:
						location_proper_list[bigram]+=1
					else:
						location_proper_list[bigram]=1			
						
				if tags[0][i-1][0].lower() in loc_preposition_list:
					bigram=tags[0][i-1][0]+" "+tags[0][i][0]+add_val
					if bigram in location_proper_list:
						location_proper_list[bigram]+=1
					else:
						location_proper_list[bigram]=1	
				# elif tags[0][i-1][0]==',':
				# 	j=i
				# 	while tags[0][j][1]!='P' and j>1:
				# 		j-=1
				# 	if tags[0][j][1] in loc_preposition_list:
				# 		bigram=tags[0][i-1][0]+" "+tags[0][i][0]+add_val
				# 		if bigram in location_proper_list:
				# 			location_proper_list[bigram]+=1
				# 		else:
				# 			location_proper_list[bigram]=1

				elif tags[0][i+1][1]=='V':
					next_verb=tags[0][i+1][0].lower()
					next_verb_list=wn.synsets(next_verb)

					for verb in need_verb_list:
						need_verbs=wn.synsets(verb)
						for a,b in product(need_verbs,next_verb_list):
							d= wn.wup_similarity(a,b)
							try:
								if d>0.5:
									#print(a,b)
									bigram=tags[0][i][0]+" "+next_verb
									if bigram in need_location_subject_list:
										need_location_subject_list[bigram]+=1
									else:
										need_location_subject_list[bigram]=1	
							except:
								continue			
					for verb in send_verb_list:
						send_verbs=wn.synsets(verb)
						for a,b in product(send_verbs,next_verb_list):
							d= wn.wup_similarity(a,b)
							try:
								if d>0.5:
									#print(a,b)
									bigram=tags[0][i][0]+" "+next_verb
									if bigram in send_location_subject_list:
										send_location_subject_list[bigram]+=1
									else:
										send_location_subject_list[bigram]=1						
							except:
								continue					
				else:				
					continue

'''
def give_location(tags):
	return_name_list=[]
	old_j=0
	for i in range(1,len(tags[0])):
			# if tags[0][i][0].lower().replace('#','') in nepal_stop_list:
			# 	continue 
			if i<old_j:
				continue
			if tags[0][i][1]=='^':
				add_val=""
				# if tags[0][i+1][0].lower() in after_place_list:
				# 	add_val=" "+tags[0][i+1][0]
				place_flag=0
				j=i+1
				while j<(len(tags[0])-1):
					if tags[0][j][0]==' ' or tags[0][j][1]=='&':
						j+=1
					elif tags[0][j][0].lower() in after_place_list:
						add_val=add_val+" "+tags[0][j][0]
						place_flag=1
						j+=1	
					elif tags[0][j][1]=='^' or tags[0][j][0]==',' or tags[0][j][1]=='A':
						add_val=add_val+" "+tags[0][j][0]
						j+=1						
					else:	
						break		
				old_j=j		
				loc_name=tags[0][i][0].replace('#','')+add_val
				if place_flag==1:
					return_name_list.append(loc_name)
					continue
				if tags[0][i-1][0].lower() in loc_preposition_list:
					return_name_list.append(loc_name)
					place_flag=1
				if tags[0][i-1][0].lower()=='of':
					try:
						prev_word=tags[0][i-2][0].lower()
						print(prev_word)
						if prev_word in of_place_list: 
							return_name_list.append(prev_word+" of "+loc_name)
							continue
						if prev_word in of_people_list:
							return_name_list.append(prev_word+" of "+loc_name)
							continue

						prev_word_list=wn.synsets(prev_word)
						both_set=set(of_place_list)|set(of_people_list)
						for item in both_set:
							possible_items=wn.synsets(item)
							for a,b in product(possible_items,prev_word_list):
								d= wn.wup_similarity(a,b)
								try:
									if d>0.5:
										print(a,b)
										place_flag=1
										return_name_list.append(prev_word+" of "+loc_name)
										break			
								except:
									continue
							if place_flag==1:
								break				
					except:	
						continue		
				
				
				#Changed now.

				if place_flag==0:
					prob_location=tags[0][i][0]
					#print(prob_location)
					try:
						if location.is_inside_Nepal(str(prob_location))==1:
							return_name_list.append(prob_location)
					except:
						continue		

				
				

				# elif tags[0][i+1][1]=='V':
				# 	next_verb=tags[0][i+1][0].lower()
				# 	next_verb_list=wn.synsets(next_verb)

				# 	for verb in need_verb_list:
				# 		need_verbs=wn.synsets(verb)
				# 		for a,b in product(need_verbs,next_verb_list):
				# 			d= wn.wup_similarity(a,b)
				# 			try:
				# 				if d>0.5:
				# 					#print(a,b)
				# 					bigram=tags[0][i][0]+" "+next_verb
				# 					if bigram in need_location_subject_list:
				# 						need_location_subject_list[bigram]+=1
				# 					else:
				# 						need_location_subject_list[bigram]=1	
				# 			except:
				# 				continue			
				# 	for verb in send_verb_list:
				# 		send_verbs=wn.synsets(verb)
				# 		for a,b in product(send_verbs,next_verb_list):
				# 			d= wn.wup_similarity(a,b)
				# 			try:
				# 				if d>0.5:
				# 					#print(a,b)
				# 					bigram=tags[0][i][0]+" "+next_verb
				# 					if bigram in send_location_subject_list:
				# 						send_location_subject_list[bigram]+=1
				# 					else:
				# 						send_location_subject_list[bigram]=1						
				# 			except:
				# 				continue					
				# else:				
				# 	continue


	for names in return_name_list:
		print(names)
		names=re.sub('#','',names)
		if names.lower() in nepal_stop_list:	
			try:
				return_name_list.remove(names)
			except:
				continue	

	return return_name_list				













# print("LOCATION")			
# for i in location_proper_list.keys():
# 	print(i,location_proper_list[i])

# print('\n\n')
# print('LOC_Sub_need')
# for i in need_location_subject_list.keys():
# 	print(i,need_location_subject_list[i])

# print("LOC_Sub_send")
# print('\n\n')
# for i in send_location_subject_list.keys():
# 	print(i,send_location_subject_list[i])
# print('\n\n')
# print(need_location_subject_list)
# print(send_location_subject_list)