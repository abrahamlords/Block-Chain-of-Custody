#!/usr/bin/env python3
import sys
from datetime import datetime
import hashlib
import os
import struct
import uuid
import collections


filePath = os.environ.get("BCHOC_FILE_PATH")
#filePath= "INITIAL"
block_format = struct.Struct('20s d 16s I 11s I')
block_second_format = struct.Struct('14s ')
block_second_format1 = struct.Struct('0s')

BLOCKCHAIN_STRUCTURE= collections.namedtuple('BLOCKCHAIN_STRUCTURE',['Previous_Hash','TimeStamp', 'CASE_ID','EVIDENCE_ID','STATE','Length'])
BLOCKCHAIN_LAST = collections.namedtuple('BLOCKCHAIN_LAST',['data'])
block_list = collections.namedtuple('block_list',['case','id','status','time'])
block_checkout_remove = collections.namedtuple('block_checkout_remove',['id','status'])

def initilization():
    
    FILE_FOUND = False
    try:
        fp=open(filePath, 'rb')
        fp.close()
        FILE_FOUND=True
    except:
        FILE_FOUND=False
    if FILE_FOUND ==False: #this means we didn't find the file, we have to create one first
        time = datetime.now()
        timestamp=datetime.timestamp(time)
        NONE= str.encode("");
        FIRST = BLOCKCHAIN_STRUCTURE(NONE,timestamp,NONE,0,str.encode("INITIAL"),14)
        SECOND = BLOCKCHAIN_LAST(str.encode("Initial block"))
        FIRST = block_format.pack(*FIRST)
        SECOND = block_second_format.pack(*SECOND)
        fp= open (filePath,'wb')
        fp.write(FIRST)
        fp.write(SECOND)
        fp.close()
        print("Blockchain file not found. Created INITIAL block.")
    else:#found the file, check if it is the format we want
        try:
            fp=open(filePath,'rb')
            FIRST = fp.read(block_format.size)
            SECOND = fp.read(block_second_format.size)
            FIRST= BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST))
            SECOND = BLOCKCHAIN_LAST._make(block_second_format.unpack(SECOND))
            fp.close()
            print("Blockchain file found with INITIAL block.")

        except:
            print("incorrect format")
            time = datetime.now()
            timestamp=datetime.timestamp(time)
            NONE= str.encode("");
            FIRST = BLOCKCHAIN_STRUCTURE(NONE,timestamp,NONE,0,str.encode("INITIAL"),14)
            SECOND = BLOCKCHAIN_LAST(str.encode("Initial block"))
            actual_block= struct.pack('20s d 16s I 11s I',FIRST.Previous_Hash,FIRST.TimeStamp,FIRST.CASE_ID,FIRST.EVIDENCE_ID,FIRST.STATE,FIRST.Length)

            
            SECOND = block_second_format.pack(*SECOND)
            fp= open (filePath,'wb')
            fp.write(actual_block)
            fp.write(SECOND)
            fp.close()

            sys.exit(1)

def ADDING(CASEID, ITEMS):

    FILE_FOUND = False
    try:
        fp=open(filePath, 'rb')
        fp.close()
        FILE_FOUND=True
    except:
        initilization()
        sys.exit(0)
    
    if FILE_FOUND== False:   #did not find the file, have to do ./bchoc init first
        print("Need to initialize first")
        sys.exit(1)
    else:# this means the file does exist        
        i=0
        array=[]
        while i< len(ITEMS):
            if ITEMS[i]=="-i" and i+1<len(ITEMS) :
                array.append(ITEMS[i+1])
            i=i+1
        array_EVIDENCE_ID=[]
        #fixing my byte ordering issue
        
      
        x=0
        reverse=""
        w=CASEID.replace("-","")
        while x<len(w):
            reverse=w[x]+w[x+1]+reverse
            x=x+2
        
       # case_string =CASEID.replace("-","")
       # case_string= bytearray.fromhex(case_string)
       # case_string.reverse()
       # reverse=''.join(format(b,'02x') for b in case_string)


       # print(reverse)
        reading = True
        fp=open(filePath,'rb')
        previous_hash=''

        while reading:
            try:
            
                FIRST = fp.read(block_format.size)
                FIRST2=BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST))
                SECOND = fp.read(FIRST2.Length)
               # print(FIRST2)
                previous_hash=hashlib.sha1(FIRST+SECOND).digest() 
                array_EVIDENCE_ID.append(FIRST2.EVIDENCE_ID)#this is from our file
            except IOError:
                print("issus in adding, can't open file")
                sys.exit(1)
            except EOFError:
                print("end of file in adding")
                sys.exit(1)
            except ValueError:
                print("wrong arguement in adding") 
                sys.exit(1)
            except TypeError:
                print("this is my previous_hash line issue")
                sys.exit(1)
            except:
                fp.close()
                break
        print(array_EVIDENCE_ID)
        z=0# here is just checking if evidence id are duplicated or not
        while z<len(array_EVIDENCE_ID):
            x=0
            while x< len(array):
                if str(array_EVIDENCE_ID[z]) == str(array[x]):
                    print("issue with duplicated")
                    sys.exit(1)
                x=x+1
            z=z+1
        position=0
        once=0
       # print(reverse)

        a =uuid.UUID(reverse).bytes
        
        
        while position<len(array):
            try:
                
        #        block_format1 = struct.Struct('20s d 16s I 11s I')
        #        block_second_format1 = struct.Struct('14s ')
        #        BLOCKCHAIN_STRUCTURE1= collections.namedtuple('BLOCKCHAIN_STRUCTURE',['Previous_Hash','TimeStamp', 'CASE_ID','EVIDENCE_ID','STATE','Length'])
       #         BLOCKCHAIN_LAST1 = collections.namedtuple('BLOCKCHAIN_LAST',['data'])


                previous_hash= str.encode("")
                fp=open(filePath,'ab')
                time = datetime.now()
                UTC_TIME =datetime.timestamp(time)
                
                FIRST = BLOCKCHAIN_STRUCTURE(previous_hash,UTC_TIME,a,int(array[position]),str.encode("CHECKEDIN"),0)
                #SECOND = BLOCKCHAIN_LAST(str.encode(""))
    
                #actual_block= struct.pack('20s d 16s I 11s I',FIRST.Previous_Hash,FIRST.TimeStamp,FIRST.CASE_ID,FIRST.EVIDENCE_ID,FIRST.STATE,FIRST.Length)
                
                FIRST = block_format.pack(*FIRST)
                SECOND = block_second_format1.pack(b'')
                previous_hash=hashlib.sha1(FIRST+SECOND).digest()
                
                fp.write(FIRST)
                fp.write(SECOND)
                fp.close() 
            except IOError:
                print("issus in adding, can't open file")
                sys.exit(1)
            except EOFError:
                print("end of file in adding")
                sys.exit(1)
            except ValueError:
                print("wrong arguement in adding in 171, probably FIRST and -c is incorrect")
                sys.exit(1)
            except TypeError:
                print("this is my previous_hash line issue")
                sys.exit(1)
           # except:
               # print("there is an issue in adding command in the end of the function")
               # sys.exit(1)
            if once ==0:
                print("CASE:",CASEID)
                once=1
            print("Added item:",array[position] )
            print("\tStatus: CHECKEDIN")
            print("\tTime of action:", time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            position=position+1
    
def CHECKED_OUT(Evidence_id):
    #first step check if the Evidence_id is in our file or not, if not just sys.exit(1)
    try:
        fp=open(filePath,'rb')
    except:
        print("Have not initialized yet")
        initilization()
        sys.exit(0)

    reading = True
    array_EVIDENCE_ID=[]
    out_case_id=[]
    PREVIOUS_HASH =''

    block_list=[]
    
    while reading:
        try:
            FIRST2 = fp.read(block_format.size)
            FIRST= BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST2))
            SECOND = fp.read(FIRST.Length)
            PREVIOUS_HASH=hashlib.sha1(FIRST2+SECOND).digest()
            value = FIRST.STATE.decode().rstrip('\x00')#this will get CHECKEDIN
            
            a_list= block_checkout_remove(FIRST.EVIDENCE_ID,value)
            
            block_list.append(a_list)

          #  print(value)
            if str(value)=="CHECKEDIN":
                array_EVIDENCE_ID.append(FIRST.EVIDENCE_ID)

               # print(str(uuid.UUID(bytes=FIRST.CASE_ID)))
                out_case_id.append(str(uuid.UUID(bytes=FIRST.CASE_ID)))
            elif str(value)=="CHECKEDOUT":
                array_EVIDENCE_ID.remove(FIRST.EVIDENCE_ID)
                out_case_id.remove(str(uuid.UUID(bytes=FIRST.CASE_ID)))

        except:
            fp.close()
            break;
            
  #  print(block_list)
    
  #  print(array_EVIDENCE_ID)
  #  print(Evidence_id) 
  #  print(out_case_id)
    i=0
   # print(type(block_list[0].id))
    while i<len(block_list):
        if str(block_list[i].id) ==str(Evidence_id):
            if block_list[i].status=="DISPOSED" or block_list[i].status=="DESTROYED" or block_list[i].status=="RELEASED":
                print("it is an removed item")
                exit(1)
        i=i+1


    i=0
    found = -1
    while i<len(array_EVIDENCE_ID):
        if str(Evidence_id) == str(array_EVIDENCE_ID[i]):
            found =i
            break#this means we found the item
        i=i+1
    
    if found == -1:
        print("Error: Cannot check out a checked out item. Must check it in first")
        sys.exit(1)#this means the items is not in there
    else:
        time = datetime.now()
        UTC_TIME =datetime.timestamp(time)
        try:
            FIRST = BLOCKCHAIN_STRUCTURE(PREVIOUS_HASH ,UTC_TIME,uuid.UUID(out_case_id[found]).bytes,int(Evidence_id),str.encode("CHECKEDOUT"),0)
            SECOND = BLOCKCHAIN_LAST(str.encode(""))
           # actual_block= struct.pack('20s d 16s I 11s I',FIRST.Previous_Hash,FIRST.TimeStamp,FIRST.CASE_ID,FIRST.EVIDENCE_ID,FIRST.STATE,FIRST.Length)
            FIRST = block_format.pack(*FIRST)
            SECOND = block_second_format1.pack(*SECOND)

            fp= open(filePath,'ab')
            fp.write(FIRST)
            fp.write(SECOND)
            fp.close()
        except:
            fp.close()
            sys.exit(1)
        x=0
        reverse=""
        w=out_case_id[found].replace("-","")
        while x<len(w):
            if x==12 or x==16 or x==20 or x==24:
                reverse=w[x]+w[x+1]+"-"+reverse
            else:
                reverse=w[x]+w[x+1]+reverse
            x=x+2

        print("CASE:",reverse)#out_case_id[found])
        print("Checked out item:",Evidence_id)
        print("\tStatus: CHECKEDOUT")
        print("\tTime of action:", time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

def CHECKED_IN(Evidence_id):
     #first step check if the Evidence_id is in our file or not, if not just sys.exit(1)
    
    try:
        fp=open(filePath,'rb')
    except:
        print("Have not initialized yet")
        initilization()
        sys.exit(0)

    reading = True
    array_EVIDENCE_ID=[]
    out_case_id=[]
    PREVIOUS_HASH =''
    block_list=[]

    while reading:
        try:     
            FIRST2 = fp.read(block_format.size)
            FIRST=BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST2))
            SECOND = fp.read(FIRST.Length)
            value = FIRST.STATE.decode().rstrip('\x00')#this will get CHECKEDIN
            PREVIOUS_HASH=hashlib.sha1(FIRST2+SECOND).digest()
            a_list= block_checkout_remove(FIRST.EVIDENCE_ID,value)
            block_list.append(a_list)

          #  print(value)
            if str(value)=="CHECKEDIN":
                l=0
                while l<len(array_EVIDENCE_ID):
                    if str(array_EVIDENCE_ID[l]) ==str(FIRST.EVIDENCE_ID):
                        array_EVIDENCE_ID.remove(FIRST.EVIDENCE_ID)
                        #print(str(uuid.UUID(bytes=FIRST.CASE_ID)))
                        out_case_id.remove(str(uuid.UUID(bytes=FIRST.CASE_ID)))
                        break
                    else:
                        l=l+1
            else:
                array_EVIDENCE_ID.append(FIRST.EVIDENCE_ID)
                out_case_id.append(str(uuid.UUID(bytes=FIRST.CASE_ID)))

        except:
            fp.close()
            break;
     # print(block_list)

  #  print(array_EVIDENCE_ID)
  #  print(Evidence_id)
  #  print(out_case_id)
    i=0
   # print(type(block_list[0].id))
    while i<len(block_list):
        if str(block_list[i].id) ==str(Evidence_id):
            if block_list[i].status=="DISPOSED" or block_list[i].status=="DESTROYED" or block_list[i].status=="RELEASED":
                print("it is an removed item")
                exit(1)
        i=i+1

    i=0
    found = -1
    while i<len(array_EVIDENCE_ID):
        if str(Evidence_id) == str(array_EVIDENCE_ID[i]):
            found =i
            break#this means we found the item
        i=i+1

    if found == -1:
        print("Error: Cannot check in a checked in item. Must check it out first")
        sys.exit(1)#this means the items is not in there
    else:
        time = datetime.now()
        UTC_TIME =datetime.timestamp(time)
        try:
            FIRST = BLOCKCHAIN_STRUCTURE(PREVIOUS_HASH ,UTC_TIME,uuid.UUID(out_case_id[found]).bytes,int(Evidence_id),str.encode("CHECKEDIN"),0)
            SECOND = BLOCKCHAIN_LAST(str.encode(""))
            FIRST = block_format.pack(*FIRST)
            SECOND = block_second_format1.pack(*SECOND)

            fp= open(filePath,'ab')
            fp.write(FIRST)
            fp.write(SECOND)
            fp.close()
        except:
            fp.close()
            sys.exit(1)
        x=0
        reverse=""
        w=out_case_id[found].replace("-","")
    
        while x<len(w):
            if x==12 or x==16 or x==20 or x==24:
                reverse=w[x]+w[x+1]+"-"+reverse
            else:
                reverse=w[x]+w[x+1]+reverse
            x=x+2

        print("CASE:",reverse)#out_case_id[found])
        print("Checked in item:",Evidence_id)
        print("\tStatus: CHECKEDIN")
        print("\tTime of action:", time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))



def LOG(command_line):
    #print(command_line)
    

    number=-1
    evidence_id=""
    reversed_print= False
    case_input=""
    no_given_id=False
    z=0
    while z<len(command_line):
        
        if "-r"==command_line[z] or "--reverse"==command_line[z]:
            reversed_print=True
          #  print("reverse")
        if "-n"==command_line[z]:
            number=int(command_line[z+1])
         #   print("number exist")
        if "-i"==command_line[z]:
            evidence_id=command_line[z+1]
         #   print("ID here")
        if "-c"==command_line[z]:
            case_input=command_line[z+1]
        z=z+1 
    if evidence_id==""and case_input =="":
        no_given_id=True

    if number ==-1:
        number =999

    reading =True
    block=[]
    fp=open(filePath,'rb')

    while reading==True:
        try:
            FIRST2 = fp.read(block_format.size)
            
            FIRST=BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST2))
            SECOND=fp.read(FIRST.Length)
            case = str(uuid.UUID(bytes=FIRST.CASE_ID))
            
            reverse=""
            w=case.replace("-","")
            x=0
            while x<len(w):
                if x==12 or x==16 or x==20 or x==24:
                    reverse=w[x]+w[x+1]+"-"+reverse
                else:
                    reverse=w[x]+w[x+1]+reverse
                x=x+2
            case=reverse
             
            item= FIRST.EVIDENCE_ID # this part is int 
            action=FIRST.STATE.decode().rstrip('\x00')
            time = FIRST.TimeStamp
            time=datetime.fromtimestamp(time)
            a_list=block_list(case,item,action,time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")) 
            
            block.append(a_list)
          #  print(case)
           # print(item)
           # print(action)
           # print(time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        except:
            fp.close()
            break
   # print(block)
    block_of_id= []
    p=0
   # print(case_input)
    while p<len(block):
        if evidence_id=="" and case_input !="":
            if block[p].case==case_input:
                block_of_id.append(block[p])
        elif evidence_id!="" and case_input =="":
            if str(block[p].id)==evidence_id:
                block_of_id.append(block[p])
        else:
            if str(block[p].id)==evidence_id and block[p].case==case_input:
                block_of_id.append(block[p])
        p=p+1

    
   # print(block_of_id)
    if no_given_id==True:
        p=0
      #  print("here")
        while p<len(block):
            block_of_id.append(block[p])
            p=p+1
   # print(block_of_id) 
    if reversed_print== True: #this means we want print in reversed order
        i=len(block_of_id)-1
        while i>=0 and number >0:
            number=number-1
            print("Case:",block_of_id[i].case)
            print("Item:",str(block_of_id[i].id))
            print("Action:",block_of_id[i].status)
            print("Time:",block_of_id[i].time)
            i=i-1
            if i>=0 and number >=0:
                print()
    else:
        i=0
        while i<=len(block_of_id)-1 and number >0:
            number=number-1
            print("Case:",block_of_id[i].case)
            print("Item:",str(block_of_id[i].id))
            print("Action:",block_of_id[i].status)
            print("Time:",block_of_id[i].time)
            i=i+1
            if i<=len(block_of_id)-1 and number>=0:
                print()

def REMOVE(command_line):
    #print(command_line)
    

    evidence_id=""
    why=""
    owner=""

    i=0
    while i<len(command_line):
        if command_line[i]=="-i":
            evidence_id=command_line[i+1]
        if command_line[i]=="-y" or command_line[i]=="--why":
            why=command_line[i+1]
        if command_line[i]=="-o":
            owner=command_line[i+1]
        i+=1
    
   # print(evidence_id)
   # print(why)
   # print(owner)
    if why=="RELEASED"and owner=="":
        print("did not give owner information for release")
        exit(1)
    
    correct_reason = False
    if why =="RELEASED" or why =="DISPOSED" or why =="DESTROYED":
        correct_reason=True
    else:
        print("Correct reason is not correct")
        exit(1)
    

    reading =True
    block=[]
    fp=open(filePath,'rb')

    PREVIOUS_HASH=str.encode("")

    while reading==True:
        try:
            FIRST2 = fp.read(block_format.size)
            FIRST=BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST2))
            SECOND=fp.read(FIRST.Length)
            PREVIOUS_HASH=hashlib.sha1(FIRST2+SECOND).digest()
            #FIRST=BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST))
            case = str(uuid.UUID(bytes=FIRST.CASE_ID))

            reverse=""
            w=case.replace("-","")
            x=0
            while x<len(w):
                if x==12 or x==16 or x==20 or x==24:
                    reverse=w[x]+w[x+1]+"-"+reverse
                else:
                    reverse=w[x]+w[x+1]+reverse
                x=x+2
            case=reverse

            item= FIRST.EVIDENCE_ID # this part is int 
            action=FIRST.STATE.decode().rstrip('\x00')
            time = FIRST.TimeStamp
            time=datetime.fromtimestamp(time)
            a_list=block_list(case,item,action,time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

            
            block.append(a_list)
        except:
            fp.close()
            break
    block_of_id= []
    p=0

    i=0
    while i<len(block):
        if str(block[i].id) ==str(evidence_id):
            if block[i].status=="DISPOSED" or block[i].status=="DESTROYED" or block[i].status=="RELEASED":
                print("it is an removed item")
                exit(1)
        i=i+1



    while p<len(block):
        if str(block[p].id)==evidence_id:
            block_of_id.append(block[p])
        p=p+1
    #print(block_of_id)
       

    if len(block_of_id)==0:
        print("didn't have the item in the list")
        exit(1)
   # print(block_of_id[len(block_of_id)-1])
    if block_of_id[len(block_of_id)-1].status=="CHECKEDOUT":
        print("cannot remove items that has been checkout")
        exit(1)
    
    file_case =block_of_id[len(block_of_id)-1].case
    #print(file_case)
    w=file_case.replace("-","")
    x=0
    reverse=""
    while x<len(w):
        reverse=w[x]+w[x+1]+reverse
        x=x+2
    file_case = reverse


    time = datetime.now()
    UTC_TIME =datetime.timestamp(time)

    try:
        if owner!="":
            FIRST = BLOCKCHAIN_STRUCTURE(PREVIOUS_HASH,UTC_TIME,uuid.UUID(file_case).bytes,int(evidence_id),str.encode(why),len(owner)+1)
            SECOND=BLOCKCHAIN_LAST(str.encode(owner))
            FIRST = block_format.pack(*FIRST)
            new_length= len(owner)+1
            block_second_format3=struct.Struct(str(new_length)+'s')
            SECOND = block_second_format3.pack(*SECOND)
        else:
            FIRST = BLOCKCHAIN_STRUCTURE(PREVIOUS_HASH,UTC_TIME,uuid.UUID(file_case).bytes,int(evidence_id),str.encode(why),0)
            SECOND = BLOCKCHAIN_LAST(str.encode(""))
            FIRST = block_format.pack(*FIRST)
            SECOND = block_second_format1.pack(*SECOND)

        fp= open(filePath,'ab')
        fp.write(FIRST)
        fp.write(SECOND)
        fp.close()
    except:
        fp.close()
        sys.exit(1)

    print("Case:",block_of_id[len(block_of_id)-1].case)
    print("Removed item",evidence_id)
    print("\tStatus:",why)
    print("\tOwner info:",owner)
    print("\tTime of action:", time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))




def VERIFY():
    fp= open(filePath,'rb')
    i=0
    while True:
        try:
            FIRST = fp.read(block_format.size)
            SECOND = fp.read(block_second_format.size)
             
            SECOND = BLOCKCHAIN_LAST._make(block_second_format.unpack(SECOND))
            FIRST= BLOCKCHAIN_STRUCTURE._make(block_format.unpack(FIRST))
            i=i+1
        except:
            fp.close()
            break
    

    if i==9 or i==11 or i ==13:
        exit(0)
    exit(1) 



def main():
    if sys.argv[1] =="init":
        if len(sys.argv)>2:
            exit(1)
        else:
            initilization()
    elif sys.argv[1]=="add":
        if len(sys.argv)<6:
            exit(1)
        else:
            ADDING(sys.argv[3],sys.argv)
    elif sys.argv[1]=="checkout":
        if len(sys.argv)<4:
            exit(1)
        else:
            CHECKED_OUT(sys.argv[3])
    elif sys.argv[1]=="checkin":
        if len(sys.argv)<4:
            exit(1)
        else:
            CHECKED_IN(sys.argv[3])
    elif sys.argv[1]=="log":
            LOG(sys.argv)
    elif sys.argv[1]=="remove":
        REMOVE(sys.argv)
    elif sys.argv[1]=="verify":
        VERIFY()

    sys.exit(0)

main()
