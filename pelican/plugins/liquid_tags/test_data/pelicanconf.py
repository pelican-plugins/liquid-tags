#!/usr/bin/env python

AUTHOR = "The Tester"
SITENAME = "Testing site"
SITEURL = "http://example.com/test"

# to make the test suite portable
TIMEZONE = "UTC"
PATH = "content"

READERS = {"html": None}

# Generate only one feed
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Disable unnecessary pages
CATEGORY_SAVE_AS = ""
TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
TAGS_SAVE_AS = ""

PLUGIN_PATHS = ["../../"]
PLUGINS = ["liquid_tags.notebook", "liquid_tags.generic"]

NOTEBOOK_DIR = "notebooks"
LIQUID_CONFIGS = (
    ("PATH", ".", "The default path"),
    ("THEME", "", "The theme in use"),
    ("SITENAME", "Default Sitename", "The name of the site"),
    ("AUTHOR", "", "Name of the blog author"),
)
