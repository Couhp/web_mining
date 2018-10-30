import tweepy
from tweepy import OAuthHandler
import pickle
import os
import time 


##### SETUP #########
consumer_key = 'Wy9BjVcCo4NJxO5v2c4O4tr37'
consumer_secret = 'P32XBNwfONdKp0qMjBh4tUC3ZYpgE7lEoPOlTxzqwXQYW9Nvzq'
access_token = '977171798025318400-x7Qhn8CAkzBK9HqsEmhgrTF348rhApn'
access_secret = 'T6RZ10K7jnI2blFNg5SiTCOcb6mX9pr5zbtAh6cijkPJC'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

### ===========================================================

#####  CRAWLER  #################

## STEP 1 => Get all user in Net


__users = {}
__queue = []
__user_in_net = set()
__all_user = set()

if os.path.exists('network_dict.dict') : 
    with open('network_dict.dict', 'rb') as handle:
        __users = pickle.load(handle)

if os.path.exists('users.txt') :
    __queue = [x.rstrip() for x in open('users.txt', 'r').readlines()] 

for user in __users :
    __user_in_net = __user_in_net.union(__users[user])


def network_size () :
    global __user_in_net 
    return len(__user_in_net)
    

def get_original_tweeter (tweet) :
    if 'RT @' in tweet.text[:4] :
        id = ''
        flag = False
        for char in tweet.text :
            if char == ':' : break
            if flag : id += char
            if char == '@' : flag = True
        return id
    return ''


def add_user (user, retweeter) :
    global __users, __counter 
    if user not in __users :
        __users[user] = set()
    __users[user].add(retweeter)
    
    __user_in_net.add(user)
    __user_in_net.add(retweeter)
    return  


def save_net () :
    global __users
    with open('network_dict.dict', 'wb') as handle:
        pickle.dump(__users, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return 


def save_current_user () :
    global __queue
    users = '\n'.join([str(x) for x in __queue])
    with open("users.txt", 'w') as fout :
        fout.write(users)
    return 

def save() :
    save_current_user()
    save_net()

def save_content (user, tweet) :
    content = tweet.text
    file_path = 'content/' + str(user)
    if os.path.exists(file_path):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(file_path, append_write)  as fout :
        fout.write(content)
    return



def main() :
    global __queue, __users, __counter, __all_user
    ROOT_USERS = ['elonmusk','AndrewYNg']
    MAX = 5000

    if __queue == [] :
        __queue = ROOT_USERS
    __all_user = set(__queue)

    while (True) :
        if len(__queue) == 0 : break
        current = __queue.pop(0)

        # for tweet in api.user_timeline(current):
        try :
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=current).items(100):
                save_content (current, tweet)
                original_tweeter = get_original_tweeter(tweet)
                if original_tweeter != '' : 
                    if original_tweeter not in __all_user :
                        __queue.append(original_tweeter)
                    
                    __all_user.add(original_tweeter)
                    add_user(current, original_tweeter)
                
            save()
        except :
            pass
        if network_size() > MAX : break
        print ("Number user in Net :", network_size(), '\nNumber waiting:', len(__queue))

        time.sleep(100)
        


## RUN ####
#
main()
        
             


         
    


