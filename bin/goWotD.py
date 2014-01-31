import os, re
import Trello2Reddit
import pprint
import praw, trello

# Debug output
pp = pprint.PrettyPrinter(indent=4)

def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the project root
    directory.
    """
    try:
        with open('../.env') as f:
            content = f.read()
    except IOError:
        content = ''
        print "Cout not read env file"
 
    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)

# Load our environment variables
read_env()

# Load configuration from environment variables 
# (These are set in .env file, which for security is not in git)
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
	(reddit_submission, trello_response) = Trello2Reddit.post_trello_to_reddit(config)
except praw.errors.InvalidUserPass:
	print ("Invalid reddit username/password. Tried %s and %s" % (config['bot_reddit_user'],config['bot_reddit_password']))
	exit()

print "Trello response"
pp.pprint(trello_response)

print "Posted latest WotD to Reddit. (Hopefully)"

