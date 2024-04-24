import sys
from datetime import datetime
import hashlib
import os
import struct
import uuid
import collections

filePath= "INITIAL"  # for loco
block_format = struct.Struct('20s d 16s I 11s I')
block_second_format = struct.Struct('14s ')  ### this size should be variable and is specified by "Data Length"
BLOCKCHAIN_STRUCTURE = collections.namedtuple('BLOCKCHAIN_STRUCTURE',
                                              ['Previous_Hash', 'TimeStamp', 'CASE_ID', 'EVIDENCE_ID', 'STATE',
                                               'Length'])
BLOCKCHAIN_LAST = collections.namedtuple('BLOCKCHAIN_LAST', ['data'])
block_list = collections.namedtuple('block_list', ['case', 'id', 'status', 'time'])
block_checkout_remove = collections.namedtuple('block_checkout_remove', ['id', 'status'])



if __name__ == '__main__':
    #NONE = str.encode("Initial block");
    #print(type(NONE))
    #print(NONE.hex())

    #hexStr = '65cc391d65684dcca3f186a2f04140f3'
    print(uuid.UUID('65cc391d65684dcca3f186a2f04140f3'))
    print(uuid.UUID('65cc391d-6568-4dcc-a3f18-6a2f04140f3'))
    print(uuid.UUID('65cc391d-6568-4dcc-a3f18-6a2f04140f3').int)
    print(uuid.UUID('f34041f0a286f1a3cc4d68651d39cc65'))
    hexStr = '135312414559765810732748806252319031539'
    try:
        print(uuid.UUID(hexStr))
    except:
        print('execpt')
        hexInt = int(hexStr, 10)
        neohexstr = '{:x}'.format(hexInt)
        print('{:x}'.format(hexInt))
        print(uuid.UUID(neohexstr))

    fruits = ['lemon', 'pear', 'watermelon', 'tomato']
    print(fruits)
    print(*fruits)

    time = datetime.now()
    timestamp = datetime.timestamp(time)
    NONE = str.encode("");
    FIRST = BLOCKCHAIN_STRUCTURE(NONE, timestamp, NONE, 0, str.encode("INITIAL"), 14)
    SECOND = BLOCKCHAIN_LAST(str.encode("Initial block"))
    print(*FIRST)
    FIRST = block_format.pack(*FIRST)
    print(*FIRST)

