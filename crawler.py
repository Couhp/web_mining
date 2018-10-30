import tweepy
from tweepy import OAuthHandler
 
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

def get_original_user (tweet) :
    if 'RT' in tweet.text :
        return str(tweet.entities['media'][0]['source_user_id_str'])
    return 'null'

def save_list_user (list_user) :
    list_user = [str(x) for x in list(list_user)]
    list_user = '\n'.join(list_user)
    
    with open('users', 'w') as fout :
        fout.write(list_user)
    return






def make_net (list_start_id, max_count=1800) :
    def get_new_user (set_users, max_count = 1000) :
        print ("new users : ", len(set_users))
        list_users = list(set_users)
        new_users = set() 
        for index in range(len(list_users)) :
            print (len(new_users))
            id = list_users[index]
            for tweet in api.user_timeline(id)[:10]:
                if tweet.retweeted :
                    new_users.add(get_original_user(tweet))
                else :
                    retweeters = set(api.retweeters(tweet._json["id"])) #.difference(set_users)
                    new_users = retweeters.union(new_users)
                    # print (len(new_users))
            if len(new_users) > max_count :
                return new_users
        return new_users
        
    set_users_id = set(list_start_id)
    temp = set()
    while True :``
        new_user = get_new_user(set_users_id, max_count-len(set_users_id))

        if len(new_user.difference(set_users_id)) < 5 :
            return set_users_id
        else :
            set_users_id = set_users_id.union(new_user)
            temp = new_user
            if len(set_users_id) > max_count :
                return set_users_id

        
        

# start_users_id = ['977919622153490432','798929315241070592','791464251894460416','964680905481687043','1034250241875365888','1046401883835961349','750432691749789696','999889547549790208','717042249624854529','1027382800062799875','928682743898214402','1002104261553995778','999632398525530114']

# list_users_id = make_net(start_users_id)

# save_list_user(list_users_id)

