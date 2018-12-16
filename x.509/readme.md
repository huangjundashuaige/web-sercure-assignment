# web 安全第三次作业 x.509解析


## x.509介绍

首先整个证书起到的作用就是解决发布公钥时存在的漏洞，也就是可能会被修改或者说有人伪造的问题，所以通过一个ca来发放保证真实性并且通过签名的手段保证不被修改就是证书整个的构成。
## x.509结构介绍
首先要说明的是这一次的实验因为关于证书的具体结构和是以什么样的语法所写的并没有详细的介绍，所以我所参考的主要还是网上的博客已经现成的代码这样才知道了究竟应该怎么去解析一个证书，参考的代码是用c所写的，我所做的很大程度上只是把c语言的代码给翻译成了python的



以下是参考的博客还有wiki：

[c语言代码](https://www.cnblogs.com/jiu0821/p/4598352.html)
[语法介绍](https://blog.csdn.net/xy010902100449/article/details/52145009)

[wiki](https://en.wikipedia.org/wiki/X.509)

## 如何解析
首先要了解的就是整个二进制的证书的形式是符合asn语法的，所谓的asn语法其实就是所谓的 type-length-value结构，所谓type就是事先确定好的标识符，只需要读入并且判断都能够知道这一个所值的是什么样的类型。

length的作用就是能够指明之后的value应该是多长的，其中length还分成两种，一种是短类型一个byte就能够取完，另一种是长类型，需要短类型超过0x80的部分的指示来继续读入byte来最终确定长度应该是多少。

value就没什么好说的了就是对应类型的值，可以是预先定义的也可以是直接可以读取的，由定义的类型来确定。

因为整个证书都是由这些tlv格式的数据所组成的，所以只需要一直重复地进行读入的操作就能够顺利的解析整个证书。
## 代码分析
```
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
places = {
    "2.5.4.6" : "Country: ",
    "2.5.4.8" : "Sate or province name: ",
    "2.5.4.7" : "Locality: ",
    "2.5.4.10" : "Organization name: ",
    "2.5.4.11" : "Organizational Unit name: ",
    "2.5.4.3" : "Common Name: "
}
```
首先我还是把所有预先设定好的参数全部都放在这一个params的文件里面当做库文件，其中都是用dict来存储，其中每一个odi就是key，而对应的类型就是value。

```
if __name__ == "__main__":
    #global rest_file 
    rest_file = open(sys.argv[1],"rb")
    while True:
        single_op_type()
```
其中主函数就是这一些，主要就是通过输入的参数确定下来需要解析的证书，然后再不断调用解析一个tlv格式的函数不断解析，最后得到整个证书的解析。

```
def single_op_type():
    global _str
    global _tag
    global _extension
    global _tag
    global _type
    #_type = None
    if _tag==False:
        _str = rest_file.read(1)
        if len(_str) ==0:
            print("end")
            exit(0) # stop the program
        if len(_str) > 0:
            _type = ord(_str)
    else:
```
然后就是通过读入文件来判断类型的函数，通过读入数据然后判断类型，与此同时得到长度，最后可以按照长度读入对应的value，最后就可以解析出来。

```
def check_for_legit_length(_length):
    legit_length = 0
    if _length>0x80:
        _length-=0x80
        for i in range(0,_length):
            legit_length*=256
            legit_length+=ord(rest_file.read(1))

    else:
        legit_length = _length
    return legit_length
```
以上是判断所读入了一个byte，然后需要判断是属于短类型还是长类型，如果是长类型就继续读入多出来的判断长度所需要的byte。

```
def handle_printable_string():
    global _str
    _str = ""
    _len = ord(rest_file.read(1))
    legit_length = check_for_legit_length(_len)
    for x in range(legit_length):
        _str += str(rest_file.read(1))[2:-1]
    return _str

def handle_null():
    global _str
    rest_file.read(1)

def handle_time():
    global _str
    _str = ""
    _len = ord(rest_file.read(1))
    legit_length = check_for_legit_length(_len)
    for x in range(legit_length):
        _str += str(r
    ...
```
然后是根据所读入的类型，来进行不同处理的函数

```
def show_result(_str):
    global count
    global bit_count
    global null_count
    global object_count
    global time_count
    global follow_object
    global print_count
    if _type == 2:
        #only consider the normal case
        if count >= len(x509params.ints):
            print(_str)
            return
        if count == 0:
            _str = x509params.versions[_str]
        print(x509params.ints[count],_str)
        count+=1
    elif _type==3:
    ...
```
这是根据不同的类型所输出不同的字符串。

## 实验截图

需要说明的是这里使用的是从专门一个提供证书标准例子的网站上得到的所以很标准。

这一次用来测试的是一个网站的root ca，也就是说issuer和subject是同一个。

```
huangjundashuaige@mister-mofia:~/workstation/github.com/web-sercure-assignment/x.509$ python x509.py ./frank4dd-cacert.der
VERSION:  V3
SERIAL NUMBER:  0c6c749bc225ba0
SIGNATURE ALGORITHM:  sha1RSA
ISSUER:
JP
Tokyo
Chuo-ku
Frank4DD
WebCert Support
Frank4DD Web CA
not before:  071207102146Z
not before:  171204102146Z
SUBJECT:
JP
Tokyo
Chuo-ku
Frank4DD
WebCert Support
Frank4DD Web CA
SUBJECT PUBLIC KEY:
    Algorithm:  RSA
    args:  None
    Subject Public Key:
    0030818902818100bbafbc8f25d5e60cbdbff8bda2a20c50acb30bfb5d04c0063d9494421c63ea489f227fbb5eaa75e016be8c004882c1370bbe4e21d54c4bac35e6c68a1e80d835cf1fce3836dc73ef927c508699f9708ffc232e9611c0f82ec7bfd0220ad4ab3b23d87b5d44577e58f543e003ad63d827c6335716955ed739a0026fd414b74c7b0203010001
Certificate Signature Algorithm: :  sha1RSA
    args:  None
Certificate Signature:
    00ba2c2e91ddb85398df4c0a4b6590df64734608746563652d7587910626cd31cda24c182f2d3019f22acc3d68bcb3230ee3cc0b73019903e0f3385df81636b2046181d1019985938b0ef57992cb988fde7506eed73eab39725bf047a0b9b24d9184dcbb1b0a2e28c87c90e72b69e8a8fb74de9b8912c071a2c375e173c484810e
```

可以看到其中有证书的version还有issuer和subject的具体信息，因为这是一个root ca，所以两个东西是一样的，还有有效期被表示在not before，not after中。

然后就是整个public key还有ca所给出的signature。

