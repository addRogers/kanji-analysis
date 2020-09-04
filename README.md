# kanji-analysis

This repo is a simple project to look at personal review data for WaniKani over time.

## Motivation

To find interesting relationships in personal review metrics (e.g. percent correct or streaks), or between / among
different subjects, present in the WaniKani app ([found here](https://www.wanikani.com/)). 
WaniKani is a kanji/vocabulary learning system for Japanese characters and words that relies on an Spaced Repetition 
System (SRS) method of review - radicals, kanji or words are introduced then reviewed flashcard style in a spaced 
manner to promote long term retention in memory. 
 
Along the way, I'll try to visualize relationships in the data and attempt to come up with a model of them.


## Structure

This project uses pipenv to organize itself - all that is required is for pipenv to be installed then 
the required environment can be created from the Pipfile.

The following files can be found in this project:

1. get_data.py: This file is a wrapper for the WaniKani API. Given a token with `--token` from the command line, it will
pull all the relevant data for the associated user and write them to csv files. Note that this isn't meant to be used
continuously or for a bulk of users - this is a one time personal analysis - so request errors are mostly ignored.

2. main.py: This will contain the meat of the code for exploration, analysis, and modeling. It relies on the JetBrains
PyCharm IDE "Scientific" mode, so it likely will not work unless using that IDE environment. Fear not however, because:

3. analysis.ipynb: The results from main.py will live in this notebook at the conclusion of this project.