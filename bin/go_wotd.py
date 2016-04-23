import sys, os, pprint, datetime, argparse

import praw, trello
# Our stuff
import read_env, send_email, trello_2_reddit

# Debug output
pp = pprint.PrettyPrinter(indent=4)

# Arguments
parser = argparse.ArgumentParser(description='Post word of the day.')
parser.add_argument('post_days', metavar='N', type=int, nargs='*',
                   help='Days of the week to post. Monday is 0 and Sunday is 6.')
args = parser.parse_args()

# Test day of week
weekday = datetime.datetime.today().weekday()
if (weekday not in args.post_days):
	print ("Skipping because today's day of week (%s) is not in list of post days." % weekday)
	exit()

if 'BOT_NAME' not in os.environ:
	# Environment variables are not set, try to read from .env file
	import read_env
	read_env.read_env()

try:
	#
	# Do it! Actually post the WotD!
	#
	(reddit_post, trello_card) = trello_2_reddit.post_trello_to_reddit(os.environ)
except praw.errors.InvalidUserPass:
	print ("Invalid reddit username/password.")
	exit()

# # TODO: Add WotD to subreddit wiki
# # https://praw.readthedocs.org/en/latest/pages/code_overview.html#praw.__init__.AuthenticatedReddit.edit_wiki_page

print "Trello response"
pp.pprint(trello_card)
print "Reddit/Praw response"
pp.pprint(reddit_post)
print "Word was " + trello_card['name']
print "Reddit URL is " + reddit_post.url

# Email mods
message = "Posted card to reddit. Title was:\n%s\nAnd body was:\n%s\nReddit URL is:%s\n\nGobble gobble!" % (
	trello_card['name'],
	trello_card['desc'],
	reddit_post.url)
send_email.send_email(
	os.environ['EMAIL_TO'].split(','),
	"WotD Posted",
	message,
	os.environ)

