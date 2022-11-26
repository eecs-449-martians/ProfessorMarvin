# stored state.py 
# stores the current loaded state with all loaded documents
import pandas as pd
import nltk


class Documents(): 
	def __init__(self): 
		self.passages = pd.DataFrame()
		self.quest_num = 0
		try:
			self.stops = set(nltk.corpus.stopwords.words('english'))
		except ImportError: 
			nltk.download('stopwords')
			self.stops = set(nltk.corpus.stopwords.words('english'))


	def add_passage(self,name,text,summary,question): 
		new_pass = pd.DataFrame([{'name':name,"text":text,"summary":summary,"question":question}])
		self.passages = pd.concat([self.passages,new_pass ],ignore_index=True )

	def delete_doc(self,doc_name): 
		self.passages = self.passages[self.passages.name != doc_name]
	
	def __get_entry(self,query): 
		# gets best match for query, and returns it 
		query_words = query.split(' ')
		score_func = lambda text: sum(sum(word == targ for word in text.split(' ') if word not in self.stops) for targ in query_words if targ not in self.stops)


		scores = self.passages.summary.apply(score_func)
		print(scores)
		if scores.max() < 1: 
			# if no overlap with summary, go to full texts
			print('no scoring elements! switching to passages')
			scores = self.passages.text.apply(score_func)
			if scores.max() < 1: 
				# if no overlap with summary, go to full texts
				print('Still no sorted elements')
				return None

		elt= scores.argmax()
		return self.passages.loc[elt]
		
	def get_passage(self,query): 
		entry = self.__get_entry(query)
		if entry is None: return None 
		return entry['text']

	def get_summary(self,query):
		entry = self.__get_entry(query)
		if entry is None: return None 
		return entry['summary']
	
	def get_question(self,query): 
		entry = self.__get_entry(query)
		if entry is None: return None 
		question_list = entry['question']
		quest_num = self.quest_num %len(question_list)
		self.quest_num +=1
		return question_list[quest_num]
	

	
	
