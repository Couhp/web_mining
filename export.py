import pickle
# import tweepy
# from tweepy import OAuthHandler
import time
 
##### SETUP #########
# consumer_key = 'Wy9BjVcCo4NJxO5v2c4O4tr37'
# consumer_secret = 'P32XBNwfONdKp0qMjBh4tUC3ZYpgE7lEoPOlTxzqwXQYW9Nvzq'
# access_token = '977171798025318400-x7Qhn8CAkzBK9HqsEmhgrTF348rhApn'
# access_secret = 'T6RZ10K7jnI2blFNg5SiTCOcb6mX9pr5zbtAh6cijkPJC'
 
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)
 
# api = tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


### =============    EXPORT  NETWORK 
with open('network_dict.dict', 'rb') as handle:
    network = pickle.load(handle)

selected_set = set()
selected_list = []
for key in network :
    selected_list.append(str(key))
    for val in network[key] :
        # if str(val) in selected_set :
        #     selected_list.append(str(val))
        # else :
        #     selected_set.add(str(val))
        selected_list.append(str(val))

# from random import randint
# for i in list(selected_set) :
#     if randint(0,2) == 1 :
#         selected_list.append(i)
#     if len(selected_list) == 2000 :
#         break

list_node = list(selected_list)
with open('network_node.txt', 'w') as fout :
# with open('network_node_mini.txt', 'w') as fout :
    data = ''
    for i in range(len(list_node)) :
        if len(list_node[i]) > 30 :
            list_node[i] = list_node[i][:10]
        data += str(i) + ' ' + list_node[i] + '\n'
    fout.write(data)


# with open('network_dict', 'rb') as handle:
#     network = pickle.load(handle)

index = {}
for line in open('network_node.txt', 'r').readlines() :
# for line in open('network_node_mini.txt', 'r').readlines() :
    a,b = line.rstrip().split(' ')
    index[b] = a

with open('network_connection.txt', 'w') as fout :
# with open('network_connection_mini.txt', 'w') as fout :
    data = ''
    for key in network :
        for val in network[key] :
            if str(key) in index and str(val) in index :
                data += index[str(key)] + ' ' + index[str(val)] + '\n'
    fout.write(data)



with open("network.gexf", 'w') as fout :
    data = '<?xml version="1.0" encoding="UTF-8"?>\n\
    <gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" version="1.1" xmlns="http://www.gexf.net/1.1draft">\n\
    <meta lastmodifieddate="2010-03-03+23:44">\n\
    <creator>Gephi 0.7</creator>\n\
    </meta>\n\
    \n<graph defaultedgetype="undirected" idtype="string" type="static">\n'
    data += "<nodes count=\"3750\" >\n"

    for line in open('network_node.txt', 'r').readlines() :
        a,b = line.rstrip().split(' ')
        data += '<node id=\"' + str(a) + '\" label=\"@' + str(b) + '\" />\n'
    data += "</nodes>\n"

    edges = [x.rstrip() for x in open('network_connection.txt', 'r').readlines()]
    data += "<edges count=\"" + str(len(edges)) + "\">\n "
    counter = 0
    for edge in edges :
        a,b = edge.split(' ')
        data += '<edge id="' + str(counter) + '" source="' + str(a) + '" target="' + str(b) + '" />\n'
        counter += 1
    data += "</edges>\n</graph>\n</gexf>"
    fout.write(data)


'''
###  ========== EXport list node name

import random
import string

def random_text () :
    digits = "".join( [random.choice(string.digits) for i in range(2)] )
    chars = "".join( [random.choice(string.ascii_letters) for i in range(4)] )
    return digits + chars

data = [x.rstrip() for x in open('network_node_mini.txt', 'r').readlines()]
result = ''
for line in data :
    index, id = line.split(' ')

    try :
        name = api.get_user(id).screen_name
        result += str(index) + ',' + str(name) + '\n'
    except :
        result += str(index) + ',' + str(random_text()) + '\n'

with open('netword_node_mini_byname.txt', 'w') as fout :
    fout.write(result)
'''



# with open('network_node.txt', 'w') as fout :
#     data = ''
#     for i in range(len(list_node)) :
#         data += str(i) + ' ' + list_node[i] + '\n'
#     fout.write(data)

               
