#!/usr/bin/env python
# coding: utf-8

# # Systems Recruitment Task - Cryptography
# 
# ## Given text is:
# - d3ZucXN0b2tib2xlamp5ZW5zdnlicGpsa3VhcGx2 
# - b2dzd2xmcndwb2JmY2J4dmdtZGZseGp1dnZuaGZ0amFiZ2M=
# - YW9sdWxlYXJsZnB6anlmd2F2bnlod29m
# - aGZyZ3VyeHJsZ2pyYWds
# - Z3JlYXRzdGFydA==
# 

# #### Looking at the last line, it seems to be base64 encrypted (due to the padding in the end)

# In[1]:


import base64


# In[2]:


cypher_text = ["d3ZucXN0b2tib2xlamp5ZW5zdnlicGpsa3VhcGx2", 
               "b2dzd2xmcndwb2JmY2J4dmdtZGZseGp1dnZuaGZ0amFiZ2M=",
               "YW9sdWxlYXJsZnB6anlmd2F2bnlod29m",
               "aGZyZ3VyeHJsZ2pyYWds",
               "Z3JlYXRzdGFydA=="]


# ### Decrypting base64 encryption using base64 module

# In[3]:


##e5 is base64 encryption
for i in range(5):
    temp = cypher_text[i].encode('ascii')
    temp = base64.b64decode(temp)
    cypher_text[i]  = temp.decode("ascii")
cypher_text
    


# #### The encryption was base64 after all, as we supposedly off to a "great start".
# 
# #### e4 seems to be a Caesar cipher with offset 13

# In[4]:


#creating dictionaries to retrieve alphabets
dict1 = {}
dict2 = {}
alphabet = 'abcdefghijklmnopqrstuvwxyz'
for i in range(26):
    dict1[i+1] = alphabet[i]
    dict2[alphabet[i]] = i+1


# In[5]:


#function to decode rot13
def caesar(message, offset):
    decrypted = ''
    for i in message:
        num = dict2[i] - offset
        if num <= 0:
            num+=26
        decrypted += dict1[num]
    return decrypted


# In[6]:


for i in range(4):
    temp = caesar(cypher_text[i], 13)
    cypher_text[i] = temp


# In[7]:


cypher_text


# #### e4 indeed is a Caesar cipher
# 
# #### e3, from the hints and given logic, is again a Caesar cipher, but with offset 20

# In[9]:


for i in range(3):
    temp = caesar(cypher_text[i], 20)
    cypher_text[i] = temp
cypher_text


# #### Looking at the hint given, e2 seems to be a substitution cipher. From the given logic, it seems that e2 is a Vigenere cipher

# In[10]:


def vignere_decode(message, key):
    key_len = len(key)
    msg_len = len(message)
    decrypted = ''
    for i in range(msg_len):
        num = (dict2[message[i]] - dict2[key[i%key_len]] + 26) % 26
        decrypted += dict1[num+1]
    return decrypted


# In[11]:


vignere_key = 'cryptography'
for i in range(2):
    cypher_text[i] = vignere_decode(cypher_text[i], vignere_key)
cypher_text


# #### e2 is indeed a Vigenere cipher. 
# 
# #### Looking at e1, it again seems to be a substitution cipher. 

# In[12]:


key = 'natdszgrqhebvpmxilfywcuko'
print(len(key))


# ### The number of letters in the key is 25, and is missing a 'j' as well. This is usually a characteristic of a Playfair cipher, where we use a 5x5 matrix, with each element being one of the English alphabets (excluding 'j')

# In[13]:


def playfair_init(key):
    playfair_sq = {}
    playfair_retrieve = {}
    k=0
    i=0
    j=0
    alphabet = 'abcdefghiklmnopqrstuvwxyz'
    bool_alph = {}
    for ch in alphabet:
        bool_alph[ch] = False
    while k < len(key):
        if bool_alph[key[k]] == False:
            playfair_sq[key[k]] = (k//5,k%5)
            playfair_retrieve[(k//5,k%5)] = key[k]
            bool_alph[key[k]] = True
        k+=1    
    for ch, bool_val in bool_alph.items():
            if bool_val == False:
                playfair_sq[ch] = (k//5, k%5)
                playfair_retrieve[(k//5, k%5)] = ch
                k+=1
        
    return playfair_sq, playfair_retrieve


# In[14]:


playfair_sq, playfair_retrieve = playfair_init(key)


# In[15]:


def playfair_decode(message, square, retrieve):
    msg_split = []
    i = 0
    if len(message)%2: message+='x'
    while i < len(message):
        temp = ''
        if message[i] == message[i+1]:
            temp += (message[i]+'x')
        else:
            temp += (message[i]+message[i+1])
        i+=2
        msg_split.append(temp)
    result = ''
    for pair in msg_split:
        if square[pair[0]][0] == square[pair[1]][0]:
            result += retrieve[(square[pair[0]][0], (square[pair[0]][1]+4)%5)]
            result += retrieve[(square[pair[0]][0], (square[pair[1]][1]+4)%5)]
        elif square[pair[0]][1] == square[pair[1]][1]:
            result += retrieve[((square[pair[0]][0]+4)%5), square[pair[0]][1]]
            result += retrieve[((square[pair[1]][0]+4)%5), square[pair[0]][1]]
        else:
            result += retrieve[(square[pair[0]][0], square[pair[1]][1])]
            result += retrieve[(square[pair[1]][0], square[pair[0]][1])]
    return result


# In[18]:


cypher_text[0] = playfair_decode('nxiusybmusxzaltinxiautvgbwvtla', playfair_sq, playfair_retrieve)


# In[19]:


print(cypher_text)


# ### The message has been decoded. 
# 
# ### Summary of encryption algorithms used here:
# - e1: Playfair cipher
# - e2: Vigenere cipher
# - e3: Caesar cipher (offset 20)
# - e4: Caesar cipher (offset 13)
# - e5: Base64 encrpytion

# In[ ]:




