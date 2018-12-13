#!/usr/bin/env python
# coding: utf-8

# In[1]:


ALGORITHM = {
    '1.2.840.10040.4.1': 'DSA',
    "1.2.840.10040.4.3" : "sha1DSA",
    "1.2.840.113549.1.1.1" :"RSA",
    "1.2.840.113549.1.1.2" : "md2RSA",
    "1.2.840.113549.1.1.3" : "md4RSA",
    "1.2.840.113549.1.1.4" : "md5RSA",
    "1.2.840.113549.1.1.5" : "sha1RSA",
    '1.3.14.3.2.29': 'sha1RSA',
    '1.2.840.113549.1.1.13': 'sha512RSA',
     '1.2.840.113549.1.1.11':'sha256RSA'
}
RDN = {
    "2.5.4.6" : "Country: ",
    "2.5.4.8" : "Sate or province name: ",
    "2.5.4.7" : "Locality: ",
    "2.5.4.10" : "Organization name: ",
    "2.5.4.11" : "Organizational Unit name: ",
    "2.5.4.3" : "Common Name: "
}
TYPE = {
    1:'BOOL',
    2:'INT',
    3:'Bit String',
    4:'Byte String',
    5:'NULL',
    6:'Object',
    0x13:'Printable String',
    0x17:'Time',
    0x18:'Time',
    0x30:'Constructor',
    0x31:'Constructor'
}

INTEGEER = {
    0: 'VERSION: ',
    1: 'default version: ',
    2: 'SERIAL NUMBER: ',
    3: '    args needed in SIGNATURE ALGORITHM: ',
    4: '    args needed in CERTIFICATE ALGORITHM: '
}

BITSTRING = {
    0: '    Subject Public Key: \n   ',
    1: 'Certificate Signature: \n   '
}

PRINTABLE = {
    0: 'PRINTABLE: ',
    1: 'PRINTABLE version: ',
    2: 'PRINTABLE NUMBER: '
}

OBJECT = {
    0:'SIGNATURE ALGORITHM: ',
    1:'ISSUER: ',
    2:'SUBJECT: ',
    3:'SUBJECT PUBLIC KEY INFO: \n    Algorithm: ',
    4:'Certificate Signature Algorithm: : '
}

NULL = {
    0: '    args needed in SIGNATURE ALGORITHM: ',
    1: '    args needed in PUBLIC KEY ALGORITHM: ',
    2: '    args needed in CERTIFICATE ALGORITHM: '
}

TIME = {
    0: '    not before: ',
    1: '    not after: '
}


VERSION = {
    '0': 'V1',
    '1': 'V2',
    "2": 'V3'
}


# In[ ]:




