About
=====
Bot for posting word of the days, and more

Usage
=====
You need a file `.env` that contains settings, or have environment variables already set. If it doesn't find environment variables, it will try to load from `.env`.

Run the app from the root direction with

	$ python bin/go_wotd.py

Scheduling is done by cron job or similar.

Setting Environment Variables
-----------------------------
Utility for Add Heroku-Config for pushing .env to Heroku App: https://github.com/ddollar/heroku-config

Usage to push vars from .env file to heroku server and overwrite existing values:

	$ heroku config:push --overwrite

Debugging
---------

Add this to code to create breakpoint

	from pudb import set_trace; set_trace()

Git
---

Push to git

	git push origin master

Push to heroku

	git push heroku master