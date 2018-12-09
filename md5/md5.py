#!/usr/bin/env python
# coding: utf-8

# In[145]:


from functools import reduce
import md5_params


# In[149]:


def H_md5(a,b,c,d,message_part):
    #print(1)
    for i in range(4):
        for j in range(16):
            g_b_c_d = md5_params.g_functions[i](b,c,d)
            X_k = int.from_bytes(message_part[4*md5_params.indexs_function_per_interation[i](j):4*md5_params.indexs_function_per_interation[i](j)+4],byteorder="little")
            temp1 = a + g_b_c_d + X_k + md5_params.T[i*16+j]
            temp2 = b + md5_params.left_rotate(temp1,md5_params.s[i*16+j])
            a , b , c , d = d , temp2 & 0xFFFFFFFF , b ,c
    return a , b ,c ,d


# In[150]:


def md5(message):
    
    message = bytearray(message,encoding="utf-8")
    if len(message) < 8:
        lack_length = 8-len(message)
        remaind_padding = bytearray("0",encoding="utf-8")
        for i in range(8-1-len(message)):
            remaind_padding.append(0x00)
        remaind_padding+=message[-lack_length:]
    else:
        remaind_padding=message[-8:]
    #print(remaind_padding)
    if 8*len(message) == 448:
        message.append(0x80)
        for i in range(63):
            message.append(0x00)
    else:
        message.append(0x80)
        while len(message) % 64 !=56:
            #print(len(message))
            message.append(0x00)
    message+=remaind_padding
    a,b,c,d = md5_params.IV
    #print(len(message))
    for x in range(len(message)//64):
        a,b,c,d = H_md5(a,b,c,d,message[x*64:x*64+64])
    #print(len(a))
    return reduce(lambda x,y:x+y,map(lambda x : (x&0xFFFFFFFF).to_bytes(4,byteorder="little"),[a,b,c,d]))


# In[ ]:





# In[152]:


if __name__ == "__main__":
    text = input("inout the text you want digest")
    print("the byte format output is {}".format(md5(text)))
    print("the bytearray format output is {}".format('{:032x}'.format(int.from_bytes(md5(text),byteorder="little"))))


# In[ ]:




