#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Carol Padiernos'
SITENAME = "Carol Padiernos's Blog"
# FIRST_NAME = 'Carol'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
# FEED_ALL_RSS
# FEED_ATOM
# FEED_RSS
CATEGORY_FEED_ATOM = None
# CATEGORY_FEED_RSS
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
         # ('Python.org', 'http://python.org/'),
         # ('Jinja2', 'http://jinja.pocoo.org/'),
         # ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('Twitter', 'https://twitter.com/carolpadiernos'),
         # ('Github', 'https://github.com/cpadiernos'),
         # ('LinkedIn', 'https://linkedin.com/in/carolpadiernos')
         # )

# TWITTER = 'https://twitter.com/carolpadiernos'
# GITHUB = 'https://github.com/cpadiernos'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = [
    'images',
    ]
    
THEME = './notmyidea-custom/'
