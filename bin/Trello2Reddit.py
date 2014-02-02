import praw, time
from trello import TrelloApi

def post_trello_to_reddit(config):
	"""
	Post latest Trello card to reddit. Return's a tuple of the Trello card
	object and a created PRAW submission object.
	"""
	
	# Login to Reddit
	user_agent = (config['bot_name']+" by /u/"+config['admin_reddit_user'])
	r = praw.Reddit(user_agent=user_agent)
	r.login(config['bot_reddit_user'], config['bot_reddit_password'])

	# Login to Trello
	trello = TrelloApi(config['trello_app_key'], token=config['trello_token'])

	# Get cards in Queue 
	queued_cards = trello.lists.get(
		config['trello_queue_list_id'],
		cards='open',
		card_fields='name,pos,desc,labels,due',
		fields='name')['cards']
	card_to_post = queued_cards[0]
	
	# TODO: Look through the 'due' dates and see if any cards is 'due' today,
	# in which case it should be posted instead of the first

	# Create Reddit post from the card
	reddit_submission = r.submit(
		config['subreddit'], 
		card_to_post['name'], 
		text=card_to_post['desc'])

	# Add a note to desc indicating that the card was posted, with link to post
	new_desc = ("%s\n\n(%s posted to /r/%s on %s with URL %s)" % (
		card_to_post['desc'], 
		config['bot_name'], 
		config['subreddit'],
		time.strftime("%Y-%m-%d"),
		submission.url))

	# Move the card to FINISHED list, update description
	trello_updated_card = trello.cards.update(
		card_to_post['id'], 
		idList=config['trello_finished_list_id'], 
		desc=new_desc)

	# TODO: Move the card to the *top* of the FINISHED list
	# See here: http://stackoverflow.com/questions/14446859/what-does-the-pos-actually-mean-in-the-trello-api

	return reddit_submission, trello_updated_card
