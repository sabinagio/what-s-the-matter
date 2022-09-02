import re
import string
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
    # Replace double space with single space 
    text = re.sub('\s+', ' ', text) 
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