# -*- coding: utf-8 -*-
import glob
import random
import os

class Markov(object):

	def __init__(self):		
		try:
			my_dir = os.path.dirname(os.path.realpath(__file__))
			my_path = my_dir + "/books"
			
			self.words = []
			self.cache = {}
			self.end_sentences = []
			
			for filename in glob.glob(os.path.join(my_path, '*.txt')):
				open_file = open(filename)
				self.words = self.words + self.file_to_words(open_file)
			words_length = len(self.words)
			if words_length < 3:
				print 'None or not enough text to process.'
			else:
				self.word_size = len(self.words)
				self.database()
			
		except Exception, e:
			print e


	def file_to_words(self, open_file):
		open_file.seek(0)
		data = open_file.read()
		words = data.split()
		return words
		

	def triples(self):
		if len(self.words)<3:
			return
		for i in range(len(self.words)-2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			# Yield does this: 
		

	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1,w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
			if (w2[-1:] == '.' or w2[-1:] == '?' or w2[-1:] == '!' or w2[-1:] == ';' or w2[-1:]==','):
					self.end_sentences.append(key)

	def generate_markov_text(self,size=25):
		# From my first try...
		#seed = random.randint(0,self.word_size-3)		
		#seed_word, next_word = self.words[seed], self.words[seed+1]
		seed_key = random.choice(self.end_sentences)
		seed_w2 = seed_key[1]
		for value in self.cache[(seed_key)]:
			key = (seed_w2, value)
			if key in self.cache:
				seed_word, next_word = seed_w2, value
				break
			else:
				continue
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1,w2)])
			if i==size-1:
				while 1:
					key = (w1,w2)
					if key in self.end_sentences:
						break
					else:
						w1, w2 = w2, random.choice(self.cache[(w1,w2)])

		gen_words.append(w2)
		gen_words = gen_words[1:]
		sentence =  ' '.join(gen_words).capitalize()
		if sentence[-1] == ',' or sentence[-1] == ';':
			sentence = sentence[:-1]+'.'
		return sentence


if __name__ == "__main__":
    markov = Markov()
    text = markov.generate_markov_text()
    print text
