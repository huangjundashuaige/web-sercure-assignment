#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math


# In[2]:


s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]


# In[3]:


T = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]


# In[8]:


IV = [0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476]


# In[65]:


indexs_function_per_interation = [lambda k:k,lambda k:(1+5*k)%16,lambda k:(5+3*k)%16,lambda k:7*k%16]


# In[66]:


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF


# In[67]:



# In[68]:


def F(b,c,d):
    return (b & c) | ((~b) & d)
def G(b,c,d):
    return (b & d) | (c & (~d))
def H(b,c,d):
    return b^c^d
def I(b,c,d):
    return c^(b|(~d))


# In[69]:


g_functions = [F,G,H,I]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




