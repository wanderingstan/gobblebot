import praw, time
from trello import TrelloApi

def post_trello_to_reddit(config):
	"""Post latest Trello card to reddit. 

	Return's a tuple of the Trello card
	object and a created PRAW submission object.
	"""
	
	# Login to Reddit
	user_agent = (config['BOT_NAME']+" by /u/"+config['ADMIN_REDDIT_USER'])
	r = praw.Reddit(user_agent=user_agent)
	r.login(config['BOT_REDDIT_USER'], config['BOT_REDDIT_PASSWORD'])

	# Login to Trello
	trello = TrelloApi(config['TRELLO_APP_KEY'], token=config['TRELLO_TOKEN'])

	# Get cards in Queued List
	queued_cards = trello.lists.get(
		config['TRELLO_QUEUE_LIST_ID'],
		cards='open',
		card_fields='name,pos,desc,labels,due',
		fields='name')['cards']
	card_to_post = queued_cards[0]

	# Get cards in Finished List
	finished_cards = trello.lists.get(
		config['TRELLO_FINISHED_LIST_ID'],
		cards='open',
		card_fields='name,pos',
		fields='name')['cards']
	last_finished_card = finished_cards[0]
	
	# TODO: Look through the 'due' dates and see if any cards is 'due' today,
	# in which case it should be posted instead of the first

	# Format our post title
	new_card_name = (card_to_post['name'] + " " + 
		time.strftime("%m/%d").replace('0', ''));
	new_card_desc = card_to_post['desc']
	if len(card_to_post['desc'])==0:
		# Redit requires there to be *some* text in a text post!
		new_card_desc="Word of the day."

	# Create Reddit post from the card
	reddit_submission = r.submit(
		config['SUBREDDIT'], 
		new_card_name, 
		text=new_card_desc)

	# Add a comment indicating that the card was posted, with link to post
	comment_text = ("I posted this card to /r/%s with URL\n%s" % (
		config['SUBREDDIT'],
		reddit_submission.url))
	trello.cards.new_action_comment(
		card_to_post['id'],
		comment_text)

	# Move the card to FINISHED list
	trello_updated_card = trello.cards.update(
		card_to_post['id'], 
		idList=config['TRELLO_FINISHED_LIST_ID'])

	# # TODO: Move the card to the *top* of the FINISHED list
	# # See here: http://stackoverflow.com/questions/14446859/what-does-the-pos-actually-mean-in-the-trello-api
	# # The trello API has no method for changing the 'pos' field
 #    resp = requests.put("https://trello.com/1/cards/%s" % (card_id), params=dict(key=self._apikey, token=self._token), data=dict(name=name, desc=desc, closed=closed, idList=idList, due=due))
 #    resp.raise_for_status()

	return reddit_submission, trello_updated_card
