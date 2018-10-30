
# coding: utf-8

# In[1]:


import desParams
from functools import reduce
init_test_key = "12345678" #key of char in one byte
def str2bin(s):
    result = ""
    for i in range(0,len(s)):
        k = ord(s[i])
        str1 = bin(k)
        #print(str1[2:len(str1)])
        j = len(str1)
        str2 = str1[2:j]
        #result = result + str2.zfill(8)
        result = result + str2.zfill(7) + "0"
    return(result)
def bin2str(b):
    result = ""
    for i in range(len(b)//8):
        #print(b[i:i+7])
        result += chr(int(b[i*8:i*8+7],2))
    return result


# In[2]:


#bin2str(str2bin(init_test_key))


# In[3]:


# input (string in binary),(p table)
# output (string in binary after transformation)
def P_transform(s,table):
    return reduce(lambda x,y:x+y,[s[table[index]-1] for index in range(len(table))]) # index inside
# the table start with 1 instead of 0 as usual


# In[4]:


def left_circle(key,position):
    result = ""
    for j in range(0,len(key)):
        #print(key[(j+position)%len(key)])
        result = result + key[(j+position)%len(key)]
    return result


# In[61]:


def makeSubKeys(key):
    subKeys = []
    #key = reduce(lambda x,y:x+y,[key[x*8:x*8+7] for x in range(8)])
    #print(len(key))
    #print(len(desParams.PC1))
    CD0 = P_transform(key,desParams.PC1)
    #print(CD0)
    #key = moveTheKey(key,BitsRotated,i+1)
    #key_PC2 = doPermutation(key,PermutationChoose2,48)
    #Keys.append(key_PC2)
    for x in range(16):
        CD0 =  left_circle(CD0[:len(CD0)//2],desParams.left_circle_positions[x]) +                left_circle(CD0[len(CD0)//2:],desParams.left_circle_positions[x]) 
        subKeys.append(P_transform(CD0,desParams.PC2))
    return subKeys


# In[63]:


def exclusive_or(a,b):
    result = ""
    for i in range(0,len(a)):
        a1 = int(a[i])
        b1 = int(b[i])
        r1 = a1 ^ b1
        result =result + str(r1)
    return(result)
def single_sbox_transform(sbox_num,text):
    row = int(text[0])*2 + int(text[5])
    col = int(text[1])*8 + int(text[2])*4 + int(text[3])*2 + int(text[4])
    num = desParams.sbox[sbox_num][row*16+col]
    result = bin(num)
    return result[2:].zfill(4)
def all_sbox_transform(text):
    return reduce(lambda x,y:x+y,[single_sbox_transform(x,text[x*6:(x+1)*6]) for x in range(8)])


# In[86]:


def wheel_function(text,key):
    text_l = text[0:32]
    text_r = text[32:64]
    result_text_l = text_r
    #print(text_l)
    textAfterExpansion = P_transform(text_r,desParams.E)
    textAfterExclusiveOr = exclusive_or(textAfterExpansion,key)
    textAfterSboxPermutation = all_sbox_transform(textAfterExclusiveOr)
    textAfterPermutation = P_transform(textAfterSboxPermutation                                         ,desParams.P_after_circle_transformation)
    result_text_r = exclusive_or(text_l,textAfterPermutation)
    result = result_text_l + result_text_r
    return result
def iterations(text,sub_keys):
    res = text
    for x in range(16):
        res = wheel_function(res,sub_keys[x])
    return res
def reverse_iterations(text,sub_keys):
    res = text
    for x in range(16):
        res = wheel_function(res,sub_keys[15-x])
    return res


# In[110]:


def single_encrypt(text,sub_keys):
    text = P_transform(text,desParams.IP)
    text = iterations(text,sub_keys)
    text = text[len(text)//2:] + text[:len(text)//2]
    text = P_transform(text,desParams.IP_1)
    return text


# In[112]:


def single_decrypt(text,sub_keys):
    text = P_transform(text,desParams.IP)
    text = reverse_iterations(text,sub_keys)
    text = text[len(text)//2:] + text[:len(text)//2]
    text = P_transform(text,desParams.IP_1)
    return text


# In[140]:


def encrypt(all_text,key):
    key = str2bin(key)
    if len(all_text) % 8 ==0:
        all_text += "00000000"
    else:
        plus_chr = chr(8-len(all_text)%8+48)
        for x in range(8-len(all_text)%8):
            all_text += plus_chr
    all_text = str2bin(all_text)
    sub_keys = makeSubKeys(key)
    res = ""
    for x in range(len(all_text)//64):
        res += single_encrypt(all_text[x*64:(x+1)*64],sub_keys)
    return res
def decrypt(all_bin_text,key):
    key = str2bin(key)
    sub_keys = makeSubKeys(key)
    res = ""
    for x in range(len(all_bin_text)//64):
        res += single_decrypt(all_bin_text[x*64:(x+1)*64],sub_keys)
    res = bin2str(res)
    last_chr = res[-1]
    #print(res[-1])
    if last_chr <= "7" and last_chr > "0":
        #print(res[-1])
        res = res[:-int(res[-1])]
    elif last_chr == '0':
        res = res[:-8]
    return res


# In[144]:


if __name__ == "__main__":
    text  = input("key in the text you want to encrypt")
    key = input("key in the 8byte cipher key")
    cipher = encrypt(text,key[:8])
    print("cipher is:{}".format(cipher))
    flag = input("do you want to decrypt the cipher to make sure its woring y/n")
    if flag =="y":
        print("decrypt cipher:{}".format(decrypt(cipher,key[:8])))

