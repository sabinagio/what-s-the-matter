import re
import numpy as np
import pandas as pd
import string
import emoji
from textblob import TextBlob #spelling correction
import nltk.pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer

# function for text cleaning
def clean_text(text):
    # Remove RT (retweet superfluous text)
    text = text.replace('RT', ' ') 
    # Remove twitter handles, e.g. @username
    text = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)','',text)
    # Convert text to lowercase & remove leading and trailing whitespaces
    text = text.lower().strip() 
    # Removing inside of tags <>
    text = re.compile('<.*?>').sub('', text) 
    # Remove punctuation marks
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text) 
    # Remove URLs
    text = re.compile('https?://S+|www.S+').sub('', text) 
    # Replace numbers by a single space
    text = re.sub(r'\[[0-9]*\]',' ', text)  
    # Get rid of decimal digits   
    text = re.sub(r'\d',' ', text) 
    # Get rid of duplicate whitespaces
    text = re.sub(r'\s+',' ', text) 
    return text

# function for spelling correction
def correct_spelling(text):
    text = str(TextBlob(text))
    return text

# function for removing emojis
def remove_emojis(text):
    no_emo = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F" 
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002500-\U00002BEF"
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
                           "]+", flags = re.UNICODE).sub(r'', text)
    return no_emo

# function for Stop Word removal
def stop(text):
    stop = stopwords.words('english')
    no_stop_words = [word for word in text.split() if word not in stop]
    return ' '.join(no_stop_words)

# function for lemmatization

# getting the tags (word type: verb, noun, adverb etc.)
def get_type(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    elif tag.startswith('DT'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatization(text):
    tokens = word_tokenize(text) #tokenizing
    word_and_tag = nltk.pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(pair[0], pos=get_type(pair[1])) for pair in word_and_tag]
    return ' '.join(lemmatized)

def translate_emojis(df, text_col="text"):

        # Define emoji patterns
        pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F" 
                u"\U0001F300-\U0001F5FF"
                u"\U0001F680-\U0001F6FF"
                u"\U0001F1E0-\U0001F1FF"
                u"\U00002500-\U00002BEF"
                u"\U00002702-\U000027B0"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642" 
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"
                u"\u3030"
                                   "]+", flags = re.UNICODE)

        # Return emojis found and translate each into a Pandas Series
        matches = pd.Series(map(lambda x: pattern.findall(x), df[text_col]))
        matches = matches.apply(lambda x: "".join(x))
        matches = matches.apply(lambda x: emoji.demojize(x))
        matches = matches.apply(lambda x: np.nan if x == "" else x)

        # Append translated emojis to dataframe
        df["emojis"] = matches


def text_features(df, text_col="text", prefix="pre"):
    
    """
    Function to add columns to the dataframe with word count, character count, and
    special characters count pre- and post-processing

    Arguments

    df = the dataframe to add columns to
    text_col = the name of the dataframe column which hosts the text
    step = the prefix for the resulting columns and the moment of the
            transformation. Can only be "pre" or "post". 
    """

    df[prefix.lower() + "_word_count"] = df[text_col].apply(lambda x: len(x.split(" ")))
    df[prefix.lower() + "_char_count"] = df[text_col].apply(lambda x: len(x))

    if prefix.lower() == "pre":
    
        def count_special_chars(text):
            char_no = 0
            for char in text:
                if char.isalnum() == False:
                    char_no += 1
            return char_no

        df[prefix.lower() + "_spec_char_count"] = df[text_col].apply(lambda x: count_special_chars(x))

    elif prefix.lower() == "post":

        keywords = ["fear", "fearful", "afraid", "scared", "terrified", "worry", \
            "worried", "anxiety", "anxious", "distress", "concern", "dismay", "strain",\
            "stress", "tension", "terror", "alarm", "panic", "unease", "scare",\
            "afraid of", "careful about"]

        def count_keywords(text):
            keyw_no = 0
            words = text.split(" ")
            for keyw in words:
                if keyw in keywords:
                    keyw_no += 1
            return keyw_no

        df[prefix.lower() + "_keyword_count"] = df[text_col].apply(lambda x: count_keywords(x))

    else:
        print("The prefix can only be 'post' or 'pre'!")