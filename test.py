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

# id = 'iamcouhp'

# def get_original_user (tweet) :
#     if 'RT @' in tweet.text[:4] :
#         id = ''
#         flag = False
#         for char in tweet.text :
#             if char == ':' : break
#             if flag : id += char
#             if char == '@' : flag = True
            
            
#         return id
#     return ''

# for tweet in tweepy.Cursor(api.user_timeline, id=id).items(2) :
#     # print (tweet._json, file=open("test.txt", 'a'))
#     print (get_original_user(tweet))
#     # print (tweet._json['quoted_status'])
    
# import pickle
# import sys 

# replies=[] 
# non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  
# name = 'taylorswift13'

# for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=name,timeout=999999).items(2):
#   for tweet in tweepy.Cursor(api.search,q='to:'+name,result_type='recent',timeout=999999).items(1000):
#     if hasattr(tweet, 'in_reply_to_status_id_str'):
#       if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
#         replies.append(tweet.text)
#   print("Tweet :",full_tweets.text.translate(non_bmp_map))
#   for elements in replies:
#        print("Replies :",elements)
#   replies.clear()

with open("network.gexf", 'w') as fout :
  data = ''
  for i in range(14261) :
    data += '<node id=\"' + str(i) + '\" />\n'
  
  edges = [x.rstrip() for x in open('network_connection.txt', 'r').readlines()]
  counter = 0
  for edge in edges :
    a,b = edge.split(' ')
    data += '<edge id="' + str(counter) + '" source="' + str(a) + '" target="' + str(b) + '" />\n'
    counter += 1
  fout.write(data)

    
