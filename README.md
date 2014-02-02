
== Setting Environment Variables ==

Add Heroku-Config for pushing .env to Heroku App: https://github.com/ddollar/heroku-config

Usage to push vars from .env file to heroku server and overwrite existing values:

	$ heroku config:push --overwrite

== Debugging ==

Add this to code to create breakpoint

	from pudb import set_trace; set_trace()
