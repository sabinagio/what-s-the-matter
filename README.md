# What's the matter?

The aim of this project is to collect and analyze Twitter data on an ongoing basis to discover the topics that people have been concerned about in the previous 7 days using the Twitter API recent search end-point.

# Project Outline

## 1. Data Collection

To begin prototyping, we extracted 20,000 tweets from the past 7 days using the following restrictions:

- the tweets are in English (`lang:en`)
- the tweets contain the following keywords:
> fear, fearful, afraid, scared, terrified, worry, worried, anxiety, anxious, distress, concern, dismay, strain,  stress, tension, terror, alarm, panic, unease, scare, afraid of, careful about
- the tweets do not contain the following phrases:
> "nothing to fear", "fear not", "don't worry", "no worries"

## 2. Data Exploration & Visualization

A deeper dive into the text, tweets, and user data aimed at uncovering:
- the distribution of tweet & user metrics in the extracted data (typically exponential)
- the extent of time captured by the initially extracted data (~30-40 minutes worth of tweets)
- relationships between tweet metrics & user metrics (in progress)
- common words used in the extracted tweets, user names, and user descriptions (to be re-evaluated post-processing)

## 3. Data Preprocessing

Before we create a model to discover the topics people have been fearful about, we need to preprocess the data. The typical steps include:
- Converting text to lowercase
- Removing stopwords, punctuation, URLs, retweet mark (`RTs`), and username handles (`@user`)
- Spelling correction
- Tokenizing strings

In addition to the previous steps, we will perform combinations of the transformations below and see how each choice affects our models:
- Removing emojis / Translating the emoji meaning into a word (to help the model with fear sentiment analysis)
- Performing stemming / lemmatization

## 4. Feature engineering

To perform further analysis of our dataset, we will also add the following features:
- word, character, and special characters count before preprocessing
- word, character, and keyword count postprocessing
