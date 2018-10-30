import pandas as pd 
import tweepy
from tweepy import OAuthHandler
import os

##### SETUP #########
consumer_key = 'Wy9BjVcCo4NJxO5v2c4O4tr37'
consumer_secret = 'P32XBNwfONdKp0qMjBh4tUC3ZYpgE7lEoPOlTxzqwXQYW9Nvzq'
access_token = '977171798025318400-x7Qhn8CAkzBK9HqsEmhgrTF348rhApn'
access_secret = 'T6RZ10K7jnI2blFNg5SiTCOcb6mX9pr5zbtAh6cijkPJC'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

## load community 
df = pd.read_csv('community.csv')
users = df['Label']

### ===========================================================

def save_content (user, tweet) :
    content = tweet.text
    file_path = 'content/' + str(user)[1:]
    if os.path.exists(file_path):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(file_path, append_write)  as fout :
        fout.write(content)
    return

def check_content(user) :
    file_path = 'content/' + str(user)[1:]
    if not os.path.exists(file_path) :
        return False
    lines = len(open(file_path).read())
    print (lines)
    if lines < 10000 :
        return True
    else :
        return False


for user in users :
    print (user)    
    if check_content(user) :
        print ('hihi')
        continue
    try :
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items(100):   
            save_content (user, tweet)
    except :
        pass
    