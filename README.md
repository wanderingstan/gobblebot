
Setting Environment Variables
=============================
Utility for Add Heroku-Config for pushing .env to Heroku App: https://github.com/ddollar/heroku-config

Usage to push vars from .env file to heroku server and overwrite existing values:

	$ heroku config:push --overwrite

Debugging
=========

Add this to code to create breakpoint

	from pudb import set_trace; set_trace()

Git
===

Push to git

	git push origin master

Push to heroku

	git push heroku master