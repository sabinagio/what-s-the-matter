# What's the matter?

The aim of this project is to collect and analyze Twitter data on an ongoing basis to discover the topics that people have been concerned about in the previous 7 days using the Twitter API recent search end-point.

# Project Outline

## 1. Data Collection

To begin prototyping, we extracted 20,000 tweets from the past 7 days using the following restrictions:

- the tweets are in English (`lang:en`)
- the tweets contain the following keywords:
> fear, fearful, afraid, scared, terrified, worry, worried, anxiety, anxious, distress, concern, dismay, strain,  stress, tension
- the tweets do not contain the following phrases:
> "nothing to fear", "fear not", "don't worry", "no worries"
