import os
import Trello2Reddit
import pprint
import praw, trello

# Debug output
pp = pprint.PrettyPrinter(indent=4)

config = {

	#
	# Reddit
	#

	'bot_name' : unicode(os.environ['BOT_NAME']),
	'admin_reddit_user' : unicode(os.environ['ADMIN_REDDIT_USER']),
	'bot_reddit_user' : unicode(os.environ['BOT_REDDIT_USER']),
	'bot_reddit_password' : unicode(os.environ['BOT_REDDIT_PASSWORD']),
	'subreddit' : unicode(os.environ['SUBREDDIT']),

	#
	# Trello
	#

	# Key for this Trello Application
	# Generate here:
	# 	https://trello.com/1/appKey/generate
	'trello_app_key' : os.environ['TRELLO_APP_KEY'],
	# User Access Token
	# Generate here:
	# 	https://trello.com/1/authorize?key=substitutewithyourapplicationkey&name=My+Application&expiration=never&response_type=token&scope=read,write
	'trello_token' : os.environ['TRELLO_TOKEN'],
	# Board that we are working on
	'trello_board_id' : os.environ['TRELLO_BOARD_ID'],
	# List that we pull cards from and post them
	'trello_queue_list_id' : os.environ['TRELLO_QUEUE_LIST_ID'],
	# List that we move cards to after posting
	'trello_finished_list_id' : os.environ['TRELLO_FINISHED_LIST_ID'],
}


print config

try:
	# Do it!
	(reddit_post, trello_card) = Trello2Reddit.post_trello_to_reddit(config)
except praw.errors.InvalidUserPass:
	print ("Invalid reddit username/password. Tried %s and %s" % (config['bot_reddit_user'],config['bot_reddit_password']))
	exit()

	# TODO: Add WotD to subreddit wiki
	# https://praw.readthedocs.org/en/latest/pages/code_overview.html#praw.__init__.AuthenticatedReddit.edit_wiki_page


# Optional send of confirmation email
# See here: http://www.nixtutor.com/linux/send-mail-through-gmail-with-python/
import smtplib  
msg = "Posted card to reddit. Title was:\n%s\nAnd body was:\n%s\nReddit URL is:%s\n\nGobble gobble!" % (
	card_to_post['name'],
	card_to_post['desc'],
	submission.url
)  
server = smtplib.SMTP(config['email_server'])  
server.starttls()  
server.login(config['email_username'],config['email_password'])  
server.sendmail(config['email_from'], config['email_to'], msg)  
server.quit()  


print "Trello response"
pp.pprint(trello_card)

print "Reddit/Praw response"
pp.pprint(reddit_post)

print "Posted latest WotD to Reddit. (Hopefully)"

