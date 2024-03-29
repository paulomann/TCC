from models.model import *
import re
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import codecs
import string
import unicodedata

with codecs.open('data/stopwords.data', encoding='utf-8', mode='r') as f:
	stop_words = [str(x).replace("\n", "").strip().lower() for x in f]

def remove_entities(text, entities):
	new_text = _replace_entities(entities.get_hashtags(), text)
	new_text = _replace_entities(entities.get_symbols(), new_text)
	new_text = _replace_entities(entities.get_user_mentions(), new_text)
	new_text = _replace_entities(entities.get_urls(), new_text)
	return new_text

def _replace_entities(entity, text):
	new_text = text
	for i in entity:
		pattern = re.compile(i, re.IGNORECASE)
		new_text = pattern.sub("", new_text)
	return new_text

def tokenize_tweet(text):
	global stop_words
	text = text.lower()
	tokenizer = TweetTokenizer()
	tokens = tokenizer.tokenize(text)
	tokens = [tok for tok in tokens if tok not in stop_words and not tok.isdigit()]
	return tokens

def check_token_validity(token):
	if '' == token:
		return False
	elif '#' in token:
		return False
	elif '.' in token:
		return False
	elif ',' in token:
		return False
	elif ';' in token:
		return False
	elif ':' in token:
		return False
	elif '~' in token:
		return False
	elif '´' in token:
		return False
	elif '`' in token:
		return False
	elif "'" in token:
		return False
	elif '<' in token:
		return False
	elif '>' in token:
		return False
	elif '=' in token:
		return False
	elif '{' in token:
		return False
	elif '}' in token:
		return False
	elif '(' in token:
		return False
	elif ')' in token:
		return False
	elif '&' in token:
		return False
	elif '%' in token:
		return False
	elif '$' in token:
		return False
	elif '@' in token:
		return False
	elif '!' in token:
		return False
	elif '*' in token:
		return False
	elif '^' in token:
		return False
	elif '?' in token:
		return False
	elif '/' in token:
		return False
	elif '\\' in token:
		return False
	return not repetitive_word(token)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ascii', 'ignore')
    return only_ascii.decode('ascii', 'ignore')

def repetitive_word(token):
	for char in token:
		count = 0
		for i in range(len(token)):
			if char == token[i]:
				count = count + 1
		if count > 5:
			return True
	return False

def process_tokens(tokens):
	new_tokens = []
	for t in tokens:
		try:
			st = remove_accents(t)
			if len(st.split('-')) >= 2:
				st = st[0]
			valid = check_token_validity(st)
		except UnicodeDecodeError as t:
			print(e)
			print("CHARACTER PROBLEM :", st)
		if valid:
			new_tokens.append(st)
	return new_tokens