import x509params
import sys
_str = ""
count = 0
bit_count = 0 
null_count = 0
object_count = 0
time_count = 0
follow_object = 0
rest_file = None
print_count = 0
follow_object = False
_type = None
_tag = False
_extension = False
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
        _str += str(rest_file.read(1))[2:-1]
    return _str

def handle_int():
    global _str
    _str = ""
    global rest_file
    length = ord(rest_file.read(1))
    legit_length = check_for_legit_length(length)
    for x in range(0,legit_length):
        _str += hex(ord(rest_file.read(1)))[2:]
    return _str

def handle_bit_stringt():
    global _str
    _str = ""
    _len = ord(rest_file.read(1))
    legit_length = check_for_legit_length(_len)
    for x in range(legit_length):
        _temp = hex(ord(rest_file.read(1)))[2:]
        if len(_temp) !=2:
            _temp = "0" + _temp
        _str += _temp
    return _str

def handle_tag():
    global _str
    global _file
    _len = ord(rest_file.read(1))
    if _len > 0x80:
        legit_length = check_for_legit_length(_len)
    single_op_type()

def handle_constructor():
    global _str
    _len = ord(rest_file.read(1))
    legit_length = check_for_legit_length(_len)
    [single_op_type() for x in range(legit_length)]

def handle_object():
    global _str
    _str = ""
    _len = ord(rest_file.read(1))
    legit_length = check_for_legit_length(_len)
    first_byte = ord(rest_file.read(1))
    v1 = int(first_byte)
    v2 = first_byte - v1*40
    _str += str(int(v1)) + " "
    _str += str(int(v2))
    i = 0
    vn = 0
    while i < legit_length -1:
        _byte = ord(rest_file.read(1))
        while _byte & 0x80 !=0:
            _byte &= 0x7f
            i+=1
            vn *= 128
            vn+=_byte
            byte = ord(rest_file.read(1))
        vn *= 128
        vn += _byte
        _str += "."+str(int(vn))
        vn = 0
        i+=1
    return _str
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
        if count >= len(x509params.INTEGEER):
            print(_str)
            return
        if count == 0:
            _str = x509params.VERSION[_str]
        print(x509params.INTEGEER[count],_str)
        count+=1
    elif _type==3:
        if bit_count >= len(x509params.BITSTRING):
            print(_str)
            return
        print(x509params.BITSTRING[bit_count],_str)
        bit_count+=1
    elif _type ==5:
        if null_count >= len(x509params.NULL):
            return
        print(x509params.NULL[null_count],"None")
        null_count+=1
        count+=1
    elif _type == 6:
        if object_count >= len(x509params.OBJECT):
            if x509params.RDN.get(_str,-1)!= -1:
                _str = x509params.RDN[_str]
            elif x509params.ALGORITHM.get(_str,-1)!=-1:
                _str = x509params.ALGORITHM[_str]
            print(_str)
            return
        if x509params.RDN.get(_str,-1)!=-1:
            _str = x509params.RDN[_str]
            if _str == "Country: ":
                print(x509params.OBJECT[object_count])
                object_count+=1
            follow_object = True
            print(_str)
        elif x509params.ALGORITHM.get(_str,-1)!=-1:
            _str = x509params.ALGORITHM[_str]
            print(x509params.OBJECT[object_count],_str)
            object_count+=1
    elif _type == 0x17 or _type == 0x18:
        if time_count == -1:
            print("VALIDITY:")
            time_count +=1
            print(x509params.TIME[time_count],_str)
            time_count+=1
        else:
            print(x509params.TIME[time_count],_str)
            #time_count+=1
    elif _type == 0x13 or _type == 0x0c:
        if follow_object == False:
            print(_str)
            print_count +=1
            #if print_count ==3:
            #    print_count =2
            #print_count %= 3
        else:
            follow_object = False
            print(_str)
    #elif _type==0x13 or _type==0x0c:
    #    if follow_object == False:
    #        print()
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
        _tag=False
    if _type < 0x80:
        if _type == 1:
            pass # bool
        elif _type == 2:
            handle_int()
        elif _type ==3:
            if _extension ==True:
                handle_printable_string()
            else:
                handle_bit_stringt()
        elif _type ==4:
            pass # byte
        elif _type ==5:
            handle_null()
        elif _type==6:
            handle_object()
        elif _type==0x13 or _type ==0x0c:
            #pass
            handle_printable_string()
        elif _type==0x17 or _type==0x18:
            handle_time()
        elif _type==0x30 or _type==0x31:
            handle_constructor()
        elif _type ==0:
            handle_tag()
        show_result(_str)
    elif _type >= 0xa0:
        # explicit type
        _tag = _type - 0xa0
        if _tag == 0:
            count = 0
        elif _tag ==3:
            _extention = True
        _type = _tag
        _tag = True
        single_op_type()
    else:
        _tag = _type - 0x80
        _type = _tag
        single_op_type()
                

if __name__ == "__main__":
    #global rest_file 
    rest_file = open(sys.argv[1],"rb")
    while True:
        single_op_type()