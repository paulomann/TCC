from models.model import Tweet, User, Entities
from controllers import database_controller
import atexit
from util.normalizer import *

def init_database():
	database_controller.open_database_connection()

def exit_handler(): 
	database_controller.commit()
	database_controller.close()

atexit.register(exit_handler)

def save_data_to_database(data_json):
	tweet = create_tweet_object(data_json)
	user = create_user_object(data_json)

	#if(not((tweet is None) or (user is None))):
		#database_controller.insert_data(tweet, user)

def create_tweet_object(data_json):
	""" Creates an object of type Tweet with the
		data in the data_json arg """

	user_json = data_json.get("user", None)

	if(validate_twitter(data_json)):

		source_device = normalize_source_device(str(data_json.get("source")))
		
		t = normalize_time(data_json.get("created_at"))

		print(data_json.get("text") + " | " + str(data_json.get("retweeted_status", None)))

		"""entities = create_entities_object(data_json.get("entities"))
		print("+++++++++++++++++++")
		print(data_json.get("text"))
		print("----------------------")
		print(entities)
		print("+++++++++++++++++++")
		#print(data_json.get("entities"))
		#print("-----------------------")"""

		tweet = Tweet(data_json.get("text"), data_json.get("id_str"), 
					  source_device, t, user_json.get("id"))

		return tweet

	return None

def create_user_object(data_json):
	""" Creates an object of type User with the
		data in the user_json arg """
	user_json = data_json.get("user", None)
	if(user_json is not None):

		user = User(user_json.get("id"), user_json.get("friends_count", 0), 
			user_json.get("description", None), user_json.get("location", None), 
			user_json.get("followers_count", 0))
		return user
	return None

def create_entities_object(entities):
	hashtags = []
	for ht in entities.get("hashtags"):
		hashtags.append(ht)
	urls = []
	for u in entities.get("urls"):
		urls.append(u)
	user_mentions = []
	for um in entities.get("user_mentions"):
		user_mentions.append(um)
	symbols = []
	for s in entities.get("symbols"):
		symbols.append(s)
	media = False
	if(entities.get("media", None) is not None):
		media = True
	return Entities(hashtags, user_mentions, urls, symbols, media)

def validate_twitter(data_json):
	""" This function return a bool value wether the
		tweet is valid or not regarding the restrictions
		of the programmer """
	user_json = data_json.get("user", None)
	reply = False
	if(data_json.get("in_reply_to_screen_name") is not None):
		reply = True
	retweet = False
	if(data_json.get("retweeted_status", None) is not None):
		retweet = True
	id_str = True
	if(data_json.get("id_str", None) is None):
		id_str = False

	return (user_json is not None) and (not reply) and (not retweet) and id_str
